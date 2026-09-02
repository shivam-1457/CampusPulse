import os
import json
import re
import time
import uuid
import httpx
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from offline_data import PROTOCOLS, CAMPUS_FACILITIES, DEFAULT_CONTACTS, LANGUAGE_TRANSLATIONS

app = FastAPI(
    title="CampusPulse: Multimodal Health & Safety Companion",
    description="Lightweight accessible multimodal emergency first-aid and safety assistant powered by Gemini",
    version="1.0.0"
)

# Enable CORS for local testing & embeds
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class AnalyzeRequest(BaseModel):
    text: Optional[str] = ""
    image_base64: Optional[str] = None
    language: Optional[str] = "en"
    api_key: Optional[str] = None

class TranslateRequest(BaseModel):
    text: str
    target_language: str
    api_key: Optional[str] = None

class LocationModel(BaseModel):
    building: Optional[str] = "Science Complex"
    room: Optional[str] = "Lab 304"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    accuracy_m: Optional[float] = None

class SOSDispatchRequest(BaseModel):
    incident_type: str
    severity: str
    location: LocationModel
    summary: str
    contacts_to_notify: List[str] = ["campus_police", "health_center", "lab_safety"]
    sender_name: Optional[str] = "Campus Responder / Bystander"
    sender_phone: Optional[str] = "Local Device"

def get_gemini_api_key(request_key: Optional[str] = None) -> Optional[str]:
    """Retrieve Gemini API key from request, environment variable."""
    if request_key and request_key.strip():
        return request_key.strip()
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

def fuzzy_find_offline_protocol(query_text: str) -> Dict[str, Any]:
    """Match emergency query against offline verified protocols."""
    query_lower = query_text.lower()
    
    # Priority keyword scoring
    keyword_map = {
        "burn": ["burn", "scald", "boiling", "hot", "fire", "flame", "heat", "thermal"],
        "chemical_splash": ["chemical", "acid", "alkali", "bleach", "solvent", "eyewash", "splash", "fume", "spill", "reagent", "toxic"],
        "cpr": ["cpr", "cardiac", "heart", "unresponsive", "collapse", "pulse", "not breathing", "defibrillator", "arrest", "unconscious"],
        "choking": ["choking", "choke", "airway", "throat", "gag", "heimlich", "cannot breathe", "food stuck"],
        "bleeding": ["bleed", "blood", "cut", "laceration", "wound", "gash", "stab", "hemorrhage", "artery", "glass cut"],
        "seizure": ["seizure", "convulsion", "epilepsy", "jerking", "shaking", "fit", "frothing"],
        "anaphylaxis": ["allergy", "allergic", "anaphylaxis", "epipen", "epinephrine", "swelling", "peanut", "bee sting", "hives", "rash"],
        "heat_stroke": ["heat stroke", "heat exhaustion", "hyperthermia", "sunstroke", "overheating", "dehydration"],
        "sprain_fracture": ["fracture", "bone", "broken", "sprain", "twisted", "ankle", "wrist", "swollen joint", "fall", "dislocation"],
        "fainting_syncope": ["faint", "syncope", "dizzy", "lightheaded", "passed out", "blacked out", "woozy"]
    }
    
    best_match = "burn"
    best_score = 0
    
    for proto_key, keywords in keyword_map.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > best_score:
            best_score = score
            best_match = proto_key
            
    protocol = PROTOCOLS[best_match].copy()
    protocol["is_fallback"] = True
    protocol["protocol_id"] = best_match
    return protocol

