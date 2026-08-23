import json
import time
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path(__file__).resolve().parent.parent
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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/api/v1/health":
            block_count = 0
            if CHAIN_FILE.exists():
                try:
                    with open(CHAIN_FILE, "r", encoding="utf-8") as f:
                        block_count = len(json.load(f))
                except Exception:
                    pass
            body = json.dumps({
                "status": "healthy",
                "service": "SecureWipe Verification Node",
                "version": "2.0.0",
                "ledger_blocks": block_count
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/verify":
            raw_hash = params.get("hash", [""])[0].strip()
            if raw_hash.lower().startswith("0x"):
                raw_hash = raw_hash[2:]

            if CHAIN_FILE.exists():
                try:
                    with open(CHAIN_FILE, "r", encoding="utf-8") as f:
                        chain = json.load(f)
                    for block in chain:
                        if block.get("block_hash") == raw_hash:
                            ts = block.get("timestamp", time.time())
                            ts_human = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(ts))
                            res = {
                                "verified": True,
                                "block_hash": block.get("block_hash"),
                                "prev_hash": block.get("prev_hash"),
                                "report_id": block.get("report_id", "SW-REC-" + raw_hash[:8].upper()),
                                "device": block.get("device", "Enterprise Storage Drive"),
                                "serial": block.get("serial", "SW-SN-" + raw_hash[:6].upper()),
                                "method": block.get("method", "NIST SP 800-88 Purge"),
                                "confidence_score": block.get("confidence_score", 100),
                                "timestamp": ts,
                                "timestamp_human": ts_human,
                                "sha256": block.get("sha256", raw_hash),
                                "cert_pdf_hash": block.get("cert_pdf_hash", raw_hash[:16]),
                                "pdf_download_url": f"/download-pdf?hash={raw_hash}",
                                "recycling_eligible": True,
                                "circular_economy_status": "Verified Safe for Resale & Circular Recycling",
                                "recommended_recyclers": CERTIFIED_RECYCLERS
                            }
                            body = json.dumps(res).encode("utf-8")
                            self.send_response(200)
                            self.send_header("Content-Type", "application/json")
                            self.end_headers()
                            self.wfile.write(body)
                            return
                except Exception:
                    pass

            body = json.dumps({
                "verified": False,
                "message": "Certificate block hash not found in blockchain ledger. Invalid or tampered certificate."
            }).encode("utf-8")
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/recyclers":
            body = json.dumps({"status": "success", "recyclers": CERTIFIED_RECYCLERS}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
            return

        index_file = WEB_DIR / "index.html"
        if index_file.exists():
            html = index_file.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html)
            return

        body = json.dumps({"status": "ok", "message": "SecureWipe Verification & PDF Generator API is operational."}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)
