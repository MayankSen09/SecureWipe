"""
SecureWipe — crypto_detect.py
Analysis of detected encryption and recommendation of the appropriate
cryptographic erasure method.
Author: TEAM SOLUTION

This module is cross-platform: it takes a DiskInfo (Linux or Windows)
and returns a CryptoProfile describing what actions to take.
"""

import re
import sys
import subprocess
import os
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

# ──────────────────────────────────────────────
# Enumerations
# ──────────────────────────────────────────────

class CryptoMethod(Enum):
    """Recommended cryptographic wipe method."""
    NONE             = auto()   # No encryption → no crypto erase
    LUKS_ERASE       = auto()   # cryptsetup erase (LUKS1/2)
    SED_ATA          = auto()   # hdparm ATA Secure Erase (SED SATA)
    SED_NVME         = auto()   # nvme format --ses=1 (SED NVMe)
    BITLOCKER_OFF    = auto()   # manage-bde -off then format
    BITLOCKER_KEY    = auto()   # BitLocker key deletion (if recovery key access available)


class SedStatus(Enum):
    """SED lock status (ATA Security Feature Set)."""
    NOT_SUPPORTED = auto()
    FROZEN        = auto()   # Frozen = cannot send Secure Erase without reboot
    LOCKED        = auto()
    ENABLED       = auto()   # Ready for Secure Erase
    NOT_ENABLED   = auto()   # SED present but not enabled


# ──────────────────────────────────────────────
# Result Structure
# ──────────────────────────────────────────────

@dataclass
class CryptoProfile:
    """
    Complete result of cryptographic analysis on a disk.
    Passed to wipe_engine to execute the correct method.
    """
    # Is a crypto erase option available?
    has_crypto_option: bool = False

    # Recommended method
    recommended_method: CryptoMethod = CryptoMethod.NONE

    # LUKS details
    luks_version: str = ""          # "LUKS1" or "LUKS2"
    luks_device: str = ""           # e.g.: /dev/sda1 (LUKS partition)
    luks_cipher: str = ""           # e.g.: aes-xts-plain64

    # SED details
    sed_frozen: bool = False        # True → Secure Erase impossible without reboot
    sed_enhanced: bool = False      # True → Enhanced Secure Erase available
    sed_time_min: int = 2           # Estimated duration in minutes

    # BitLocker details
    bitlocker_drives: list = field(default_factory=list)  # e.g.: ["C:"]
    bitlocker_pct: int = 0          # % encrypted

    # Warnings to display to the user
    warnings: list = field(default_factory=list)

    # Display info
    display_name: str = ""          # Short name for the menu
    display_desc: str = ""          # Description for the menu


# ──────────────────────────────────────────────
# Subprocess Utility
# ──────────────────────────────────────────────

def _run(cmd: list, timeout: int = 8) -> tuple[int, str, str]:
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            env={**os.environ, "LANG": "C", "LC_ALL": "C"},
        )
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except Exception as e:
        return 1, "", str(e)


def _tool_ok(name: str) -> bool:
    rc, _, _ = _run(["which", name] if sys.platform != "win32" else ["where", name])
    return rc == 0


# ──────────────────────────────────────────────
# LUKS Analysis (Linux)
# ──────────────────────────────────────────────

def _analyse_luks(device: str) -> tuple[str, str, str, str]:
    """
    Returns (luks_version, luks_device, luks_cipher, warning).
    Uses cryptsetup luksDump to obtain details.
    """
    # Look for LUKS partition on this disk via blkid
    luks_device = ""
    rc, out, _ = _run(["blkid", "-t", "TYPE=crypto_LUKS", "-o", "device"])
    if rc == 0 and out:
        for line in out.splitlines():
            line = line.strip()
            # Keep partitions belonging to this disk (e.g., /dev/sda → /dev/sda1, /dev/sda2)
            dev_base = device.rstrip("0123456789").replace("n1", "")  # nvme0n1 → /dev/nvme0
            if line.startswith(device) or line.startswith(dev_base):
                luks_device = line
                break
        if not luks_device and out.splitlines():
            luks_device = out.splitlines()[0].strip()

    if not luks_device:
        luks_device = device  # fallback to entire disk

    # luksDump for details
    luks_version = "LUKS"
    luks_cipher  = "aes-xts-plain64"
    warning      = ""

    if _tool_ok("cryptsetup"):
        rc, out, _ = _run(["cryptsetup", "luksDump", luks_device], timeout=5)
        if rc == 0:
            v = re.search(r'Version:\s+(\d)', out)
            c = re.search(r'[Cc]ipher(?:\s+name)?:\s+(\S+)', out)
            if v:
                luks_version = f"LUKS{v.group(1)}"
            if c:
                luks_cipher = c.group(1)
        else:
            warning = "cryptsetup luksDump failed — the disk will still be wiped via luksErase."
    else:
        warning = "cryptsetup not installed — LUKS erase will be performed via dd on the partition."

    return luks_version, luks_device, luks_cipher, warning


