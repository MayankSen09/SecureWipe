# Product Requirement Document (v2.1 — Complete Platform Build Spec)
## Integrated Secure Data Erasure, Mobile Asset Sanitization & File Recovery Platform
**Context: SIH 2026 Internal Selection Round — PS 26149 (NTRO - National Technical Research Organisation)**
**Timeline: 24 hours build window**
**Audience: AI Coding Assistants, System Architects, Compliance Auditors, and Hackathon Evaluation Jury**

---

## 0. Executive Summary & Build Strategy

The problem statement (PS 26149) requires an enterprise-grade platform combining:
1. **Secure Drive & Media Eraser** (HDD, SSD, NVMe, USB drives)
2. **Mobile Asset Sanitization Agent** (Android smartphones & tablets via ADB/Fastboot)
3. **Secure File & Folder Selective Shredder** (with metadata stripping & journal awareness)
4. **Advanced File Carving & Recovery Engine** (with confidence scoring & auto-classification)
5. **Unified Audit, Verification & Ledger System** (Signed PDF certificates, QR validation, local SHA-256 blockchain, Ethereum/Polygon smart contract integration, and a FastAPI web verification portal)

### Architectural Open-Source Integration & Attribution Strategy
We evaluated existing open-source tools:
- **SecureWipe** (github.com/MayankSen09/SecureWipe, GPL v3): Provides standards-compliant drive sanitization (NIST SP 800-88 Rev.2, ANSSI Palier 1/2), low-level disk handle access (`\\.\PhysicalDriveX` / `/dev/sdX`), HPA/DCO hidden region unhiding, SSD/NVMe firmware erase triggers, BitLocker/LUKS crypto-shredding, and local blockchain ledger recording.
- **Scalpel** (github.com/sleuthkit/scalpel, Apache 2.0): Provides high-performance, file-system-agnostic signature carving.

**Decision & Transparency Standard:**
- We integrate **SecureWipe** as our core drive-erasure engine and **Scalpel** as our raw carving engine.
- We **explicitly credit both projects** in code, UI, generated certificates, and documentation.
- Our original engineering contribution focuses on:
  1. **Android Mobile Asset Sanitization Agent** (`android/agent.py`) for ADB/Fastboot UserData key destruction.
  2. **File & Folder Selective Eraser** (`core/wipe_engine.py` extension) with file-system metadata stripping & progress management.
  3. **Dual-Tier Audit Confidence Scoring Engine** (`core/confidence.py` for erasure 0–100% score + carving recovery confidence scoring).
  4. **Multi-Interface Web & Verification Portal** (`api/app.py` FastAPI service + `web/index.html` portal + Vercel deployment).
  5. **Blockchain Audit Ledger & Smart Contract Integration** (`trust/blockchain.py` SHA-256 hash-chain + `trust/SecureWipeLedger.sol`).
  6. **Unified Desktop GUI & Multi-Lingual Engine** (`gui/app.py` Tkinter wizard + `core/i18n.py` for EN/FR/HI).

---

## 1. Objectives & Key Capabilities

Deliver a production-ready, multi-platform prototype in 24 hours that:
- Executes standards-compliant drive sanitization (NIST SP 800-88 Clear/Purge/Crypto Erase, ANSSI Palier 1/2, IEEE 2883-2022).
- Sanitizes connected Android mobile assets via ADB & Fastboot commands (UserData key destruction & block wiping).
- Provides selective secure file & folder deletion with metadata scrubbing (EXIF, PDF, Office properties).
- Performs file signature carving with an original confidence-scoring matrix (High/Medium/Low) and automatic file classification.
- Computes weighted Audit Confidence Scores (0–100%) based on firmware triggers, sector verification, and hidden area clearance.
- Maintains an immutable SHA-256 local blockchain ledger with optional Polygon/Ethereum smart contract anchoring.
- Generates tamper-evident, multi-lingual PDF audit certificates containing scannable QR codes for offline and web-based verification.
- Hosts a web verification portal (`/verify`, `/download-pdf`) and REST API endpoints.
- Supports air-gapped / offline defense environments (NTRO requirement).

---

## 2. Platform Scope

