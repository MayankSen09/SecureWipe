"""
SecureWipe — disk_windows.py
Windows Storage Device Detection and Analysis.

Approach:
  - Get-PhysicalDisk (PowerShell/Storage module) → disk metadata
  - Get-Partition + Get-Volume → drive letter mapping
  - manage-bde -status → BitLocker encryption detection
  - WMI Win32_DiskDrive → fallback if Storage module is unavailable
  - diskpart → fallback for legacy platforms

Required Privileges: Local Administrator (Elevated UAC)
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from typing import Optional

from core.i18n import t

# ──────────────────────────────────────────────
# Windows Constants
# ──────────────────────────────────────────────

# MSFT_PhysicalDisk.MediaType
MEDIA_TYPE = {
    0: "unknown",
    3: "hdd",    # HDD
    4: "ssd",    # SSD
    5: "ssd",    # SCM (Storage Class Memory) → treated as SSD
}

# MSFT_PhysicalDisk.BusType
BUS_TYPE = {
    0 : "unknown",
    1 : "scsi",
    2 : "atapi",
    3 : "ata",
    4 : "ieee1394",
    5 : "ssa",
    6 : "fibre",
    7 : "usb",
    8 : "raid",
    9 : "iscsi",
    10: "sas",
    11: "sata",
    12: "sd",
    13: "mmc",
    17: "nvme",
    18: "scm",
    19: "ufs",
}

DISK_TYPE_HDD  = "hdd"
DISK_TYPE_SSD  = "ssd"
DISK_TYPE_NVME = "nvme"
DISK_TYPE_UNK  = "unknown"

ENC_NONE       = "none"
ENC_BITLOCKER  = "bitlocker"
ENC_SED        = "sed"

# ──────────────────────────────────────────────
# Data Structure (same interface as disk_linux)
# ──────────────────────────────────────────────

@dataclass
class DiskInfo:
    """Represents a physical storage device detected on Windows."""
    device: str          # e.g. \\.\PhysicalDrive0
    name: str            # e.g. PhysicalDrive0
    model: str
    serial: str
    disk_type: str       # hdd / ssd / nvme / unknown
    size_bytes: int
    size_human: str
    is_system: bool
    encryption: str      # none / bitlocker / sed
    transport: str       # sata / nvme / usb / ...
    vendor: str = ""
    firmware: str = ""
    drive_letters: list  = field(default_factory=list)   # e.g. ['C:', 'D:']
    device_id: str = ""  # Windows disk number (0, 1, 2...)
    smart_available: bool = False
    mountpoints: list    = field(default_factory=list)   # alias for drive_letters for Linux compatibility
    hpa_detected: bool = False
    hpa_wiped: bool = False


# ──────────────────────────────────────────────
# PowerShell Utilities
# ──────────────────────────────────────────────

def _run_ps(script: str, timeout: int = 15) -> tuple[int, str, str]:
    """
    Executes a PowerShell script and returns (rc, stdout, stderr).
    Uses -NonInteractive -NoProfile for execution speed.
    Enforces UTF-8 encoding for special characters.
    """

    # Pass script via a temporary file to avoid command-line escaping issues
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".ps1", delete=False, encoding="utf-8"
    ) as f:
        f.write("[Console]::OutputEncoding = [System.Text.Encoding]::UTF8\n")
        f.write("$OutputEncoding = [System.Text.Encoding]::UTF8\n")
        f.write(script)
        tmp_path = f.name

    try:
        r = subprocess.run(
            [
                "powershell.exe",
                "-NonInteractive",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-File", tmp_path,
            ],
            capture_output=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except FileNotFoundError:
        # PowerShell unavailable — fallback to pwsh (PowerShell Core)
        try:
            r = subprocess.run(
                ["pwsh", "-NonInteractive", "-NoProfile",
                 "-ExecutionPolicy", "Bypass", "-File", tmp_path],
                capture_output=True, timeout=timeout,
                encoding="utf-8", errors="replace",
            )
            return r.returncode, r.stdout.strip(), r.stderr.strip()
        except FileNotFoundError:
            return 127, "", "PowerShell not found"
    except subprocess.TimeoutExpired:
        return 124, "", "PowerShell timeout"
    except Exception as e:
        return 1, "", str(e)
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def _run_cmd(cmd: list[str], timeout: int = 10) -> tuple[int, str, str]:
    """Executes a standard cmd.exe command."""
    try:
        r = subprocess.run(
            cmd, capture_output=True, timeout=timeout,
            encoding="utf-8", errors="replace",
        )
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"Not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, "", "Timeout"
    except Exception as e:
        return 1, "", str(e)


# ──────────────────────────────────────────────
# Main PowerShell Script
# ──────────────────────────────────────────────

_PS_MAIN_SCRIPT = r"""
$ErrorActionPreference = 'SilentlyContinue'

