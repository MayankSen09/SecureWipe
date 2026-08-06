# 🛡️ SecureWipe — Enterprise Secure Data Wiping Platform

## 📌 Executive Summary

**SecureWipe** is an enterprise-grade secure data wiping and verification platform designed for trustworthy IT asset disposal and recycling. SecureWipe includes cryptographically verifiable auditability, multi-layered wiping confidence scoring, tamper-proof blockchain certificate anchoring, hidden storage detection, and cross-platform mobile asset wiping.

---

## ✨ Key Features & Technical Extensions

| Module | Location | Description |
| :--- | :--- | :--- |
| **Confidence Score Engine** | `core/confidence.py` | Calculates a 0–100 audit score based on firmware erase success (50 pts), random sector sampling pass (30 pts), and hidden area (HPA) sanitization (20 pts). |
| **Blockchain Anchoring** | `trust/blockchain.py` | SHA-256 local block-chain ledger ensuring certificate immutability and instant tamper detection (`trust/chain.json`). |
| **Verification Portal** | `api/app.py` & `web/index.html` | FastAPI REST service + modern clean web portal for instant QR-code proof validation. |
| **Hidden Area Detection (HPA)** | `core/disk_linux.py` | `hdparm -N` sector analysis comparing physical disk boundaries against native max address. |
| **Android Asset Agent** | `android/agent.py` | ADB / Fastboot mobile asset wipe agent with full `--mock` mode support. |
| **Standards Compliance** | `core/wipe_engine.py` | Full implementation of NIST SP 800-88 Rev. 2 Clear/Purge and ANSSI Palier 1/2 standards. |

---

## 🚀 Quick Start & Testing

### 1. Installation

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. End-to-End Demonstration Script

Run the automated demonstration script in mock mode:

```bash
python demo.py
```

This performs:
1. Mock disk sanitization run (NIST SP 800-88 / ANSSI P1).
2. Wipe Confidence Score calculation.
3. PDF certificate generation with embedded QR code & Blockchain Hash.
4. Certificate anchoring into local block-chain ledger (`trust/chain.json`).
5. Ledger integrity validation.
6. Verification API query against `http://localhost:8000/verify?hash=<block_hash>`.

---

## 🏛️ Verification Portal API

Run the verification service:

```bash
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

- **Web Portal:** Open `http://localhost:8000/` in your browser.
- **REST Endpoint:** `GET /verify?hash=<block_hash>` returns full block metadata and confidence score.

---

## 📱 Mobile Asset Agent (Android)

Sanitize connected Android assets or run in mock mode:

```bash
python android/agent.py --mock
```

---

## 🧪 Running Unit Tests

```bash
python -m unittest tests/test_confidence.py
python trust/blockchain.py
```

---

## 🗺️ Roadmap & Phase 2 Vision

- **Distributed Ledger Integration:** Swap local JSON hash-chain for Hyperledger Fabric / Polygon testnet anchor.
- **HPA/DCO Automatic Zeroing:** Extend `hdparm -N` to issue `hdparm -N p<max>` for automatic hidden sector unhiding & wiping.
- **Enterprise ERP Connector:** Webhooks for SAP / ServiceNow IT Asset Management (ITAM) lifecycle tracking.

---
