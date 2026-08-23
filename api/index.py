import os
import sys
from pathlib import Path

# Add project root and api directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
API_DIR = Path(__file__).resolve().parent

for p in (str(BASE_DIR), str(API_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from api.app import app