# System drive (e.g. "C")
$sysDrive = ($env:SystemDrive).TrimEnd('\').TrimEnd(':')

# Drive letters grouped by disk number
$diskLetters = @{}
try {
    Get-Partition | Where-Object { $_.DriveLetter -and $_.DriveLetter -ne '' } | ForEach-Object {
        $num = $_.DiskNumber.ToString()
        $letter = ($_.DriveLetter.ToString()) + ':'
        if (-not $diskLetters[$num]) { $diskLetters[$num] = [System.Collections.Generic.List[string]]::new() }
        $diskLetters[$num].Add($letter)
    }
} catch {}

# Retrieve physical disks
$disks = @()
try {
    $physDisks = Get-PhysicalDisk
} catch {
    $physDisks = @()
}

foreach ($pd in $physDisks) {
    $devId = $pd.DeviceId.ToString().Trim()

    # Associated drive letters
    $letters = @()
    if ($diskLetters[$devId]) { $letters = $diskLetters[$devId].ToArray() }

    # Is system disk?
    $isSystem = $false
    foreach ($l in $letters) {
        if ($l.TrimEnd(':') -eq $sysDrive) { $isSystem = $true; break }
    }

    # BitLocker status
    $encType = 'none'
    foreach ($letter in $letters) {
        try {
            $bde = & manage-bde -status $letter 2>$null
            if ($bde -match 'Protection On') { $encType = 'bitlocker'; break }
        } catch {}
    }

    # Serial number sanitization
    $serial = 'N/A'
    if ($pd.SerialNumber -and $pd.SerialNumber.Trim() -ne '') {
        $serial = $pd.SerialNumber.Trim()
    }

    # Firmware version
    $fw = ''
    if ($pd.FirmwareVersion) { $fw = $pd.FirmwareVersion.Trim() }

    # BusType enrichment via Get-Disk
    $gdBusType = [int]$pd.BusType
    $isRemovable = $false
    try {
        $gd = Get-Disk -Number ([int]$devId) -ErrorAction SilentlyContinue
        if ($gd -and $gd.BusType) {
            if ($gd.BusType -eq "NVMe")     { $gdBusType = 17 }
            elseif ($gd.BusType -eq "SATA") { $gdBusType = 11 }
            elseif ($gd.BusType -eq "USB")  { $gdBusType = 7; $isRemovable = $true }
        }
        if ($gd.IsRemovable) { $isRemovable = $true }
    } catch {}

    $disks += [PSCustomObject]@{
        FriendlyName  = if ($pd.FriendlyName)  { $pd.FriendlyName.Trim()  } else { 'Unknown' }
        SerialNumber  = $serial
        MediaType     = [int]$pd.MediaType
        BusType       = $gdBusType
        IsRemovable   = $isRemovable
        Size          = [long]$pd.Size
        DeviceId      = $devId
        DriveLetters  = ($letters -join ',')
        IsSystem      = $isSystem
        Encryption    = $encType
        FirmwareVer   = $fw
    }
}

if ($disks.Count -gt 0) {
    $disks | ConvertTo-Json -Depth 3 -Compress
} else {
    # WMI fallback if Get-PhysicalDisk failed
    $wmiDisks = Get-WmiObject -Class Win32_DiskDrive
    $fallback = @()
    foreach ($wd in $wmiDisks) {
        $devNum  = $wd.Index.ToString()
        $letters = @()
        if ($diskLetters[$devNum]) { $letters = $diskLetters[$devNum].ToArray() }
        $isSystem = $false
        foreach ($l in $letters) {
            if ($l.TrimEnd(':') -eq $sysDrive) { $isSystem = $true; break }
        }
        $encType = 'none'
        foreach ($letter in $letters) {
            try {
                $bde = & manage-bde -status $letter 2>$null
                if ($bde -match 'Protection On') { $encType = 'bitlocker'; break }
            } catch {}
        }
        # WMI MediaType: "Fixed hard disk" -> 3 (HDD), detect SSD via name
        $mt = 3
        if ($wd.Model -match 'SSD|Solid') { $mt = 4 }
        if ($wd.Model -match 'NVMe|NVM') { $mt = 4 }

        $fallback += [PSCustomObject]@{
            FriendlyName  = if ($wd.Model) { $wd.Model.Trim() } else { 'Unknown' }
            SerialNumber  = if ($wd.SerialNumber) { $wd.SerialNumber.Trim() } else { 'N/A' }
            MediaType     = $mt
            BusType       = 11
            Size          = [long]$wd.Size
            DeviceId      = $devNum
            DriveLetters  = ($letters -join ',')
            IsSystem      = $isSystem
            Encryption    = $encType
            FirmwareVer   = if ($wd.FirmwareRevision) { $wd.FirmwareRevision.Trim() } else { '' }
        }
    }
    $fallback | ConvertTo-Json -Depth 3 -Compress
}
"""


# ──────────────────────────────────────────────
# Parsing
# ──────────────────────────────────────────────

def _bytes_to_human(n: int) -> str:
    """Same as disk_linux — local copy to prevent cross imports."""
    if n <= 0:
        return "? GiB"
    orig = n
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if n < 1024.0:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PiB"


def _detect_type(media_type: int, bus_type: int, model: str) -> str:
    """
    Determines HDD / SSD / NVMe.
    Priority: BusType NVMe > model name > MediaType > name heuristics.
    """
    model_upper = model.upper()

    # 1. BusType 17 = NVMe
    if bus_type == 17:
        return DISK_TYPE_NVME

    # 2. NVMe keywords in model name
    if re.search(r'NVME|NVM EXPRESS|M\.2|PCIE|PCIe', model_upper):
        return DISK_TYPE_NVME

    # 3. Known NVMe brands
    if re.search(r'MICRON.*(MTFD|2200|2400|3400)', model_upper):
        return DISK_TYPE_NVME
    if re.search(r'SAMSUNG.*(9[678]0|MZV|MZAL)', model_upper):
        return DISK_TYPE_NVME
    if re.search(r'WD.*SN[0-9]{3}', model_upper):
        return DISK_TYPE_NVME
    if re.search(r'SK HYNIX.*BC[0-9]', model_upper):
        return DISK_TYPE_NVME
    if re.search(r'KIOXIA|TOSHIBA.*KXG', model_upper):
        return DISK_TYPE_NVME
    if re.search(r'INTEL.*SSD.*[67][0-9]{2}P', model_upper):
        return DISK_TYPE_NVME

    # 4. Windows MediaType
    t = MEDIA_TYPE.get(media_type, DISK_TYPE_UNK)

    # 5. Name heuristics if MediaType unknown
    if t == DISK_TYPE_UNK:
        if re.search(r'\bSSD\b|SOLID.STATE', model_upper):
            return DISK_TYPE_SSD
        if re.search(r'\bHDD\b|BARRACUDA|IRONWOLF|SEAGATE|WESTERN DIGITAL WD[^S]', model_upper):
            return DISK_TYPE_HDD

    return t


def _parse_ps_output(raw_json: str) -> list[DiskInfo]:
    """Parses PowerShell JSON output into a list of DiskInfo."""
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        return []

    if isinstance(data, dict):
        data = [data]

    disks = []
    for d in data:
        dev_id   = str(d.get("DeviceId", "0")).strip()
        device   = f"\\\\.\\PhysicalDrive{dev_id}"
        name     = f"PhysicalDrive{dev_id}"
        model    = (d.get("FriendlyName") or "Unknown").strip()
        serial   = (d.get("SerialNumber") or "N/A").strip()
        media    = int(d.get("MediaType", 0))
        bus      = int(d.get("BusType", 0))
        size_b   = int(d.get("Size", 0))
        letters_raw = (d.get("DriveLetters") or "")
        letters  = [l.strip() for l in letters_raw.split(",") if l.strip()]
        is_sys   = bool(d.get("IsSystem", False))
        enc      = (d.get("Encryption") or "none").lower()
        fw       = (d.get("FirmwareVer") or "").strip()
        is_removable_flag = bool(d.get("IsRemovable", False))
        if is_removable_flag or bus == 7:
            transport = "usb"
        else:
            transport = BUS_TYPE.get(bus, "unknown")

        disk = DiskInfo(
            device       = device,
            name         = name,
            model        = model,
            serial       = serial,
            disk_type    = _detect_type(media, bus, model),
            size_bytes   = size_b,
            size_human   = _bytes_to_human(size_b),
            is_system    = is_sys,
            encryption   = enc,
            transport    = transport,
            firmware     = fw,
            drive_letters= letters,
            device_id    = dev_id,
            mountpoints  = letters,
        )
        disks.append(disk)

    disks.sort(key=lambda d: int(d.device_id) if d.device_id.isdigit() else 0)
    return disks


# ──────────────────────────────────────────────
# Tools Verification
# ──────────────────────────────────────────────

def check_windows_tools() -> dict[str, bool]:
    """Verifies availability of required tools on Windows."""

    def _ps_cmd_ok(cmd: str) -> bool:
        rc, out, _ = _run_ps(f"try {{ {cmd} | Out-Null; Write-Output 'ok' }} catch {{ Write-Output 'fail' }}")
        return rc == 0 and "ok" in out

    def _cmd_ok(name: str) -> bool:
        rc, _, _ = _run_cmd(["where", name])
        return rc == 0

    return {
        "powershell"  : _run_ps("Write-Output 'ok'")[1] == "ok",
        "Get-PhysicalDisk": _ps_cmd_ok("Get-PhysicalDisk"),
        "manage-bde"  : _cmd_ok("manage-bde"),
        "diskpart"    : _cmd_ok("diskpart"),
        "cipher"      : _cmd_ok("cipher"),
        "format"      : _cmd_ok("format"),
    }


# ──────────────────────────────────────────────
# Main Function
# ──────────────────────────────────────────────

def list_disks() -> list[DiskInfo]:
    """
    Detects all physical storage devices on Windows.
    Returns a list of DiskInfo.
    """
    rc, out, err = _run_ps(_PS_MAIN_SCRIPT, timeout=20)

    if rc != 0 or not out.strip():
        return []

    json_line = ""
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("[") or line.startswith("{"):
            json_line = line
            break

    if not json_line:
        return []

    return _parse_ps_output(json_line)


# ──────────────────────────────────────────────
# Disk Number from Drive Letter
# ──────────────────────────────────────────────

def get_disk_number_for_letter(letter: str) -> Optional[str]:
    """
    Returns physical disk number (e.g. '0') for a drive letter (e.g. 'C:').
    """
    script = f"""
$part = Get-Partition | Where-Object {{ $_.DriveLetter -eq '{letter.rstrip(':')[0]}' }}
if ($part) {{ Write-Output $part.DiskNumber }} else {{ Write-Output '' }}
"""
    rc, out, _ = _run_ps(script)
    return out.strip() if rc == 0 and out.strip().isdigit() else None


# ──────────────────────────────────────────────
# Mock for testing
# ──────────────────────────────────────────────

def _mock_disks() -> list[DiskInfo]:
    """
    Realistic mock disks for testing outside Windows.
    """

    return [
        DiskInfo(
            device=r"[MOCK] \\.\PhysicalDrive0",
            name="PhysicalDrive0",
            model="Samsung SSD 870 EVO 500GB",
            serial="S5YXNX0T654321",
            disk_type=DISK_TYPE_SSD,
            size_bytes=500_107_862_016,
            size_human="465.8 GiB",
            is_system=False,
            encryption=ENC_NONE,
            transport="sata",
            firmware="SVT01B6Q",
            drive_letters=["D:"],
            device_id="0",
            mountpoints=["D:"],
        ),
        DiskInfo(
            device=r"[MOCK] \\.\PhysicalDrive1",
            name="PhysicalDrive1",
            model="Seagate Barracuda ST2000DM008",
            serial="ZFN0ABCD",
            disk_type=DISK_TYPE_HDD,
            size_bytes=2_000_398_934_016,
            size_human="1.8 TiB",
            is_system=True,
            encryption=ENC_BITLOCKER,
            transport="sata",
            firmware="0001",
            drive_letters=["C:"],
            device_id="1",
            mountpoints=["C:"],
        ),
        DiskInfo(
            device=r"[MOCK] \\.\PhysicalDrive2",
            name="PhysicalDrive2",
            model="WD Black SN850X 1TB NVMe",
            serial="WD987654321",
            disk_type=DISK_TYPE_NVME,
            size_bytes=1_000_204_886_016,
            size_human="931.5 GiB",
            is_system=False,
            encryption=ENC_NONE,
            transport="nvme",
            firmware="620131WD",
            drive_letters=["E:"],
            device_id="2",
            mountpoints=["E:"],
        ),
    ]
