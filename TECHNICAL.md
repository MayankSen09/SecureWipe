# SecureWipe — Technical Documentation

## Overview

### Why a Simple Format is Not Enough

When you delete a file or format a disk, the operating system **only removes the pointer** to the data — like tearing out a book's index without destroying the pages. The data remains physically present on the disk and can be recovered with specialized tools (TestDisk, PhotoRec, Recuva, etc.) within minutes.

SecureWipe overwrites the actual data, making any recovery impossible.

---

### The 5 Sanitization Modes

---

#### Mode 1 — ANSSI Level 1: 1 Zero Pass

**What it does:**
The program writes `0x00` (null bytes) over every sector of the disk from end to end in a single pass. It then reads 10% of sectors at random to verify they contain zeros.

**Security level:** ⭐⭐⭐☆☆
**Speed:** Fast (limited by disk speed)
**Use case:** Internal transfers within the same organization.

**ANSSI Guidelines:**
This corresponds to ANSSI Level 1 of the data destruction guide. Sufficient for internal transfers where the trust level between parties is established.

**Limits:**
A highly motivated adversary with laboratory equipment (magnetic force microscope) could theoretically read residual traces on an HDD. In practice, no real attack has been documented on modern drives.

---

#### Mode 2 — ANSSI Level 2 / NIST Clear: 1 Random Pass

**What it does:**
The program writes **cryptographically secure pseudo-random data** (`/dev/urandom` on Linux, `secrets.token_bytes()` on Windows) over every sector in a single pass. Verification confirms the written data is not uniformly null.

**Security level:** ⭐⭐⭐⭐☆
**Speed:** Slightly slower than Level 1 (random generation)
**Use case:** Transfer to a third party, hardware resale, standard disposal.

**ANSSI and NIST Guidelines:**
- ANSSI Level 2: mandatory when hardware leaves the organization's perimeter.
- NIST SP 800-88 "Clear": recommended level for low to medium sensitivity data.

**Why is one pass enough on modern drives?**
Drives manufactured after 2000 have such high recording density that residual traces after a single random pass are undetectable even in a lab. The Gutmann method (35 passes) was designed for 1980–1990 drives and is now obsolete — its own author acknowledges this.

---

#### Mode 3 — NIST Purge: ATA Secure Erase / NVMe Format

**What it does:**
Instead of writing data from the OS, this mode sends a **command directly to the disk firmware** to erase itself.

**On HDD/SSD SATA** (`hdparm --security-erase`):
The disk firmware resets all its cells, including zones **normally inaccessible from the OS**: replacement sectors (reallocated sectors), HPA (Host Protected Area), DCO (Device Configuration Overlay). Standard software erasure cannot reach these zones.

**On NVMe** (`nvme format --ses=2`):
The NVMe controller regenerates its internal encryption key. All existing data, including in wear-leveling reserved zones, becomes **mathematically inaccessible** instantly.

**Security level:** ⭐⭐⭐⭐⭐
**Speed:** Variable (seconds to several hours depending on model)
**Use case:** Sensitive data, health records, classified data. Recommended default method for all SSD/NVMe.

**NIST Guidelines:**
NIST SP 800-88 "Purge": recommended level before any perimeter exit for high sensitivity data. Only level guaranteeing erasure of inaccessible zones.

**Why is this mode essential for SSDs?**
On an SSD, writes never go to the same physical location twice (wear-leveling). If you overwrite a file, the old version remains on a different cell that the OS cannot address. Only the firmware knows the actual location of all data — hence the need to go through it.

**Limit:**
Not available on USB-connected drives. The USB-SATA bridge blocks ATA Security commands in 95% of cases — a hardware limitation, not a software one.

---

#### Mode 4 — Crypto Erase: Encryption Key Destruction

**What it does:**
If the disk is encrypted (LUKS on Linux, BitLocker on Windows, SED), SecureWipe destroys the **encryption key** rather than overwriting the data.

**LUKS** (`cryptsetup erase`):
Destroys all key slots. The AES-256 master key disappears. Data on the disk remains physically present but is random noise without the key — recovery impossible, even in a lab.

**BitLocker** (`manage-bde -off`):
Removes the VMK (Volume Master Key) and FVEK (Full Volume Encryption Key) from the TPM and disk.

**SED — Self-Encrypting Drive** (`hdparm --security-erase`):
The drive permanently encrypts all its data with an internal key. The Secure Erase command regenerates this key — the entire disk becomes instantly unreadable.

**Security level:** ⭐⭐⭐⭐⭐
**Speed:** Instant (a few seconds)
**Use case:** Any already-encrypted disk. Fastest and most secure method when encryption is in place.

**Why is it as secure as NIST Purge?**
The security of AES-256 is such that without the key, brute-forcing the encryption would take longer than the age of the universe with all current supercomputers combined.

**Recommendation:**
Systematically encrypt your disks from day one (BitLocker, LUKS). Future erasure will be instant and irreversible.

---

#### Mode 5 — Custom: Configurable N Passes

**What it does:**
Performs between 2 and 7 passes alternating zeros and random data. Example for 3 passes: zeros → random → zeros.

**Security level:** ⭐⭐⭐⭐☆ (identical to Level 2 in practice)
**Speed:** Slow (N times longer than a single pass)
**Use case:** Documentary compliance requiring multiple passes, or peace of mind.

**Important Note:**
SecureWipe displays an explicit warning: multiple passes provide **no measurable security benefit** on modern drives compared to a single random pass. This mode exists solely to comply with internal policies that explicitly require it.

---

### Summary Table

| Mode | Method | Media | Inaccessible zones | Speed | Recommended use |
|------|--------|-------|--------------------|-------|----------------|
| ANSSI Level 1 | 1 zero pass | HDD | No | Fast | Internal transfer |
| ANSSI Level 2 | 1 random pass | HDD | No | Fast | External transfer, resale |
| NIST Purge | Firmware Secure Erase | HDD + SSD + NVMe | **Yes** | Variable | Sensitive data |
| Crypto Erase | AES key destruction | LUKS / BitLocker / SED | **Yes** | Instant | Encrypted disk |
| Custom | N passes | HDD | No | Slow | Documentary compliance |

---

### The PDF Certificate

After each wipe, SecureWipe generates a certificate including:

- **Unique timestamped ID** (format `YYYYMMDDHHmm`)
- **Device information**: model, serial number, capacity, type
- **Method applied** and compliance standard
- **Post-wipe verification result**
- **Operation duration**
- **Certificate SHA-256** + offline-verifiable QR code
- **Anti-falsification watermark**

This document constitutes reasonable due diligence evidence for GDPR, HDS or NIS2 audits.