### 2.1 In-Scope Capabilities
| Domain | Sub-System / Capability | Engine / Approach | Status |
|---|---|---|---|
| **Module 1: Drive Eraser** | HDD/SSD/NVMe/USB detection, HPA/DCO unhiding (`hdparm`), BitLocker/LUKS crypto-shredding, NIST SP 800-88 / ANSSI Palier 1/2 algorithms | SecureWipe core (`core/wipe_engine.py`, `core/disk_windows.py`, `core/disk_linux.py`) | Integrated backend |
| **Module 1B: Mobile Agent** | Android smartphone sanitization via ADB (`getprop`) & Fastboot (`fastboot -w` UserData key destruction) | Original `android/agent.py` | Original build |
| **Module 2: File/Folder Eraser** | Selective multi-pass overwrite (1-pass zero, 3-pass NIST, custom N-pass), metadata stripping (EXIF, PDF properties), batch isolation | Original extension in `core/wipe_engine.py` & `src/erase_files/` | Original build |
| **Module 3: Carving & Recovery** | Signature-based file recovery (JPEG, PDF, DOCX/ZIP, PNG), byte entropy calculation ($H \ge 7.5$), auto-classification | Scalpel CLI wrapper + original scoring layer (`src/recover/`) | Integrated + Original layer |
| **Audit & Confidence Engine** | Dual-tier scoring: Erasure score (Firmware 50pts + Verification 30pts + HPA 20pts) and Carving score (Header+Footer, Size Plausibility, Entropy) | Original `core/confidence.py` | Original build |
| **Trust Ledger & Verification** | SHA-256 Hash Chain (`trust/chain.json`), Ethereum/Polygon smart contract template (`trust/SecureWipeLedger.sol`), REST API endpoints (`/verify`, `/download-pdf`) | Original `trust/blockchain.py` & `api/app.py` | Original build |
| **User Interfaces** | Desktop Dark Wizard GUI (Tkinter), Interactive CLI (`rich`), Web Portal (`web/index.html`), Vercel Edge Deployment (`vercel.json`) | Original (`gui/app.py`, `securewipe.py`, `web/`) | Original build |
| **Internationalization** | Multi-lingual certificates & UI support (English, French, Hindi) | Original `core/i18n.py` & `i18n/*.json` | Original build |

### 2.2 Explicitly Out of Scope for 24h Prototype
- Apple iOS device wiping via idevicerestore (Android ADB/Fastboot is supported; iOS requires proprietary Apple host tools).
- Hardware RAID array deep-rebuilding or network-attached storage (NAS/SAN) over iSCSI/Fibre Channel.
- Fragmented file carving without headers/footers (demo relies on signature-bounded contiguous & semi-contiguous blocks).
- Enterprise Multi-Tenant Single Sign-On (SSO/SAML) — single operator / local admin role for prototype.

---

## 3. Environment & Technical Stack

| Layer | Technology | Purpose / Technical Function |
|---|---|---|
| **Primary OS** | Windows 10/11 & Linux (Ubuntu 22.04+ / WSL2) | Cross-platform runtime with direct disk handle access |
| **Core Runtime** | Python 3.9+ | Binary buffer manipulation, system calls, subprocess execution |
| **Windows Disk Layer** | `WMI`, `Win32 API`, `diskpart` | Direct physical drive handle opening (`\\.\PhysicalDriveX`) |
| **Linux Disk Layer** | `hdparm`, `lsblk`, `smartctl`, `dd` | Sector mapping, LBA boundary check, `hdparm -N` HPA/DCO unhiding |
| **Mobile Layer** | `ADB` & `Fastboot` CLI tools | Android device property discovery & UserData key destruction |
| **Carving Engine** | Scalpel 1.60+ | Low-level sector scanning using config signatures (`scalpel.conf`) |
| **Desktop GUI** | Tkinter / CustomTkinter | Multi-step dark-themed wizard interface (`gui/app.py`) |
| **Web & REST API** | FastAPI + Uvicorn + Vercel | REST verification service (`/verify`, `/download-pdf`, `/api/v1/health`) |
| **Web Frontend** | HTML5 / Vanilla CSS3 / JS | Dark-mode web verification portal (`web/index.html`) |
| **Certificate Engine** | FPDF2 + Pillow + QRCode | PDF audit certificate generation with embedded SHA-256 QR codes |
| **Trust Ledger** | Python `hashlib` + Solidity | Local SHA-256 hash-chain (`trust/chain.json`) + Smart Contract (`trust/SecureWipeLedger.sol`) |

