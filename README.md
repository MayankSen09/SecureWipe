# 🛡️ TrustWipe — SecureWipe Platform

<div align="center">

[![Live Demo](https://img.shields.io/badge/🌐%20Live%20Demo-secure--wipe--eta.vercel.app-6366f1?style=for-the-badge&logo=vercel&logoColor=white)](https://secure-wipe-eta.vercel.app/)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-22c55e?style=for-the-badge)](LICENSE)
[![NIST SP 800-88](https://img.shields.io/badge/Standard-NIST%20SP%20800--88-f97316?style=for-the-badge)](https://csrc.nist.gov/)
[![ANSSI Certified](https://img.shields.io/badge/Standard-ANSSI%20Palier%201%2F2-ef4444?style=for-the-badge)](https://www.ssi.gouv.fr/)
[![Blockchain Anchored](https://img.shields.io/badge/Ledger-SHA--256%20Blockchain-a855f7?style=for-the-badge)](trust/chain.json)

**A professional-grade, auditable data sanitization platform for secure IT asset disposal and circular economy compliance.**

[**🚀 Try the Live Demo →**](https://secure-wipe-eta.vercel.app/)

</div>

---

## 📋 Table of Contents

- [What is TrustWipe?](#-what-is-trustwipe)
- [Key Features](#-key-features)
- [Live Demo](#-live-demo)
- [Technology Stack](#️-technology-stack)
- [Quick Start](#-quick-start)
- [How to Run](#-how-to-run)
- [Project Architecture](#-project-architecture)
- [Sanitization Modes](#-sanitization-modes)
- [Compliance Standards](#-compliance--standards)
- [Testing](#-testing--verification)
- [License](#-license)

---

## 🔍 What is TrustWipe?

When you delete a file or format a disk, the operating system **only removes the pointer** to the data — the actual bytes remain physically on disk and are recoverable with free tools like Recuva or TestDisk in minutes.

**TrustWipe (SecureWipe)** solves this by overwriting every sector with industry-standard algorithms, then producing a **cryptographically signed PDF audit certificate** anchored to a local SHA-256 blockchain ledger — providing undeniable, tamper-proof proof of destruction for GDPR, ANSSI, and NIST compliance.

> Built for IT asset managers, refurbishers, data centers, and organizations with regulatory data disposal obligations.

---

## 💡 Key Features

| Feature | Description |
|:--------|:------------|
| 🧹 **Multi-Standard Erasure** | NIST SP 800-88 (Clear / Purge / Crypto Erase) & ANSSI Palier 1/2 multi-pass algorithms |
| 🔍 **Hidden Region Detection** | `hdparm` analysis to sanitize Host Protected Areas (HPA) & Device Configuration Overlays (DCO) |
| 📊 **Audit Confidence Score** | Automated 0–100 score: firmware erase (50 pts) + sector verification (30 pts) + hidden area clearance (20 pts) |
| 🔗 **Blockchain Anchoring** | Immutable SHA-256 local blockchain ledger for tamper-proof certificate validation |
| 📄 **Signed PDF Certificates** | Auto-generated audit certificates with embedded offline-scannable SHA-256 QR codes |
| 📱 **Android Wipe Agent** | Mobile asset sanitization via ADB & Fastboot for Android device disposal |
| 🌐 **Web Verification Portal** | Public certificate verification portal — no account required |
| 🖥️ **Desktop GUI + CLI** | Dark-themed Tkinter wizard GUI and interactive terminal interface |

---

## 🌐 Live Demo

> **Try TrustWipe instantly — no installation required.**

🔗 **[https://secure-wipe-eta.vercel.app/](https://secure-wipe-eta.vercel.app/)**

The web portal lets you:
- Verify any existing certificate by entering its SHA-256 hash
- Explore the blockchain ledger for audit records
- Download signed PDF certificates for verified wipe operations
- Understand the sanitization standards applied to each device

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|:------|:-----------|:--------|
| **Language** | Python 3.9+ | Core engine — device detection, zeroing, confidence scoring |
| **Backend API** | FastAPI + Uvicorn | REST endpoints for hash verification, PDF downloads & web suite |
| **Desktop GUI** | Tkinter + CustomTkinter | Cross-platform dark-themed operator wizard |
| **Web Frontend** | HTML5 / Vanilla CSS / JS | High-performance verification portal & audit UI |
| **Certificate Engine** | FPDF2 + QRCode | Signed PDF generator with embedded QR codes |
| **Trust Ledger** | SHA-256 Hash-Chain + Solidity | Immutable local blockchain + Ethereum smart contract template |
| **CLI Interface** | Rich + Argparse | Terminal formatting, progress bars & prompt handlers |
| **Mobile Agent** | ADB + Fastboot | Android device sanitization pipeline |
| **Deployment** | Vercel | Edge-deployed web portal & API |

---

## ⚡ Quick Start

### Prerequisites

- Python 3.9 or higher
- Git

### Installation

```powershell
# 1. Clone the repository
git clone https://github.com/MayankSen09/SecureWipe.git
cd SecureWipe

# 2. Create & activate a virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows PowerShell
# source venv/bin/activate     # Linux / macOS

# 3. Install dependencies
pip install -r requirements.txt
```

### Verify Installation (30-second demo)

```powershell
.\venv\Scripts\python.exe demo.py
```

This runs a full automated pipeline: device detection → sanitization → confidence scoring → PDF generation → blockchain anchoring — all in mock/safe mode.

---

## 🚀 How to Run

### Option A — Automated Demo Pipeline

Runs the complete end-to-end workflow in safe mock mode:

```powershell
.\venv\Scripts\python.exe demo.py
```

### Option B — Desktop GUI (Recommended for operators)

Dark-themed wizard with drive selector and live wipe progress:

```powershell
.\venv\Scripts\python.exe securewipe.py --gui --mock
```

### Option C — Command-Line Interface (CLI)

Interactive sanitization directly in your terminal:

```powershell
.\venv\Scripts\python.exe securewipe.py --cli --mock
```

### Option D — Web Suite & Verification Portal

Start the FastAPI server and access the certificate verification portal:

```powershell
.\venv\Scripts\python.exe -m uvicorn api.app:app --host 0.0.0.0 --port 8000
```

| Endpoint | Description |
|:---------|:------------|
| `http://localhost:8000` | Web verification portal |
| `GET /api/v1/health` | Service health check |
| `GET /verify?hash=<hash>` | Verify a certificate by SHA-256 |
| `GET /download-pdf?hash=<hash>` | Download signed PDF certificate |

> **Or use the live hosted version:** [https://secure-wipe-eta.vercel.app/](https://secure-wipe-eta.vercel.app/)

### Option E — Android Smartphone Wipe Agent

Sanitize connected Android devices via ADB/Fastboot:

```powershell
.\venv\Scripts\python.exe android/agent.py --mock
```

---

## 📂 Project Architecture

```
TrustWipe/
├── api/
│   └── app.py                # FastAPI REST API — verification & PDF download engine
├── core/
│   ├── wipe_engine.py        # Multi-standard sanitization & zeroing engine
│   ├── confidence.py         # 0–100 Audit confidence score calculator
│   ├── disk_windows.py       # Windows WMI & Diskpart drive enumeration
│   ├── disk_linux.py         # Linux drive detection & hdparm HPA/DCO analyzer
│   ├── crypto_detect.py      # BitLocker & TCG Opal SED encryption scanner
│   └── i18n.py               # Internationalization (EN / FR / HI)
├── cert/
│   ├── generator.py          # PDF certificate builder with embedded QR code
│   └── template/             # Certificate logos and visual assets
├── trust/
│   ├── blockchain.py         # Local SHA-256 blockchain ledger engine
│   ├── chain.json            # Persistent blockchain ledger store
│   └── SecureWipeLedger.sol  # Polygon/Ethereum smart contract template
├── gui/
│   ├── app.py                # Tkinter wizard GUI
│   ├── theme.py              # Dark palette & custom styling
│   ├── steps/                # Multi-step wizard screens
│   └── widgets/              # Reusable UI components
├── android/
│   └── agent.py              # Android ADB/Fastboot wiping agent
├── web/
│   └── index.html            # Web portal & certificate verification UI
├── tests/
│   └── test_confidence.py    # Confidence engine unit tests
├── securewipe.py             # Main CLI & GUI launcher entrypoint
├── demo.py                   # Automated pipeline demo script
├── app.py                    # Vercel deployment entrypoint
├── vercel.json               # Vercel routing configuration
└── requirements.txt          # Python dependencies
```

---

## 🔐 Sanitization Modes

TrustWipe supports 5 industry-standard sanitization modes, selectable based on your security requirements:

| Mode | Method | Covers Hidden Zones | Speed | Best For |
|:-----|:-------|:------------------:|:-----:|:---------|
| **ANSSI Level 1** | 1× Zero-overwrite pass | ❌ | ⚡ Fast | Internal organizational transfers |
| **ANSSI Level 2 / NIST Clear** | 1× Cryptographically random pass | ❌ | ⚡ Fast | External transfers, hardware resale |
| **NIST Purge** | ATA Secure Erase / NVMe Format (firmware-level) | ✅ **Yes** | ⏱ Variable | Sensitive data, SSDs, NVMe drives |
| **Crypto Erase** | AES encryption key destruction | ✅ **Yes** | ⚡ Instant | Any LUKS / BitLocker / SED encrypted disk |
| **Custom N-Pass** | 2–7 alternating zero/random passes | ❌ | 🐢 Slow | Documentary compliance requirements |

> 💡 **For SSDs and NVMe drives, always use NIST Purge or Crypto Erase.** Wear-leveling means standard overwrite cannot reach all physical cells — only firmware-level commands guarantee complete erasure.

---

## 📜 Compliance & Standards

TrustWipe's certificates are recognized under the following regulatory frameworks:

| Standard | Description |
|:---------|:------------|
| **NIST SP 800-88 Rev. 2** | NIST Guidelines for Media Sanitization — Clear, Purge & Crypto Erase |
| **ANSSI Palier 1 / Palier 2** | French National Cybersecurity Agency — 1-pass & 3-pass zeroing rules |
| **IEEE 2883-2022** | IEEE Standard for Sanitizing Storage |
| **DoD 5220.22-M** | National Industrial Security Program Operating Manual |
| **GDPR Art. 5(1)(f)** | Data integrity & confidentiality in storage disposal |

---

## 🧪 Testing & Verification

```powershell
# Run the full unit test suite
.\venv\Scripts\python.exe -m unittest discover tests

# Verify blockchain ledger chain integrity
.\venv\Scripts\python.exe trust/blockchain.py
```

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

Distributed under the **GNU GPL v3 License**. See [`LICENSE`](LICENSE) for full details.

---

<div align="center">

Made with ❤️ for secure, compliant, and sustainable IT asset disposal.

**[🌐 Live Demo](https://secure-wipe-eta.vercel.app/) · [📖 Technical Docs](TECHNICAL.md) · [🔄 Technical Flow](TECHNICAL_FLOW.md)**

</div>