# ──────────────────────────────────────────────
# SED / ATA Security Analysis (Linux)
# ──────────────────────────────────────────────

def _analyse_sed_linux(device: str) -> tuple[SedStatus, bool, int]:
    """
    Analyzes ATA Security state via hdparm -I.
    Returns (status, enhanced_available, erase_time_min).
    """
    if not _tool_ok("hdparm"):
        return SedStatus.NOT_SUPPORTED, False, 2

    rc, out, _ = _run(["hdparm", "-I", device], timeout=6)
    if rc != 0:
        return SedStatus.NOT_SUPPORTED, False, 2

    # Security section in hdparm output
    in_security = False
    supported    = False
    enabled      = False
    frozen       = False
    locked       = False
    enhanced     = False
    erase_min    = 2

    for line in out.splitlines():
        if re.search(r'^\s*Security:', line):
            in_security = True
            continue
        if not in_security:
            continue
        # End of section: non-empty line starting at column 0 (no indentation)
        if line and not line[0].isspace() and "Security" not in line:
            break

        l = line.lower().strip()
        if not l:
            continue
        # Detect negation "not X" to avoid inverted meanings
        is_negated = l.startswith("not")
        if "supported" in l and not is_negated:
            supported = True
        if "enabled" in l and not is_negated:
            enabled = True
        if "frozen" in l and not is_negated:
            frozen = True
        if "locked" in l and not is_negated:
            locked = True
        if "enhanced erase" in l:
            enhanced = True
        # Estimated time: "2min for SECURITY ERASE UNIT"
        m = re.search(r'(\d+)min for security erase', l)
        if m:
            erase_min = int(m.group(1))

    if not supported:
        return SedStatus.NOT_SUPPORTED, False, 2
    if frozen:
        return SedStatus.FROZEN, enhanced, erase_min
    if locked:
        return SedStatus.LOCKED, enhanced, erase_min
    if enabled:
        return SedStatus.ENABLED, enhanced, erase_min
    return SedStatus.NOT_ENABLED, enhanced, erase_min


# ──────────────────────────────────────────────
# BitLocker Analysis (Windows)
# ──────────────────────────────────────────────

def _analyse_bitlocker_windows(drive_letters: list) -> tuple[list, int, str]:
    """
    Analyzes BitLocker status on disk drive letters.
    Returns (encrypted_drives, pct_encrypted, warning).
    """
    encrypted = []
    pct_total = 0
    warning   = ""

    for letter in drive_letters:
        rc, out, _ = _run(["manage-bde", "-status", letter], timeout=8)
        if rc != 0:
            continue
        # Protection Status
        ps = re.search(r'Protection Status:\s+(.+)', out)
        if ps and "on" in ps.group(1).lower():
            encrypted.append(letter)
        # % encrypted
        pct = re.search(r'Percentage Encrypted:\s+([\d.]+)%', out)
        if pct:
            pct_total = max(pct_total, int(float(pct.group(1))))

    if not encrypted:
        warning = "manage-bde indicates BitLocker is not active on this disk."

    return encrypted, pct_total, warning


# ──────────────────────────────────────────────
# NVMe Secure Erase Analysis
# ──────────────────────────────────────────────

def _analyse_nvme(device: str) -> tuple[bool, str]:
    """
    Checks if nvme-cli is available and if NVMe format is supported.
    Returns (supported, warning).
    """
    if not _tool_ok("nvme"):
        return False, "nvme-cli not installed. Install with: apt install nvme-cli"

    # nvme id-ctrl to verify support for Format NVM Command
    rc, out, _ = _run(["nvme", "id-ctrl", device, "--output-format=normal"], timeout=6)
    if rc != 0:
        return True, ""  # Assume supported if unable to verify

    # Check fna (Format NVM Attributes) — bit 2 = supports crypto erase
    fna = re.search(r'fna\s*:\s*(0x[0-9a-fA-F]+|\d+)', out)
    if fna:
        val = int(fna.group(1), 16) if fna.group(1).startswith("0x") else int(fna.group(1))
        if val & 0x4:  # bit 2 = Cryptographic Erase supported
            return True, ""
        else:
            return True, "NVMe controller supports Format but not necessarily Crypto Erase (fna bit 2 = 0). Wiping will still proceed."

    return True, ""


# ──────────────────────────────────────────────
# Main Function
# ──────────────────────────────────────────────