---

## 4. Platform System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   USER INTERFACE LAYER                                       │
│   Desktop Wizard (Tkinter)  │  Web Portal (FastAPI/HTML5)  │  CLI (Rich)  │  Android Agent   │
└───────────┬───────────────────────────────┬────────────────────────┬──────────────┬─────────┘
            │                               │                        │              │
┌───────────▼───────────────────────────────▼────────────────────────▼──────────────▼─────────┐
│                                   ORCHESTRATION LAYER                                        │
│   Module 1: Drive Wiping   │  Module 1B: Mobile Agent  │ Module 2: File Shred  │ Module 3: Carve│
└───────────┬───────────────────────────────┬────────────────────────┬──────────────┬─────────┘
            │                               │                        │              │
┌───────────▼───────────────────────────────▼────────────────────────▼──────────────▼─────────┐
│                               CORE EXECUTION & HARDWARE LAYER                                │
│ Windows: WMI / Win32 Handles  │ Linux: hdparm / smartctl  │ ADB / Fastboot  │ Scalpel Carver │
└───────────┬───────────────────────────────┬────────────────────────┬──────────────┬─────────┘
            │                               │                        │              │
            └───────────────────────────────┼────────────────────────┘              │
                                            ▼                                       │
┌───────────────────────────────────────────────────────────────────────────────────▼─────────┐
│                               DUAL-TIER CONFIDENCE SCORING ENGINE                            │
│  Erasure Score: Firmware (50pts) + Sampling (30pts) + HPA/DCO (20pts) → Scale: 0–100%         │
│  Carving Score: Header/Footer Match + Plausible Size + Entropy Analysis → HIGH / MED / LOW   │
└───────────────────────────────────────────────────┬─────────────────────────────────────────┘
                                                    │
                                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                SHARED AUDIT & REPORTING PIPELINE                            │
│  Signed PDF Builder (FPDF2)  │  QR Code Engine  │  SHA-256 Local Hash Chain  │ Smart Contract │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Functional Requirements by Module

### 5.1 Module 1 — Secure Drive & Media Eraser (SecureWipe Integration)
- **Drive Discovery & Disambiguation:**
  - Enumerate all physical disks via WMI/Win32 (`disk_windows.py`) or `lsblk`/`smartctl` (`disk_linux.py`).
  - Retrieve model, serial number, transport type (NVMe, SATA, USB), size, and encryption state (BitLocker/LUKS/TCG Opal).
  - Automatically flag system/boot drive as `is_system = True` and **hard-block** wiping commands targeting system drives.
- **HPA/DCO Hidden Region Clearance:**
  - Execute `hdparm -N` on Linux targets to compare Native Max LBA against User Visible LBA.
  - Temporarily unhide hidden sectors before overwriting to ensure complete sector coverage (+20 pts to Audit Score).
- **Sanitization Standards & Algorithms:**
  - **NIST SP 800-88 Clear:** 1-pass zero-fill (`0x00`) across all LBAs from LBA 0 to Max LBA.
  - **ANSSI Palier 2:** 3-pass sequence (Pass 1: `0x00`, Pass 2: `0xFF`, Pass 3: Cryptographic random bytes via `os.urandom`).
  - **NIST SP 800-88 Purge / Crypto Erase:** Firmware-level ATA Secure Erase / NVMe Format trigger or Master Encryption Key (MEK) destruction for BitLocker/LUKS/SED drives.
- **Verification Sampling:**
  - Read back 10% random sector samples across head, middle, and tail LBAs to verify zeroed state (`0x00`).
