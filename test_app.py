"""
Automated unit & integration tests for CampusPulse backend.
"""

import os
import json
import base64
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_index_page():
    res = client.get("/")
    assert res.status_code == 200
    assert "CampusPulse" in res.text

def test_get_facilities():
    res = client.get("/api/facilities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 4
    assert any(f["type"] == "AED" for f in data)

def test_get_contacts():
    res = client.get("/api/contacts")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert any(c["id"] == "campus_police" for c in data)

def test_get_protocols():
    res = client.get("/api/protocols")
    assert res.status_code == 200
    data = res.json()
    assert "burn" in data
    assert "chemical_splash" in data
    assert "cpr" in data
    assert "anaphylaxis" in data

def test_analyze_burn_fallback():
    payload = {
        "text": "Student touched hot heating mantle in organic chemistry lab, red skin and blistering",
        "language": "en"
    }
    res = client.post("/api/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "burn" in data["title"].lower() or "thermal" in data["title"].lower()
    assert len(data["steps"]) >= 3
    assert len(data["dos"]) >= 1
    assert len(data["donts"]) >= 1
    assert "immediate_action" in data

def test_analyze_chemical_splash_fallback():
    payload = {
        "text": "Acid chemical splash in student eyes from broken glassware",
        "language": "en"
    }
    res = client.post("/api/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "chemical" in data["title"].lower() or "splash" in data["title"].lower()
    assert "eyewash" in data["immediate_action"].lower() or "flush" in data["immediate_action"].lower()

def test_analyze_cpr_fallback():
    payload = {
        "text": "Person collapsed on basketball court, unresponsive, no pulse or breathing",
        "language": "en"
    }
    res = client.post("/api/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "cpr" in data["title"].lower() or "cardiac" in data["title"].lower()
    assert data["timer_type"] == "cpr_metronome"

def test_analyze_with_image():
    # 1x1 transparent PNG base64
    sample_img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    payload = {
        "text": "Hazard sign inspection",
        "image_base64": sample_img,
        "language": "en"
    }
    res = client.post("/api/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "immediate_action" in data

def test_translate_endpoint():
    payload = {
        "text": "Cool immediately with cool running water for 15 minutes",
        "target_language": "es"
    }
    res = client.post("/api/translate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "translated_text" in data
    assert data["target_language"] == "es"

def test_sos_dispatch():
    payload = {
        "incident_type": "Chemical Splash",
        "severity": "severe",
        "location": {
            "building": "Chemistry Hall",
            "room": "Lab 304",
            "latitude": 37.7749,
            "longitude": -122.4194
        },
        "summary": "Hydrochloric acid splash to forearm, eyewash active",
        "contacts_to_notify": ["campus_police", "health_center", "lab_safety"]
    }
    res = client.post("/api/sos/dispatch", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ACTIVE_EMERGENCY_DISPATCHED"
    assert "tracking_id" in data
    assert "sms_url" in data
    assert "whatsapp_url" in data
    assert len(data["notified_contacts"]) == 3

if __name__ == "__main__":
    test_index_page()
    test_get_facilities()
    test_get_contacts()
    test_get_protocols()
    test_analyze_burn_fallback()
    test_analyze_chemical_splash_fallback()
    test_analyze_cpr_fallback()
    test_analyze_with_image()
    test_translate_endpoint()
    test_sos_dispatch()
    print("ALL 10 TESTS PASSED SUCCESSFULLY! [OK]")
