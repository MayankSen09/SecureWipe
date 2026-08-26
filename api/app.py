"""
SecureWipe — api/app.py
Vercel Serverless Function entrypoint.
"""
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import app, health_check, get_recyclers, list_disks_api, verify_hash, MockDisk
