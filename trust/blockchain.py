"""
SecureWipe — trust/blockchain.py
Local blockchain ledger anchoring layer for certificate integrity verification.
Author: TEAM SOLUTION
"""

import hashlib
import json
import os
import sys
import time
from pathlib import Path

CHAIN_FILE = Path(__file__).parent / "chain.json"

def get_prev_hash() -> str:
    if os.path.exists(CHAIN_FILE):
        try:
            with open(CHAIN_FILE, "r", encoding="utf-8") as f:
                chain = json.load(f)
                if chain:
                    return chain[-1]["block_hash"]
        except Exception:
            pass
    return "0" * 64

def prepare_block(cert_meta: dict) -> dict:
    """Pre-calculates an anchor block before PDF generation."""
    prev_hash = get_prev_hash()
    meta_str = json.dumps(cert_meta, sort_keys=True)
    meta_hash = hashlib.sha256(meta_str.encode("utf-8")).hexdigest()
    
    timestamp = cert_meta.get("timestamp", time.time())
    
    block_raw = {
        "timestamp": timestamp,
        "meta_hash": meta_hash,
        "prev_hash": prev_hash,
        "device": cert_meta.get("device", ""),
        "serial": cert_meta.get("serial", ""),
        "method": cert_meta.get("method", ""),
        "confidence_score": cert_meta.get("confidence_score", 100),
    }
    block_hash = hashlib.sha256(json.dumps(block_raw, sort_keys=True).encode("utf-8")).hexdigest()
    block_raw["block_hash"] = block_hash
    return block_raw

def anchor(cert_path: str, block_info: dict = None) -> str:
    """
    Anchors the final PDF file and appends the block into trust/chain.json.
    """
    with open(cert_path, "rb") as f:
        pdf_hash = hashlib.sha256(f.read()).hexdigest()

    chain = []
    if os.path.exists(CHAIN_FILE):
        try:
            with open(CHAIN_FILE, "r", encoding="utf-8") as f:
                chain = json.load(f)
        except Exception:
            chain = []

    if block_info is None:
        block_info = prepare_block({"pdf_hash": pdf_hash, "timestamp": time.time()})

    block_info["cert_pdf_hash"] = pdf_hash
    block_info["index"] = len(chain)

    chain.append(block_info)
    CHAIN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHAIN_FILE, "w", encoding="utf-8") as f:
        json.dump(chain, f, indent=2)

    return block_info["block_hash"]

def verify_chain() -> tuple[bool, str]:
    if not os.path.exists(CHAIN_FILE):
        return True, "Chain file does not exist yet."

    try:
        with open(CHAIN_FILE, "r", encoding="utf-8") as f:
            chain = json.load(f)
    except Exception as e:
        return False, f"Failed to read chain JSON: {e}"

    for i, block in enumerate(chain):
        expected_prev = "0" * 64 if i == 0 else chain[i - 1]["block_hash"]
        if block.get("prev_hash") != expected_prev:
            return False, f"Tamper detected at block #{i}: prev_hash linkage broken!"

        saved_hash = block.get("block_hash")
        block_copy = {k: v for k, v in block.items() if k not in ("block_hash", "cert_pdf_hash", "index")}
        calc_hash = hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode("utf-8")).hexdigest()
        if saved_hash != calc_hash:
            return False, f"Tamper detected at block #{i}: block content modified!"

    return True, f"Chain intact — {len(chain)} blocks verified."

if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    valid, msg = verify_chain()
    print("CHAIN INTEGRITY CHECK:")
    print("STATUS:", "[OK] VERIFIED" if valid else "[FAIL] ALTERED / TAMPERED")
    print("DETAILS:", msg)
    sys.exit(0 if valid else 1)
