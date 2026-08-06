# 🛡️ SecureWipe — System Architecture & Technical Flow Documentation

## 📌 Executive Overview

**SecureWipe** is an enterprise-grade data sanitization and audit verification platform designed for trustworthy IT asset disposal and circular economy recycling. It enforces strict compliance with **NIST SP 800-88 Rev. 2** (Clear/Purge/Crypto Erase) and **ANSSI Palier 1/2** standards across storage media (NVMe, SSDs, HDDs, USB drives, and Android mobile assets).

This document details the exact technical flow, technology stack, target scoping rules, and sector-by-sector data destruction process.

---

## 🧬 1. Technology Stack

| Layer | Technology | Technical Function |
| :--- | :--- | :--- |
| **Engine Language** | `Python 3.9+` | Core execution runtime, low-level binary buffer manipulation, and system calls |
| **Windows Storage Layer** | `WMI`, `Win32 API`, `diskpart` | Direct physical drive handle opening (`\\.\PhysicalDriveX`) and partition queries |
| **Linux Storage Layer** | `hdparm`, `lsblk`, `smartctl`, `dd` | Sector mapping, LBA boundary calculation, and `hdparm -N` HPA/DCO manipulation |
| **Mobile Asset Agent** | `ADB` & `Fastboot` | Recovery trigger, partition zeroing (`/dev/block/...`), and UserData key destruction |
| **Audit Scoring Engine** | `core/confidence.py` | Weighted confidence score algorithm (Firmware 50pts + Verification 30pts + HPA 20pts) |
| **Certificate Generator** | `FPDF2`, `Pillow`, `qrcode` | PDF audit certificate builder with embedded scannable SHA-256 QR codes |
| **Trust Ledger** | `SHA-256 Hash Chain`, `Solidity` | Local block-chain ledger (`trust/chain.json`) and Polygon/Ethereum smart contract |
| **Web Service & REST API** | `FastAPI`, `Uvicorn`, `HTML5/CSS3` | Async API service (`/verify`, `/download-pdf`) and responsive dark UI portal |

---

## 🛑 2. Safety Architecture: Why SecureWipe Does Not Wipe Itself

A common question in storage software engineering is: **"Why doesn't the wiping software delete itself during execution?"**

SecureWipe resolves this using strict operating system abstraction and target scoping rules:

