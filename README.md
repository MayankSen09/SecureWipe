# SecureWipe

SecureWipe is an open-source, enterprise-grade data sanitization and audit verification engine. It enforces **NIST SP 800-88 Rev. 2** (Clear/Purge) and **ANSSI Palier 1/2** standards across storage media (NVMe, SSDs, HDDs, USBs, and Android devices) with tamper-proof blockchain anchoring and downloadable signed PDF audit certificates.

---

## ⚡ Quick Start

### 1. Setup & Installation

```powershell
# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate       # Windows PowerShell
# source venv/bin/activate    # Linux / macOS

# Install dependencies
pip install -r requirements.txt
```

---

## 🛠️ Usage Modes

### 1. Interactive Desktop GUI Wizard
Launch the desktop application with step-by-step wizard, disk selection, and real-time wiping progress:

```powershell
python securewipe.py --gui --mock
```

### 2. Terminal CLI Tool
Run sanitization directly from your terminal (includes `--mock` mode for safe dry runs):

```powershell
python securewipe.py --cli --mock
```

### 3. Web Suite & Verification Portal
Start the FastAPI verification server and web interface:

```powershell
python -m uvicorn api.app:app --host 0.0.0.0 --port 8000
```

- **Web Dashboard:** Open `http://localhost:8000` in your browser.
- **Verification Endpoint:** `GET /verify?hash=<block_hash>`
- **PDF Download:** `GET /download-pdf?hash=<block_hash>`

### 4. End-to-End Automated Demo
Run the complete pipeline demonstration (disk detection -> wipe -> confidence score -> PDF generator -> blockchain ledger -> API check):

```powershell
python demo.py
```

### 5. Android Mobile Asset Agent
Sanitize connected mobile assets via ADB/Fastboot or run in mock mode:

```powershell
python android/agent.py --mock
```

---

## 🏛️ Architecture & Project Structure

```text
SecureWipe/
├── api/
│   └── app.py              # FastAPI verification service & PDF download engine
├── core/
│   ├── wipe_engine.py      # NIST SP 800-88 & ANSSI multi-pass zeroing engine
│   ├── confidence.py       # 0–100 Audit confidence scoring calculator
│   ├── disk_windows.py     # Windows storage drive enumeration (WMI / Diskpart)
│   ├── disk_linux.py       # Linux drive enumeration & HPA/DCO hidden sector detection
│   └── crypto_detect.py    # BitLocker / TCG Opal SED self-encryption detection
├── cert/
│   └── generator.py        # PDF certificate builder with embedded SHA-256 QR code
├── trust/
│   ├── blockchain.py       # SHA-256 block-chain hash ledger engine
│   ├── chain.json          # Persistent local blockchain ledger store
│   └── SecureWipeLedger.sol# Polygon / Ethereum smart contract interface
├── gui/
│   ├── app.py              # Tkinter desktop application wizard
│   └── theme.py            # Dark UI theme styling rules
├── android/
│   └── agent.py            # Android ADB/Fastboot asset wiping agent
├── web/
│   └── index.html          # Web portal & certificate verification interface
├── tests/
│   └── test_confidence.py  # Confidence engine unit tests
├── securewipe.py           # Main CLI entrypoint
├── demo.py                 # Automated end-to-end demonstration script
└── requirements.txt        # Core project dependencies
```

---

## 🧪 Testing & Verification

Run unit tests and verify local blockchain ledger integrity:

```powershell
# Run confidence engine unit tests
python -m unittest tests/test_confidence.py

# Verify blockchain ledger chain integrity
python trust/blockchain.py
```

---

## 📜 License & Compliance

- **License:** GPL v3
- **Compliance:** NIST SP 800-88 Rev. 2 (Clear/Purge), ANSSI Palier 1/2, IEEE 2883-2022, DoD 5220.22-M

