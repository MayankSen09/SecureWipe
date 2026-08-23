import os
import sys
import traceback
from pathlib import Path

# Add project root and api directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
API_DIR = Path(__file__).resolve().parent

for p in (str(BASE_DIR), str(API_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from api.app import app
except Exception as err:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse, HTMLResponse
    
    app = FastAPI(title="TrustWipe API Emergency Diagnostic Fallback")
    
    @app.get("/")
    @app.get("/{full_path:path}")
    def catch_all_error(full_path: str = ""):
        tb = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(err),
                "traceback": tb,
                "sys_path": sys.path
            }
        )
