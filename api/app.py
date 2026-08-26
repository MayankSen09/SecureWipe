"""
SecureWipe — api/app.py
Legacy entrypoint. Imports from root app.py.
"""
from app import app, health_check, get_recyclers, list_disks_api, verify_hash, MockDisk

