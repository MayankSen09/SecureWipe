import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from api.app import app
except Exception as e:
    import traceback
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse

    app = FastAPI()
    err_msg = str(e)
    tb_msg = traceback.format_exc()

    @app.get("/{full_path:path}")
    def catch_all(full_path: str = ""):
        return HTMLResponse(f"<h1>Startup Error</h1><p>{err_msg}</p><pre>{tb_msg}</pre>", status_code=500)
