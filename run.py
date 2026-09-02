"""
Runner script for CampusPulse application.
Launches FastAPI backend on http://127.0.0.1:8000
"""

import sys
import uvicorn

if __name__ == "__main__":
    print("================================================================")
    print("🚑 Starting CampusPulse: Accessible Multimodal Health Companion")
    print("🌐 Web Application available at: http://127.0.0.1:8000")
    print("================================================================")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
