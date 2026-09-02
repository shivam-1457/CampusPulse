import sys
import os

# Add root directory to sys.path so modules can be imported by Vercel serverless runtime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Vercel entrypoint
app = app