### A. Target Disambiguation (Drive Scoping)
1. During disk discovery (`core/disk_windows.py` or `core/disk_linux.py`), SecureWipe queries physical drive mountpoints and system flags.
2. The drive containing the active Operating System, Python runtime, and SecureWipe codebase (e.g. `C:\` or `/dev/nvme0n1p2`) is automatically flagged as `is_system = True`.
3. SecureWipe explicitly **blocks** any sanitization command targeted at `is_system = True` drives in standard operational mode.

### B. Secondary Target Execution
- SecureWipe executes wiping commands strictly on **secondary target physical drives** (e.g., `PhysicalDrive1`, attached external SSDs/HDDs, or USB drives).
- The Python process, buffer memory, and certificate generator remain executing safely on the host system while raw binary pattern buffers are written to the target disk handles.

---

## 🔬 3. Step-by-Step Data Destruction Flow

When a wipe operation is triggered, SecureWipe executes a 5-phase sequential pipeline:

```
[Phase 1: Target Inspection]
            │
            ▼
[Phase 2: HPA/DCO Unhiding]
            │
            ▼
[Phase 3: Sector Zeroing / Crypto Shred]
            │
            ▼
[Phase 4: Sector Verification & Scoring]
            │
            ▼
[Phase 5: Cert Render & Blockchain Anchor]
```

### Phase 1: Target Inspection & Cryptographic Scan (`core/crypto_detect.py`)
- Reads drive geometry (LBA count, sector size: 512-byte vs 4Kn).
- Scans partition headers (GPT/MBR) and volume encryption signatures (BitLocker, LUKS, or TCG Opal Self-Encrypting Drives).

### Phase 2: Hidden Area Detection & Boundary Unhiding (`core/disk_linux.py`)
- Standard OS formatting ignores hidden disk boundaries (HPA — Host Protected Area & DCO — Device Configuration Overlay).
- SecureWipe issues `hdparm -N` commands to compare **Native Max LBA** against **User Visible LBA**.
- If a hidden partition exists, SecureWipe unhides the hidden sectors so they can be zeroed (+20 Points to Audit Confidence Score).

### Phase 3: Sector Zeroing & Hardware Key Shredding (`core/wipe_engine.py`)
What actually gets destroyed depends on the standard selected:

1. **NIST SP 800-88 Clear (HDD / Flash):**
   - Opens raw physical handle (`\\.\PhysicalDriveX`) in binary write mode (`rb+`).
   - Writes 1MB binary chunk buffers of `0x00` zeros across all sectors from LBA 0 to Max LBA.
   - Destroys partition tables (MBR/GPT), filesystem metadata (NTFS/ext4/FAT32), master file tables ($MFT), and raw user data.

2. **ANSSI Palier 2 (3-Pass Algorithm):**
   - *Pass 1:* Overwrites all LBA sectors with `0x00` zeros.
   - *Pass 2:* Overwrites all LBA sectors with `0xFF` ones.
   - *Pass 3:* Overwrites all LBA sectors with cryptographically random bytes (`os.urandom`).

3. **NIST SP 800-88 Purge / Crypto Erase (BitLocker / SED):**
   - Issues NVMe Format / ATA Secure Erase firmware commands.
   - Shreds the Master Encryption Key (MEK / Volume Master Key). Without the key, all drive blocks instantly revert to unrecoverable random noise.

### Phase 4: Verification & Confidence Calculation (`core/confidence.py`)
- Re-opens target drive in read-only binary mode (`rb`).
- Performs a 10% random LBA sector sampling across initial, mid-drive, and trailing sectors.
- Confirms every sampled byte contains strictly `0x00`.
- Calculates the weighted **Audit Confidence Score (0–100%)**:
  $$\text{Score} = \text{Firmware Erase (50pts)} + \text{Sampling Verification (30pts)} + \text{HPA Clearance (20pts)}$$

### Phase 5: Certificate Generation & Blockchain Anchoring (`cert/generator.py` & `trust/blockchain.py`)
- Renders signed PDF Certificate containing operator identity, serial number, timestamp, confidence score, and standard.
- Computes SHA-256 block hash:
  $$\text{Block Hash} = \text{SHA256}(\text{PrevHash} + \text{CertPDFHash} + \text{Timestamp} + \text{Serial})$$
- Appends block record to `trust/chain.json` and embeds scannable QR code on the PDF certificate pointing to `/verify?hash=<block_hash>`.

---

## 📊 Summary Table: What Gets Deleted

| Component | Standard Format / Reset | SecureWipe Execution |
| :--- | :--- | :--- |
| **User Files & Folders** | Unlinked (recoverable via Recuva) | **Zero-filled / Overwritten** |
| **Partition Table (GPT/MBR)** | Kept or reset | **Completely Overwritten** |
| **Master File Table ($MFT / Inodes)** | Marked free | **Zero-filled** |
| **Hidden Areas (HPA / DCO)** | **Ignored (Data leaks)** | **Unhidden & Zero-filled** |
| **Hardware Encryption Keys (MEK)** | Untouched | **Shredded / Destroyed** |

---

## 🏛️ Verification & Audit Integrity

The entire sanitization proof is verifiable offline or online:
1. Scan the embedded QR Code on the PDF certificate.
2. Query `GET /verify?hash=<block_hash>` on the verification server.
3. SecureWipe confirms whether the SHA-256 hash exists in `trust/chain.json` and returns the tamper-proof audit record.