- **Erasure Audit Confidence Score Engine (`core/confidence.py`):**
  $$\text{Score} = \text{Firmware/Crypto Erase (50pts)} + \text{Verification Sampling (30pts)} + \text{HPA Clearance (20pts)}$$
  - Categorize as **HIGH** ($\ge 90\%$), **MEDIUM** ($\ge 70\%$), or **LOW** ($< 70\%$).

### 5.2 Module 1B — Android Mobile Asset Sanitization Agent (`android/agent.py`)
- **Device Detection:**
  - Query ADB interface for connected Android hardware (`adb devices`).
  - Extract properties: `ro.product.model`, `ro.serialno`, `ro.build.version.release`, storage capacity.
- **Mobile Wipe Execution:**
  - Trigger device reboot into fastboot bootloader (`adb reboot bootloader`).
  - Issue `fastboot -w` command to trigger hardware UserData partition purge and cryptographic encryption key destruction.
- **Mock Demonstration Mode:**
  - Support `--mock` flag to simulate full Android sanitization workflow for demonstration without physical mobile hardware.

### 5.3 Module 2 — Secure File & Folder Eraser
- **Target Selection & Enumeration:**
  - Accept individual file paths, multi-file selections, or recursive directory paths.
- **Multi-Pass Overwrite & Shredding:**
  - Overwrite raw file data using specified algorithms (1-pass zeroing, 3-pass NIST, or custom N-pass).
  - Truncate file length to 0 bytes before unlinking from the file system index.
- **Metadata Scrubbing:**
  - Strip image EXIF metadata (GPS coordinates, camera details) using Pillow/ExifTool prior to deletion.
  - Strip document properties (author, revision history) for PDF and Office files.
- **File System Journaling Mitigation:**
  - Log warning regarding file system journal remnants (e.g. ext4 journal, NTFS `$LogFile`).
  - Provide an optional **Free Space Zeroing** command to sanitize unallocated drive space.
- **Fault-Tolerant Batch Processing:**
  - Continue batch execution if individual files fail (e.g. permission locked); log per-file status (`SUCCESS`, `FAILED`, `ACCESS_DENIED`).

### 5.4 Module 3 — Advanced File Carving & Recovery (Scalpel Wrapper + Scoring)
- **Carving Target:** Accept raw block devices (`/dev/sdb`), physical disk handles (`\\.\PhysicalDrive1`), or disk image files (`.img`, `.dd`).
- **Engine Execution:** Invoke Scalpel via subprocess with configured file signatures (JPEG, PDF, DOCX/ZIP, PNG).
- **Shannon Entropy Analysis:**
  - Compute byte entropy $H = -\sum p_i \log_2 p_i$ for recovered fragments. High entropy ($H \ge 7.5$) indicates compressed/encrypted content.
- **Confidence Scoring Matrix:**
  - **HIGH Confidence ($\ge 90\%$):** Valid Header AND Footer found, entropy within valid signature range, size matches plausible profile.
  - **MEDIUM Confidence ($\ge 70\%$):** Valid Header found, size within plausible range, footer missing or truncated.
  - **LOW Confidence ($< 70\%$):** Header found but recovered size exceeds maximum plausible file size or contains corrupt byte structure.
- **Auto-Classification:** Automatically organize recovered candidates into categories: `Images/`, `Documents/`, `Archives/`.
- **Post-Wipe Verification Workflow:** Re-run carving on media after Module 1/1B wiping to demonstrate **0 recoverable files** (proof of destruction).

### 5.5 Module 4 — Trust Ledger & Web Verification System
- **Local SHA-256 Hash Chain (`trust/blockchain.py`):**
  - Append each operation to `trust/chain.json`.
  - Block Hash formula:
    $$\text{Block Hash} = \text{SHA256}(\text{PrevHash} + \text{CertPDFHash} + \text{Timestamp} + \text{Serial} + \text{ConfidenceScore})$$
- **Smart Contract Integration (`trust/SecureWipeLedger.sol`):**
  - Ethereum/Polygon Solidity smart contract template for on-chain audit log anchoring.
- **PDF Certificate Generator (`cert/generator.py`):**
  - Generate cryptographically signed PDF certificates containing operator info, hardware serials, wiping method, confidence score, and embedded QR code.
  - Multi-lingual rendering (English, French, Hindi) via `core/i18n.py`.
