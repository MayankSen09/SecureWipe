# 🛡️ SecureWipe

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg)](LICENSE)
[![Standards: NIST SP 800-88](https://img.shields.io/badge/Standards-NIST%20800--88%20%7C%20ANSSI-orange.svg)](https://csrc.nist.gov/)
[![Blockchain Verified](https://img.shields.io/badge/Ledger-SHA256%20Anchored-purple.svg)](trust/chain.json)

**SecureWipe** is a secure data sanitization and audit verification platform built for trustworthy IT asset disposal and circular economy recycling.

It implements **NIST SP 800-88 Rev. 2** (Clear/Purge) and **ANSSI Palier 1/2** standards across storage media (NVMe, SSDs, HDDs, USBs, and Android smartphones), featuring automated confidence scoring, local blockchain ledger anchoring, and downloadable signed PDF audit certificates.

---

## 💡 Key Features

- 🧹 **Multi-Standard Erasure Engine:** Full support for NIST SP 800-88 (Purge/Clear/Crypto Erase) & ANSSI Palier 1/2 multi-pass zeroing algorithms.
- 🔍 **Hidden Region Sanitization:** `hdparm` sector analysis for unhiding & sanitizing hidden Host Protected Areas (HPA) & Device Configuration Overlay (DCO).
- 📊 **Audit Confidence Engine:** Calculates a 0–100 audit score based on firmware erase success (50 pts), random sector verification (30 pts), and hidden area clearance (20 pts).
- 🔗 **Blockchain Anchoring:** Immutable SHA-256 local block-chain ledger ensuring tamper-proof certificate validation (`trust/chain.json`).
- 📄 **PDF & QR Verification:** Automated signed PDF audit certificate generator with embedded offline-scannable SHA-256 QR codes.
- 📱 **Cross-Platform Mobile Support:** Mobile asset sanitization agent for Android devices via ADB & Fastboot.

---

## ⚡ Quick Start

### 1. Installation

Clone the repository and set up your virtual environment:

```powershell
# Clone the repository
git clone https://github.com/MayankSen09/SecureWipe.git
cd SecureWipe

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate       # Windows PowerShell
# source venv/bin/activate    # Linux / macOS

# Install required packages
pip install -r requirements.txt
```

---

## 🚀 How to Run

### Option A: Interactive Desktop Application (GUI)
Launch the dark-themed desktop wizard with drive selector and live wiping progress:

```powershell
python securewipe.py --gui --mock
```

### Option B: Fast Command-Line Tool (CLI)
Run interactive sanitization directly in your terminal:

```powershell
python securewipe.py --cli --mock
```

### Option C: Web Suite & Verification Portal
Start the FastAPI server to access the live web verification portal:

```powershell
python -m uvicorn api.app:app --host 0.0.0.0 --port 8000
```
- 🌐 **Web Portal:** Open [http://localhost:8000](http://localhost:8000) in your browser.
- 🔍 **Verification API:** `GET /verify?hash=<block_hash>`
- 📄 **PDF Certificate Endpoint:** `GET /download-pdf?hash=<block_hash>`

### Option D: End-to-End Automated Pipeline Demo
Run the complete automated workflow (detection → zeroing → confidence calculation → PDF render → ledger anchor):

```powershell
python demo.py
```

### Option E: Android Smartphone Wipe Agent
Sanitize connected mobile assets via ADB/Fastboot or test in mock mode:

```powershell
python android/agent.py --mock
```

---

## 📂 Project Architecture

```text
SecureWipe/
├── api/
│   └── app.py              # FastAPI REST verification & PDF download engine
├── core/
│   ├── wipe_engine.py      # Multi-standard sanitization & zeroing engine
│   ├── confidence.py       # 0–100 Audit confidence score engine
│   ├── disk_windows.py     # Windows WMI & Diskpart drive enumeration
│   ├── disk_linux.py       # Linux drive detection & hdparm HPA/DCO analyzer
│   ├── crypto_detect.py    # BitLocker & TCG Opal SED encryption scanner
│   └── i18n.py             # Internationalization support (EN / FR / HI)
├── cert/
│   ├── generator.py        # PDF certificate builder with embedded QR code
│   └── template/           # Certificate logos and visual assets
├── trust/
│   ├── blockchain.py       # Local SHA-256 block-chain ledger engine
│   ├── chain.json          # Persistent block-chain ledger store
│   └── SecureWipeLedger.sol# Polygon/Ethereum smart contract template
├── gui/
│   ├── app.py              # Tkinter wizard GUI interface
│   ├── theme.py            # Custom styling & dark palette
│   ├── steps/              # Multi-step wizard screens
│   └── widgets/            # Reusable UI widgets
├── android/
│   └── agent.py            # Android ADB/Fastboot wiping agent
├── web/
│   └── index.html          # Web portal & certificate verification UI
├── tests/
│   └── test_confidence.py  # Confidence engine unit tests
├── securewipe.py           # Main CLI & GUI launcher entrypoint
├── demo.py                 # Automated pipeline demonstration script
└── requirements.txt        # Python dependencies
```

---

## 🧪 Testing & Verification

Ensure system integrity by running unit tests and checking the blockchain chain:

```powershell
# Run confidence engine unit tests
python -m unittest tests/test_confidence.py

# Verify blockchain ledger chain integrity
python trust/blockchain.py
```

---

## 📜 Compliance & Standards

- **NIST SP 800-88 Rev. 2:** Clear, Purge, & Cryptographic Erase
- **ANSSI Palier 1 / Palier 2:** 1-pass & 3-pass zeroing rules
- **IEEE 2883-2022:** Standard for Sanitizing Storage
- **DoD 5220.22-M:** National Industrial Security Program Operating Manual

---

## 📄 License

Distributed under the **GPL v3 License**. See `LICENSE` for more information.


