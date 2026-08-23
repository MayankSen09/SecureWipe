#Requires -Version 5.1
<#
.SYNOPSIS
    SecureWipe - install.ps1
    Windows Dependency Installer
.EXAMPLE
    powershell.exe -ExecutionPolicy Bypass -File install.ps1
#>

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonMinVersion = [Version]"3.10.0"

function Write-Header($text) {
    Write-Host ""
    Write-Host "  $text" -ForegroundColor Cyan
    Write-Host ("  " + ("-" * $text.Length)) -ForegroundColor DarkBlue
}

function Write-Ok($text)   { Write-Host "  [OK] $text" -ForegroundColor Green  }
function Write-Warn($text) { Write-Host "  [!]  $text" -ForegroundColor Yellow }
function Write-Err($text)  { Write-Host "  [X]  $text" -ForegroundColor Red    }
function Write-Info($text) { Write-Host "  ->   $text" -ForegroundColor White  }

Write-Host ""
Write-Host "  +------------------------------------------+" -ForegroundColor Cyan
Write-Host "  |      SecureWipe -- Installation          |" -ForegroundColor Cyan
Write-Host "  +------------------------------------------+" -ForegroundColor Cyan
Write-Host ""

$IsAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator
)

if (-not $IsAdmin) {
    Write-Err "This script must be run as Administrator."
    Write-Info "Right click install.ps1 -> Run with PowerShell (as Administrator)"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Ok "Administrator privileges confirmed"

Write-Header "[1/4] Verifying Python installation"

$PythonCmd = $null

foreach ($cmd in @("python3", "python", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python (\d+\.\d+\.\d+)") {
            $foundVer = [Version]$matches[1]
            if ($foundVer -ge $PythonMinVersion) {
                $PythonCmd = $cmd
                Write-Ok "Python $foundVer found ($cmd)"
                break
            } else {
                Write-Warn "Python $foundVer found but version is too old (minimum 3.10 required)"
            }
        }
    } catch {}
}

if (-not $PythonCmd) {
    Write-Warn "Python 3.10+ not found. Attempting install via winget..."
    try {
        winget install Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
        $machinePath = [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
        $userPath    = [System.Environment]::GetEnvironmentVariable("PATH", "User")
        $env:PATH    = $machinePath + ";" + $userPath
        $PythonCmd   = "python"
        Write-Ok "Python installed via winget"
    } catch {
        Write-Err "Unable to install Python automatically."
        Write-Info "Please download Python 3.10+ from https://www.python.org/downloads/"
        Write-Info "Check 'Add Python to PATH' during installation"
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Header "[2/4] Installing Python dependencies"

$RequirementsFile = Join-Path $ScriptDir "requirements.txt"

if (-not (Test-Path $RequirementsFile)) {
    Write-Err "requirements.txt not found in $ScriptDir"
    exit 1
}

try {
    Write-Info "pip install -r requirements.txt..."
    & $PythonCmd -m pip install -r $RequirementsFile --quiet --upgrade
    Write-Ok "Python dependencies installed"
} catch {
    Write-Err "pip error: $_"
    Write-Info "Manual command: $PythonCmd -m pip install rich reportlab qrcode[pil] Pillow psutil"
    exit 1
}

Write-Header "[3/4] Verifying Windows native utilities"

$tools = @{
    "manage-bde" = "BitLocker Management (Windows Native)"
    "diskpart"   = "Disk Management (Windows Native)"
    "cipher"     = "EFS Encryption (Windows Native)"
}

foreach ($tool in $tools.Keys) {
    $found = Get-Command $tool -ErrorAction SilentlyContinue
    if ($found) {
        Write-Ok "$tool -- $($tools[$tool])"
    } else {
        Write-Warn "$tool not found -- $($tools[$tool])"
    }
}

try {
    $null = Get-PhysicalDisk -ErrorAction Stop
    Write-Ok "Get-PhysicalDisk available"
} catch {
    Write-Warn "Get-PhysicalDisk not available -- WMI fallback will be used"
}

Write-Header "[4/4] Final Verification"

try {
    $check = & $PythonCmd -c "import rich, reportlab, qrcode, PIL; print('OK')" 2>&1
    if ($check -eq "OK") {
        Write-Ok "All Python dependencies are available"
    } else {
        Write-Err "Incomplete Python dependencies: $check"
        exit 1
    }
} catch {
    Write-Err "Verification error: $_"
    exit 1
}

Write-Host ""
Write-Host "  +------------------------------------------+" -ForegroundColor Green
Write-Host "  |  Installation Completed Successfully!    |" -ForegroundColor Green
Write-Host "  +------------------------------------------+" -ForegroundColor Green
Write-Host ""
Write-Host "  Standard Launch (admin required):" -ForegroundColor White
Write-Host "  $PythonCmd securewipe.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Mock Mode (testing without real wipe):" -ForegroundColor White
Write-Host "  Set SECUREWIPE_MOCK=1 then: $PythonCmd securewipe.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Web Server & Verification API:" -ForegroundColor White
Write-Host "  $PythonCmd api/app.py" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"

