import os
import sys
import json
import time
import tempfile
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse, Response

app = FastAPI(
    title="SecureWipe Verification & PDF Certificate Generator API",
    description="REST API for tamper-proof data sanitization verification, PDF certificate generation, and blockchain anchoring.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
for p in (str(BASE_DIR), str(Path(__file__).resolve().parent), str(Path.cwd())):
    if p not in sys.path:
        sys.path.insert(0, p)

possible_chain_files = [
    BASE_DIR / "trust" / "chain.json",
    Path(__file__).resolve().parent / "trust" / "chain.json",
    Path.cwd() / "trust" / "chain.json",
]
CHAIN_FILE = next((f for f in possible_chain_files if f.exists()), BASE_DIR / "trust" / "chain.json")

possible_web_dirs = [
    BASE_DIR / "web",
    Path(__file__).resolve().parent / "web",
    Path.cwd() / "web",
]
WEB_DIR = next((d for d in possible_web_dirs if (d / "index.html").exists()), BASE_DIR / "web")

CERTIFIED_RECYCLERS = [
    {
        "id": "rec_01",
        "name": "Attero Recycling",
        "type": "E-Waste Recycler & Extractor",
        "accreditation": "CPCB Certified",
        "location": "Noida / Pan-India",
        "estimated_payout": "₹8,500 - ₹24,000 / unit"
    },
    {
        "id": "rec_02",
        "name": "Karo Sambhav",
        "type": "Producer Responsibility Organisation (PRO)",
        "accreditation": "E-Waste Rules 2022 Compliant",
        "location": "Gurugram / National Network",
        "estimated_payout": "Enterprise Asset Recovery"
    },
    {
        "id": "rec_03",
        "name": "Cashify Refurbish",
        "type": "IT Asset Refurbisher & Reseller",
        "accreditation": "Data Sanitization Verified",
        "location": "Pan-India Pickup",
        "estimated_payout": "Instant Bank Payout"
    }
]

def _normalize_hash(raw: str) -> str:
    h = raw.strip()
    if h.lower().startswith("0x"):
        h = h[2:]
    return h

@app.get("/", tags=["Verification & Ledger"])
@app.get("/api/index", tags=["Verification & Ledger"])
@app.get("/api/index.py", tags=["Verification & Ledger"])
def read_root():
    try:
        index_file = WEB_DIR / "index.html"
        if index_file.exists():
            return HTMLResponse(content=index_file.read_text(encoding="utf-8", errors="replace"))
    except Exception as e:
        return JSONResponse({"status": "ok", "message": "SecureWipe API operational", "error": str(e)})
    return {"status": "ok", "message": "SecureWipe Verification & PDF Generator API is operational."}

@app.get("/api/v1/health", tags=["Verification & Ledger"])
def health_check():
    block_count = 0
    if CHAIN_FILE.exists():
        try:
            with open(CHAIN_FILE, "r", encoding="utf-8") as f:
                chain = json.load(f)
                block_count = len(chain)
        except Exception:
            pass

    return {
        "status": "healthy",
        "service": "SecureWipe Verification Node",
        "version": "2.0.0",
        "platform": sys.platform,
        "ledger_blocks": block_count,
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }

@app.get("/verify", tags=["Verification & Ledger"])
def verify_hash(hash: str = Query(..., description="Blockchain block hash to verify")):
    clean_hash = _normalize_hash(hash)

    if CHAIN_FILE.exists():
        try:
            with open(CHAIN_FILE, "r", encoding="utf-8") as f:
                chain = json.load(f)
            for block in chain:
                if block.get("block_hash") == clean_hash:
                    ts = block.get("timestamp", time.time())
                    ts_human = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(ts))
                    return {
                        "verified": True,
                        "block_hash": block.get("block_hash"),
                        "prev_hash": block.get("prev_hash"),
                        "report_id": block.get("report_id", "SW-REC-" + clean_hash[:8].upper()),
                        "device": block.get("device", "Enterprise Storage Drive"),
                        "serial": block.get("serial", "SW-SN-" + clean_hash[:6].upper()),
                        "method": block.get("method", "NIST SP 800-88 Purge"),
                        "confidence_score": block.get("confidence_score", 100),
                        "timestamp": ts,
                        "timestamp_human": ts_human,
                        "sha256": block.get("sha256", clean_hash),
                        "cert_pdf_hash": block.get("cert_pdf_hash", clean_hash[:16]),
                        "pdf_download_url": f"/download-pdf?hash={clean_hash}",
                        "recycling_eligible": True,
                        "circular_economy_status": "Verified Safe for Resale & Circular Recycling",
                        "recommended_recyclers": CERTIFIED_RECYCLERS
                    }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read ledger: {str(e)}")

    return JSONResponse(
        status_code=404,
        content={
            "verified": False,
            "message": "Certificate block hash not found in blockchain ledger. Invalid or tampered certificate."
        }
    )

@app.get("/recyclers")
def get_recyclers():
    return {"status": "success", "recyclers": CERTIFIED_RECYCLERS}

try:
    from a2wsgi import ASGIMiddleware
    handler = ASGIMiddleware(app)
except Exception:
    handler = app
