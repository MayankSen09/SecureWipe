import sys
import traceback
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from api.app import app
except Exception as e:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI()
    err_str = traceback.format_exc()

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"])
    def catch_all(full_path: str = ""):
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": err_str})
