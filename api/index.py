import os
import sys
from pathlib import Path

# Ensure both project root and api directory are present in sys.path
root_dir = Path(__file__).resolve().parent.parent
api_dir = Path(__file__).resolve().parent

for p in (str(root_dir), str(api_dir)):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from app import app
except ImportError:
    from api.app import app
