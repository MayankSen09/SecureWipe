import os
import sys
from pathlib import Path

# Add workspace root to sys.path for Vercel module resolution
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from api.app import app
