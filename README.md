# 🚑 CampusPulse: Accessible Multimodal Health & Safety Companion

A lightweight, accessible multimodal AI emergency companion powered by **Gemini** designed for immediate, structured first-aid guidance during minor or major campus medical emergencies, physical safety incidents, and laboratory hazards.

---

## 🌟 Key Features

### 1. 📷 Multimodal Incident & Hazard Triage
- **Text & Voice Input**: Real-time natural language symptom and hazard reporting with hands-free Speech-to-Text (`Web Speech API`).
- **Vision & Image Capture**: Upload or live-snap photos of injuries (burns, lacerations, sprains) or laboratory hazard labels (chemical bottles, NFPA hazard diamonds, spill warnings).
- **Gemini 2.5 / 2.0 Flash Intelligence**: Clinical triage structuring returning severity rating (*Low / Moderate / Severe*), bold immediate action, step-by-step numbered protocol, Do's & Don'ts, red-flag symptoms, and recommended supplies.
- **Zero-Latency Offline Fallback**: 25+ pre-compiled verified protocols (following American Red Cross and AHA standards) guaranteeing 100% functionality without internet.

### 2. ♿ Universal Accessibility Suite (WCAG 2.1 AAA Inspired)
- **🔊 Text-to-Speech (TTS)**: Instant voice readout of life-saving steps for rescuers in high-stress or low-visibility scenarios.
- **🟡 High Contrast Mode**: Pure black/yellow OLED high-contrast palette for maximum legibility in harsh lighting or for low-vision users.
- **📖 Dyslexia-Friendly Typography**: Adjusted letter-spacing and font glyphs to reduce visual crowding.
- **🔍 Large Text Scaling**: Instant one-click UI magnification.
- **💡 Plain-Language Mode**: Translates complex clinical terminology into clear 5th-grade reading level instructions.

### 3. 🌐 Multilingual Emergency Translation
- Instant one-tap translation of emergency protocols and safety placards into **10+ languages** (Spanish, Hindi, Mandarin, French, Arabic, German, etc.) with parallel dual-language display.

### 4. 💓 Action Guides & First-Aid Timers
- **CPR Metronome (110 BPM)**: Rhythmic audio-visual heartbeat guide for hands-only chest compressions.
- **Cool Water Rinse Timer (15 Min)**: Countdown timer for thermal burns.
- **Eyewash Continuous Flush Timer (15 Min)**: Essential laboratory safety tool for chemical eye exposure.
- **Direct Pressure Timer (5 Min)**: Uninterrupted bleeding control guide.
- **Interactive Checklists**: Checkable steps so rescuers don't skip critical procedures under panic.

### 5. 🆘 One-Touch Emergency SOS Dispatcher
- **Campus GPS & Building Selector**: Captures GPS coordinates and room locations.
- **Automated Dispatch Payload**: Generates tracking IDs and alerts **Campus Police (911)**, **Campus Health Center**, and **Lab Safety Officers**.
- **1-Tap Broadcast Links**: Pre-formatted `sms:911` and WhatsApp broadcast links.
- **🚨 Audio-Visual SOS Beacon**: Screen strobe and loud acoustic alarm for attracting immediate attention.

### 6. 🗺️ Campus AED & Safety Station Directory
- Real-time directory and distance calculation to nearest **AEDs (Defibrillators)**, **Emergency Eyewash & Showers**, and **First-Aid Kits**.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (Python 3.14 included)
- Packages: `fastapi`, `uvicorn`, `httpx`, `pydantic` (already installed)

### Running the Application
```bash
# Navigate to the project directory
cd C:\Users\Dell\.gemini\antigravity\scratch\campus_pulse

# Start the application server
python run.py
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:8000`**

### Running Automated Tests
```bash
python test_app.py
```

---

## ⚙️ Configuration & API Key

CampusPulse works immediately in **Verified Offline Mode** without requiring any API keys. 

To enable **Live Gemini 2.5 Flash Multimodal AI**:
1. Open the web app at `http://127.0.0.1:8000`.
2. Click **⚙️ Settings** in the top navigation bar.
3. Enter your Gemini API key (or set the environment variable `GEMINI_API_KEY=your_key`).
4. Click **Save Settings**.

---

## 📁 Project Architecture

```
campus_pulse/
├── main.py              # FastAPI backend (Gemini API proxy, SOS dispatcher, translation)
├── offline_data.py      # Verified first-aid protocol database & safety facilities
├── run.py               # Application startup script
├── test_app.py          # 10 automated test cases for backend endpoints
├── static/
│   ├── index.html       # Accessible semantic HTML5 layout
│   ├── styles.css       # High-contrast, dyslexia-friendly, responsive CSS system
│   └── app.js           # Multimodal handler, Web Speech, Web Audio metronome, SOS
└── README.md            # Documentation
```