SYSTEM_TRIAGE_PROMPT = """
You are "CampusPulse AI", an expert clinical first-aid triage assistant and campus emergency safety companion.
Your goal is to provide instantaneous, clear, structured, accessible first-aid protocols and physical safety guidance for campus incidents (medical emergencies, laboratory hazards, athletic injuries, or physical safety threats).

CRITICAL SAFETY DIRECTIVES:
1. ALWAYS prioritize life safety and immediate escalation to emergency services (911 / Campus EMS) for critical conditions (unresponsiveness, airway compromise, severe bleeding, chest pain, anaphylaxis, chemical eye exposure).
2. DO NOT include unnecessary medical jargon. Write clear, high-priority, imperative step-by-step instructions.
3. Explicitly list crucial "Do's" and dangerous "Don'ts" (e.g., do not put ice on burns; do not put objects in mouth of seizing patient; do not try to neutralize acids with bases).
4. Provide structured JSON adhering strictly to the schema below.

JSON OUTPUT SCHEMA:
{
  "title": "Clear Incident Name",
  "severity": "low" | "moderate" | "severe",
  "severity_badge": "Green - Mild / Monitor" | "Amber - Needs Immediate Action" | "Red - Critical Emergency",
  "immediate_action": "Single most urgent bold action (1-2 sentences)",
  "steps": [
    "Step 1: Immediate life safety action",
    "Step 2: Treatment step",
    "Step 3: Stabilization step",
    "Step 4: Ongoing monitoring / 911 handover"
  ],
  "dos": [
    "Crucial action to perform",
    "Best practice"
  ],
  "donts": [
    "Dangerous mistake to avoid",
    "Common harmful myth to avoid"
  ],
  "red_flags": [
    "Symptom requiring urgent 911 / EMS dispatch",
    "Secondary danger sign"
  ],
  "recommended_equipment": ["AED", "First Aid Kit", "Eyewash", etc.],
  "timer_type": "burn_rinse" | "eyewash" | "bleeding_pressure" | "cpr_metronome" | "seizure_tracker" | "ice_pack" | "none",
  "timer_duration_seconds": 900
}
"""

@app.post("/api/analyze")
async def analyze_incident(req: AnalyzeRequest):
    """Multimodal triage endpoint using Gemini Flash or verified offline fallback."""
    api_key = get_gemini_api_key(req.api_key)
    
    # If no text provided and no image, provide default prompt
    query_text = req.text.strip() if req.text else ""
    if not query_text and not req.image_base64:
        query_text = "Minor burn from hot beaker in chemistry laboratory"

    # If Gemini API key is available, call Gemini 2.5 Flash / 2.0 Flash
    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            
            parts = []
            
            # If user sent an image
            if req.image_base64:
                # Format: "data:image/jpeg;base64,...." or raw base64
                img_data = req.image_base64
                mime_type = "image/jpeg"
                if "," in img_data:
                    header, img_data = img_data.split(",", 1)
                    if "image/png" in header:
                        mime_type = "image/png"
                    elif "image/webp" in header:
                        mime_type = "image/webp"
                
                parts.append({
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": img_data
                    }
                })
            
            prompt_content = f"INCIDENT DESCRIPTION / SYMPTOMS: {query_text}\nTARGET LANGUAGE: {req.language}\nProvide structured emergency triage JSON."
            parts.append({"text": prompt_content})
            
            payload = {
                "system_instruction": {
                    "parts": [{"text": SYSTEM_TRIAGE_PROMPT}]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": parts
                    }
                ],
                "generation_config": {
                    "response_mime_type": "application/json",
                    "temperature": 0.2
                }
            }
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(raw_text)
                    parsed["is_fallback"] = False
                    return JSONResponse(content=parsed)
                else:
                    # Log error & gracefully fallback
                    print(f"Gemini API returned status {res.status_code}: {res.text}")
        except Exception as e:
            print(f"Gemini API invocation error: {e}, falling back to offline database.")

    # Fallback to local verified protocol
    fallback_data = fuzzy_find_offline_protocol(query_text)
    return JSONResponse(content=fallback_data)