- **FastAPI Verification Server (`api/app.py` & `web/index.html`):**
  - `GET /verify?hash=<block_hash>`: Validate certificate authenticity against ledger.
  - `GET /download-pdf?hash=<block_hash>`: Serve stored audit PDF.
  - Hosted deployment capability via Vercel (`vercel.json`, `app.py`).

---

## 6. Shared Data Schemas & API Endpoints

### 6.1 Shared Operation Log Data Model (`OperationLogEntry`)
```python
OperationLogEntry = {
    "operation_id": str,          # UUIDv4
    "module": str,                # "erase_drive" | "erase_mobile" | "erase_file" | "recover"
    "timestamp": str,             # ISO 8601 UTC timestamp
    "operator_name": str,         # Operator identifier
    "target_identifier": str,     # Serial number, device path, or target directory
    "target_model": str,          # Drive/Phone model or File count
    "method_applied": str,        # e.g., "NIST SP 800-88 Purge", "ANSSI 3-Pass", "Scalpel Carve"
    "execution_engine": str,      # "SecureWipe Core", "Android Agent", "Scalpel Engine"
    "status": str,                # "SUCCESS" | "PARTIAL" | "FAILED"
    "confidence_score": int,      # 0 to 100
    "confidence_rating": str,     # "HIGH" | "MEDIUM" | "LOW"
    "details": {
        "bytes_processed": int,
        "passes_completed": int,
        "hpa_detected": bool,
        "hpa_wiped": bool,
        "files_recovered": int,   # Module 3 specific
        "confidence_breakdown": dict
    },
    "cert_pdf_sha256": str,       # SHA-256 hash of output PDF
    "block_hash": str,            # Blockchain hash anchor
    "locale": str                 # "en" | "fr" | "hi"
}
```

### 6.2 OpenAPI REST Endpoints Schema
| Endpoint | Method | Input Parameters | Output Response |
|---|---|---|---|
| `/api/v1/health` | `GET` | None | `{"status": "ok", "version": "2.1.0"}` |
| `/verify` | `GET` | `hash: str` | Ledger verification record JSON (`valid`, `timestamp`, `serial`, `score`) |
| `/download-pdf` | `GET` | `hash: str` | PDF binary file stream |
| `/api/v1/erase` | `POST` | Target device JSON payload | Job ID & real-time progress WebSocket stream |
| `/api/v1/carve` | `POST` | Disk image path & signature config | Carving summary JSON with confidence scores |

---

## 7. Repository Structure

```
SecureWipe/
├── api/
│   ├── app.py                # FastAPI REST API — verification & PDF download engine
│   └── index.py              # Serverless entrypoint
├── core/
│   ├── wipe_engine.py        # Multi-standard sanitization & zeroing engine
│   ├── confidence.py         # 0–100 Audit confidence score calculator
│   ├── disk_windows.py       # Windows WMI & Diskpart drive enumeration
│   ├── disk_linux.py         # Linux drive detection & hdparm HPA/DCO analyzer
│   ├── crypto_detect.py      # BitLocker & TCG Opal SED encryption scanner
│   ├── ui.py                 # CLI formatted UI output
│   └── i18n.py               # Internationalization engine (EN / FR / HI)
├── cert/
│   ├── generator.py          # PDF certificate builder with embedded QR code
│   └── template/             # Certificate visual assets and logos
├── trust/
│   ├── blockchain.py         # Local SHA-256 blockchain ledger engine
│   ├── chain.json            # Persistent blockchain ledger store
│   └── SecureWipeLedger.sol  # Polygon/Ethereum smart contract template
├── gui/
│   ├── app.py                # Tkinter dark-themed multi-tab wizard GUI
│   ├── theme.py              # Palette and style tokens
│   ├── steps/                # Wizard workflow screens
│   └── widgets/              # Reusable UI widgets
├── android/
│   └── agent.py              # Android ADB & Fastboot mobile sanitization agent
├── web/
│   └── index.html            # Web verification portal UI
├── i18n/
│   └── en.json               # Language translation key dictionary
├── tests/
│   └── test_confidence.py    # Unit tests for confidence scoring engine
├── securewipe.py             # Main CLI & GUI entrypoint launcher
├── demo.py                   # Automated end-to-end demonstration pipeline
├── install.ps1 / install.sh  # Automated setup scripts
├── vercel.json               # Vercel deployment configuration
└── PRD_Integrated_Erasure_Recovery_Platform_v2.md # Build Specification
```