def analyse_disk_crypto(disk) -> CryptoProfile:
    """
    Analyzes encryption on a DiskInfo (Linux or Windows).
    Returns a CryptoProfile with recommended method and details.

    Compatible with disk_linux.DiskInfo and disk_windows.DiskInfo
    via common interface.
    """
    profile = CryptoProfile()

    enc       = getattr(disk, "encryption", "none").lower()
    dtype     = getattr(disk, "disk_type", "unknown").lower()
    device    = getattr(disk, "device", "")
    transport = getattr(disk, "transport", "").lower()
    letters   = getattr(disk, "drive_letters", []) or getattr(disk, "mountpoints", [])

    is_linux   = sys.platform != "win32"
    is_windows = sys.platform == "win32"

    # ── Case 1: LUKS (Linux) ──────────────────
    if enc == "luks" and is_linux:
        luks_v, luks_dev, luks_cipher, warn = _analyse_luks(device)
        profile.has_crypto_option    = True
        profile.recommended_method   = CryptoMethod.LUKS_ERASE
        profile.luks_version         = luks_v
        profile.luks_device          = luks_dev
        profile.luks_cipher          = luks_cipher
        profile.display_name         = f"Crypto Erase — {luks_v}"
        profile.display_desc         = (
            f"Destruction of the {luks_v} master key ({luks_cipher}). "
            "Data becomes immediately inaccessible."
        )
        if warn:
            profile.warnings.append(warn)
        return profile

    # ── Case 2: SED (Linux, SATA) ─────────────
    if enc == "sed" and is_linux and dtype in ("hdd", "ssd"):
        status, enhanced, erase_min = _analyse_sed_linux(device)

        if status == SedStatus.FROZEN:
            profile.has_crypto_option = True
            profile.recommended_method = CryptoMethod.SED_ATA
            profile.sed_frozen    = True
            profile.sed_enhanced  = enhanced
            profile.sed_time_min  = erase_min
            profile.warnings.append(
                "⚠ The SED disk is in 'frozen' state (locked by BIOS/UEFI).\n"
                "  → Unplug and hot-plug the SATA disk,\n"
                "    or reboot from a LiveUSB without SED sleep,\n"
                "    then restart SecureWipe."
            )
            profile.display_name = "Crypto Erase — SED ATA (⚠ frozen)"
            profile.display_desc = "ATA Secure Erase available after unlocking frozen state."

        elif status in (SedStatus.ENABLED, SedStatus.NOT_ENABLED, SedStatus.LOCKED):
            profile.has_crypto_option  = True
            profile.recommended_method = CryptoMethod.SED_ATA
            profile.sed_frozen    = False
            profile.sed_enhanced  = enhanced
            profile.sed_time_min  = erase_min
            profile.display_name  = "Crypto Erase — SED ATA Secure Erase"
            profile.display_desc  = (
                f"ATA Secure Erase{' Enhanced' if enhanced else ''} command. "
                f"Estimated duration: {erase_min} min."
            )
        else:
            profile.has_crypto_option = False
            profile.recommended_method = CryptoMethod.NONE

        return profile

    # ── Case 3: SED NVMe (Linux) ──────────────
    if enc == "sed" and is_linux and dtype == "nvme":
        supported, warn = _analyse_nvme(device)
        profile.has_crypto_option  = supported
        profile.recommended_method = CryptoMethod.SED_NVME if supported else CryptoMethod.NONE
        profile.display_name       = "Crypto Erase — NVMe Format (--ses=1)"
        profile.display_desc       = "nvme format with Cryptographic Erase. Data immediately inaccessible."
        if warn:
            profile.warnings.append(warn)
        return profile

    # ── Case 4: BitLocker (Windows) ───────────
    if enc == "bitlocker" and is_windows:
        enc_drives, pct, warn = _analyse_bitlocker_windows(letters)
        profile.has_crypto_option    = True
        profile.recommended_method   = CryptoMethod.BITLOCKER_OFF
        profile.bitlocker_drives     = enc_drives or letters
        profile.bitlocker_pct        = pct
        profile.display_name         = "Crypto Erase — Disable BitLocker"
        profile.display_desc         = (
            f"Disables BitLocker ({pct}% encrypted) then formats the disk. "
            "AES key destroyed, data inaccessible."
        )
        if warn:
            profile.warnings.append(warn)
        return profile

    # ── Case 5: No Encryption ─────────────────
    profile.has_crypto_option  = False
    profile.recommended_method = CryptoMethod.NONE
    return profile


# ──────────────────────────────────────────────
# Readable Summary for UI
# ──────────────────────────────────────────────

def crypto_summary(profile: CryptoProfile, lang: str = "en") -> dict:
    """
    Returns a dict ready for display in the wipe_mode menu.
    {
        'available': bool,
        'name': str,
        'desc': str,
        'warnings': list[str],
        'method': CryptoMethod,
    }
    """
    return {
        "available": profile.has_crypto_option,
        "name":      profile.display_name,
        "desc":      profile.display_desc,
        "warnings":  profile.warnings,
        "method":    profile.recommended_method,
        "profile":   profile,
    }