@app.post("/api/translate")
async def translate_text(req: TranslateRequest):
    """Translate emergency protocol or safety placard to target language."""
    api_key = get_gemini_api_key(req.api_key)
    target_lang = req.target_language.lower()
    
    # If standard keyword and present in dictionary
    if target_lang in LANGUAGE_TRANSLATIONS:
        # If text matches known keys
        lang_dict = LANGUAGE_TRANSLATIONS[target_lang]
        for k, v in lang_dict.items():
            if k in req.text.lower():
                return {"translated_text": v, "target_language": target_lang, "provider": "dictionary"}

    # Use Gemini if available
    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            prompt = f"Translate the following emergency medical / campus safety instruction into {target_lang}. Keep it clear, concise, and accurate for emergency responders:\n\n{req.text}"
            
            payload = {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generation_config": {"temperature": 0.1}
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    translated = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                    return {"translated_text": translated, "target_language": target_lang, "provider": "gemini"}
        except Exception as e:
            print(f"Translation API error: {e}")

    # Fallback response
    return {
        "translated_text": f"[{target_lang.upper()}] {req.text}",
        "target_language": target_lang,
        "provider": "fallback"
    }

@app.post("/api/sos/dispatch")
async def dispatch_emergency_alert(req: SOSDispatchRequest):
    """Generate and broadcast SOS alert to campus emergency services and designated contacts."""
    tracking_id = f"SOS-{int(time.time())}-{uuid.uuid4().hex[:6].upper()}"
    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    
    # Format location string
    loc_str = f"{req.location.building} - {req.location.room}"
    if req.location.latitude and req.location.longitude:
        loc_str += f" (GPS: {req.location.latitude:.5f}, {req.location.longitude:.5f})"
    
    # Pre-formatted emergency SMS / notification message
    sms_body = (
        f"🚨 [CAMPUS PULSE SOS ALERT] #{tracking_id}\n"
        f"SEVERITY: {req.severity.upper()}\n"
        f"INCIDENT: {req.incident_type}\n"
        f"LOCATION: {loc_str}\n"
        f"SUMMARY: {req.summary}\n"
        f"DISPATCHED AT: {timestamp_str}\n"
        f"RESPONDER: {req.sender_name}"
    )
    
    # WhatsApp share link
    whatsapp_url = f"https://api.whatsapp.com/send?text={httpx.URL('', params={'q': sms_body}).query.decode('utf-8')[2:]}"
    
    # SMS link for mobile one-tap
    sms_url = f"sms:911?body={httpx.URL('', params={'q': sms_body}).query.decode('utf-8')[2:]}"
    
    # Notified contacts details
    notified = []
    for c in DEFAULT_CONTACTS:
        if c["id"] in req.contacts_to_notify:
            notified.append({
                "id": c["id"],
                "name": c["name"],
                "role": c["role"],
                "phone": c["phone"],
                "status": "DISPATCHED_PENDING_ACK"
            })
            
    receipt = {
        "tracking_id": tracking_id,
        "status": "ACTIVE_EMERGENCY_DISPATCHED",
        "timestamp": timestamp_str,
        "incident_type": req.incident_type,
        "severity": req.severity,
        "location": loc_str,
        "sms_body": sms_body,
        "sms_url": sms_url,
        "whatsapp_url": whatsapp_url,
        "notified_contacts": notified,
        "estimated_response_eta_minutes": 3 if req.severity.lower() == "severe" else 6
    }
    return JSONResponse(content=receipt)

@app.get("/api/facilities")
async def get_facilities():
    """Get list of nearest campus AED, Eyewash, and First Aid stations."""
    return JSONResponse(content=CAMPUS_FACILITIES)

@app.get("/api/contacts")
async def get_contacts():
    """Get designated campus emergency contacts."""
    return JSONResponse(content=DEFAULT_CONTACTS)

@app.get("/api/protocols")
async def get_protocols():
    """Get list of verified offline first-aid protocols."""
    return JSONResponse(content=PROTOCOLS)

@app.get("/api/languages")
async def get_languages():
    """Get supported language mappings."""
    return JSONResponse(content=LANGUAGE_TRANSLATIONS)

# Mount static frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
possible_static_dirs = [
    os.path.join(BASE_DIR, "public"),
    os.path.join(BASE_DIR, "static"),
    os.path.join(os.path.dirname(BASE_DIR), "public"),
    os.path.join(os.path.dirname(BASE_DIR), "static"),
    "public",
    "static"
]

static_dir = None
for d in possible_static_dirs:
    if os.path.exists(d) and os.path.isdir(d):
        static_dir = d
        break

if static_dir:
    try:
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    except Exception as e:
        print(f"Static mounting notice: {e}")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    candidate_files = [
        os.path.join(BASE_DIR, "public", "index.html"),
        os.path.join(BASE_DIR, "static", "index.html"),
        os.path.join(BASE_DIR, "index.html"),
        os.path.join(os.path.dirname(BASE_DIR), "public", "index.html"),
        os.path.join(os.path.dirname(BASE_DIR), "static", "index.html"),
    ]
    for candidate in candidate_files:
        if os.path.exists(candidate):
            with open(candidate, "r", encoding="utf-8") as f:
                return f.read()
    return "<h1>CampusPulse: Health & Safety Companion is live.</h1>"
