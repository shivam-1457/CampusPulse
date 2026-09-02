"""
Runner script for CampusPulse application.
Launches FastAPI backend with dynamic port resolution for local development & Render/cloud deployment.
"""

import os
import sys
import uvicorn

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    
    print("================================================================")
    print("🚑 Starting CampusPulse: Accessible Multimodal Health Companion")
    print(f"🌐 Server binding on: http://{host}:{port}")
    print("================================================================")
    uvicorn.run("main:app", host=host, port=port, reload=False, log_level="info")