---

## 8. Safety Architecture, Air-Gapped Operation & Edge Cases

### 8.1 Safety Architecture & System Protection
- **Drive Lock Safeguard:** Devices flagged with `is_system = True` (containing active OS/Python runtime) are strictly excluded from selection.
- **Double Confirmation Step:** GUI requires explicit text verification (typing target drive label) before initiating destructive operations.
- **Dry-Run Mode (`--mock`):** All modules support `--mock` execution for safe judging demonstrations without altering physical disks.

### 8.2 Air-Gapped Defense Operation (NTRO Requirement)
- **Zero External Dependencies at Runtime:** Core wiping, carving, PDF rendering, and QR generation execute 100% offline.
- **Offline QR Verification:** Embedded QR codes contain full cryptographic payload (`SHA-256(Cert + Serial + Timestamp)`) readable by any offline scanner without internet connectivity.

### 8.3 Failure Handling Matrix
| Edge Case | Failure Mode | Mitigation / System Action |
|---|---|---|
| System drive targeted | Operator error | Hard-blocked by `disk_windows.py`/`disk_linux.py` system check |
| HPA unhiding fails | Drive firmware locked | Log warning, proceed with standard LBA zeroing, deduct 20pts from score |
| ADB disconnects mid-wipe | USB cable pulled | Log `status: PARTIAL`, require fastboot reconnect |
| Scalpel not installed | Missing binary | System startup check fails loudly with installation instructions |
| Locked/In-use file | File lock | Skip locked file, log `FAILED (ACCESS_DENIED)`, complete remaining batch |

---

## 9. Definition of Done & Success Criteria

- [x] Multi-standard drive erasure (NIST SP 800-88 / ANSSI) produces verified zeroed sectors and signed PDF certificate.
- [x] Android Mobile Agent (`android/agent.py`) executes property discovery and fastboot purge in live/mock modes.
- [x] Selective file/folder eraser overwrites data passes and scrubs EXIF/document metadata.
- [x] Scalpel carving engine recovers files from test image, assigns High/Med/Low confidence scores, and auto-classifies results.
- [x] Post-wipe carving verification confirms **0 recoverable files** on sanitized media.
- [x] Audit Confidence Scoring engine computes accurate 0–100% scores based on firmware, sampling, and HPA factors.
- [x] SHA-256 local blockchain ledger appends block records and verifies chain integrity (`trust/blockchain.py`).
- [x] FastAPI web server serves `/verify` hash lookup and `/download-pdf` certificate stream.
- [x] Desktop GUI runs seamlessly in dark theme without terminal commands required.
- [x] Multi-lingual PDF certificates render accurately in English, French, and Hindi.

---

## 10. Demonstration Workflow (5-Minute Hackathon Demo Script)

1. **(30s) Drive Erasure & HPA Clearance:** Launch Desktop GUI -> Select target USB drive -> Execute NIST SP 800-88 Purge -> View live sector zeroing & 100% confidence score.
2. **(60s) Android Mobile Sanitization:** Trigger `android/agent.py --mock` -> Demonstrate ADB property scan & Fastboot UserData key destruction -> View generated Mobile Audit Cert.
3. **(90s) File Carving & Confidence Scoring:** Run Module 3 Carving against pre-formatted disk image -> Show recovered files categorized into Images/Docs with color-coded High/Med/Low confidence badges.
4. **(60s) Post-Wipe Verification Proof:** Execute carving against the sanitized USB drive from Step 1 -> Display **0 files recovered** (conclusive proof of destruction).
5. **(60s) Web Verification & Blockchain Ledger:** Open Web Verification Portal (`/verify`) -> Scan PDF QR code -> Query ledger SHA-256 hash -> Download verifiable audit certificate.
