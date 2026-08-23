import os
import sys
from pathlib import Path

# Ensure project root and api directory are present in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
API_DIR = Path(__file__).resolve().parent

for p in (str(BASE_DIR), str(API_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

# Top-level ASGI app entrypoint for Vercel
from api.app import app

# Alias handler for Vercel Serverless Function compatibility
handler = app
