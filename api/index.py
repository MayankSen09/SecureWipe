import os
import sys
import traceback
from pathlib import Path

# Ensure project root and api directory are present in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
API_DIR = Path(__file__).resolve().parent

for p in (str(BASE_DIR), str(API_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from api.app import app
    handler = app
except Exception as err:
    tb = traceback.format_exc()
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI(title="SecureWipe Diagnostic Handler")

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    def diagnostic_route(full_path: str = ""):
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(err),
                "traceback": tb,
                "sys_path": sys.path
            }
        )
    handler = app
