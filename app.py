"""
SecureWipe — app.py
Root-level FastAPI entrypoint for Vercel deployment.
"""

import json
import sys
import time
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI(
    title="SecureWipe Verification & PDF Certificate Generator API",
    description="REST API for tamper-proof data sanitization verification and blockchain anchoring.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve paths relative to project root
BASE_DIR = Path(__file__).resolve().parent
CHAIN_FILE = BASE_DIR / "trust" / "chain.json"
WEB_DIR = BASE_DIR / "web"

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


def _load_chain():
    if CHAIN_FILE.exists():
        try:
            with open(CHAIN_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


@app.get("/")
def read_root():
    index_file = WEB_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8", errors="replace"))
    return {"status": "ok", "message": "SecureWipe Verification & PDF Generator API is operational."}


@app.get("/api/v1/health")
def health_check():
    chain = _load_chain()
    return {
        "status": "healthy",
        "service": "SecureWipe Verification Node",
        "version": "2.0.0",
        "platform": sys.platform,
        "ledger_blocks": len(chain),
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }


@app.get("/verify")
def verify_hash(hash: str = Query(..., description="Blockchain block hash to verify")):
    clean_hash = _normalize_hash(hash)
    chain = _load_chain()

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
                "recycling_eligible": True,
                "circular_economy_status": "Verified Safe for Resale & Circular Recycling",
                "recommended_recyclers": CERTIFIED_RECYCLERS
            }

    return JSONResponse(
        status_code=404,
        content={
            "verified": False,
            "message": "Certificate block hash not found in blockchain ledger. Invalid or tampered certificate."
        }
    )


@app.get("/api/blocks")
def get_blocks(limit: int = Query(50, description="Number of recent blocks to retrieve")):
    chain = _load_chain()
    # Reverse to get newest blocks first
    chain.reverse()
    return {
        "status": "success",
        "total_blocks": len(chain),
        "blocks": chain[:limit]
    }


@app.get("/recyclers")
def get_recyclers():
    return {"status": "success", "recyclers": CERTIFIED_RECYCLERS}


@app.get("/api/disks")
def list_disks_api():
    return {
        "status": "success",
        "disks": [
            {
                "device": "\\\\.\\PhysicalDrive0 [Demo]",
                "model": "Samsung SSD 870 EVO 500GB",
                "serial": "S5YXNX0T654321",
                "size_human": "465.8 GiB",
                "disk_type": "SSD",
                "encryption": "none",
                "is_system": False
            },
            {
                "device": "\\\\.\\PhysicalDrive1 [Demo]",
                "model": "Kingston DataTraveler 3.0",
                "serial": "KGT30USB998877",
                "size_human": "64.0 GiB",
                "disk_type": "USB",
                "encryption": "none",
                "is_system": False
            }
        ]
    }
