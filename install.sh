#!/usr/bin/env bash
# =============================================================================
# SecureWipe — install.sh
# Linux Dependency Installer
# Usage: sudo bash install.sh
# =============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║       SecureWipe — Installation          ║${NC}"
echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════╝${NC}"
echo ""

# ── Privilege Verification ──
if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}ERROR: This script must be run with root privileges.${NC}"
    echo "  → sudo bash install.sh"
    exit 1
fi

# ── Package Manager Detection ──
if command -v apt-get &>/dev/null; then
    PKG_MANAGER="apt"
elif command -v dnf &>/dev/null; then
    PKG_MANAGER="dnf"
elif command -v yum &>/dev/null; then
    PKG_MANAGER="yum"
elif command -v pacman &>/dev/null; then
    PKG_MANAGER="pacman"
else
    echo -e "${YELLOW}⚠ Package manager not detected. Installing Python dependencies only.${NC}"
    PKG_MANAGER="none"
fi

echo -e "  Package Manager: ${CYAN}${PKG_MANAGER}${NC}"
echo ""

# ── System Utilities ──
install_sys_tools() {
    echo -e "${BOLD}[1/3] Installing system tools...${NC}"

    PKGS_APT="python3 python3-pip hdparm nvme-cli smartmontools util-linux"
    PKGS_DNF="python3 python3-pip hdparm nvme-cli smartmontools util-linux"
    PKGS_PAC="python python-pip hdparm nvme-cli smartmontools util-linux"

    case $PKG_MANAGER in
        apt)
            apt-get update -qq
            apt-get install -y $PKGS_APT 2>/dev/null || \
                echo -e "  ${YELLOW}Some optional packages were unavailable (skipped)${NC}"
            ;;
        dnf|yum)
            $PKG_MANAGER install -y $PKGS_DNF 2>/dev/null || true
            ;;
        pacman)
            pacman -Sy --noconfirm $PKGS_PAC 2>/dev/null || true
            ;;
        none)
            echo -e "  ${YELLOW}Skipped (no package manager found)${NC}"
            ;;
    esac

    echo -e "  ${GREEN}✓${NC} System tools"
}

# ── Python Environment ──
check_python() {
    echo -e "${BOLD}[2/3] Verifying Python installation...${NC}"

    if command -v python3 &>/dev/null; then
        PY_VER=$(python3 --version 2>&1 | awk '{print $2}')
        PY_MAJOR=$(echo $PY_VER | cut -d. -f1)
        PY_MINOR=$(echo $PY_VER | cut -d. -f2)

        if [[ $PY_MAJOR -ge 3 && $PY_MINOR -ge 10 ]]; then
            echo -e "  ${GREEN}✓${NC} Python ${PY_VER} (OK)"
        else
            echo -e "  ${YELLOW}⚠ Python ${PY_VER} — SecureWipe requires Python 3.10+${NC}"
            echo "  → Update Python if issues arise."
        fi
    else
        echo -e "  ${RED}✗ Python3 not found. Please install Python 3.10+${NC}"
        exit 1
    fi
}

# ── Python Dependencies ──
install_python_deps() {
    echo -e "${BOLD}[3/3] Installing Python dependencies...${NC}"

    if python3 -m pip install -r "${SCRIPT_DIR}/requirements.txt" --quiet 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Python dependencies installed"
    elif python3 -m pip install -r "${SCRIPT_DIR}/requirements.txt" \
            --break-system-packages --quiet 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Python dependencies installed (--break-system-packages)"
    else
        echo -e "  ${YELLOW}Attempting virtual environment setup...${NC}"
        python3 -m venv "${SCRIPT_DIR}/.venv"
        "${SCRIPT_DIR}/.venv/bin/pip" install -r "${SCRIPT_DIR}/requirements.txt" --quiet
        echo -e "  ${GREEN}✓${NC} Dependencies installed in .venv"
        echo -e "  ${YELLOW}ℹ To activate virtual environment: source ${SCRIPT_DIR}/.venv/bin/activate${NC}"
    fi
}

# ── Permissions ──
set_permissions() {
    chmod +x "${SCRIPT_DIR}/securewipe.py"
    chmod +x "${SCRIPT_DIR}/install.sh"
    echo -e "  ${GREEN}✓${NC} Execution permissions set"
}

# ── Final Verification ──
verify_install() {
    echo ""
    echo -e "${BOLD}Verifying installation:${NC}"

    for tool in python3 hdparm nvme smartctl dd shred lsblk; do
        if command -v $tool &>/dev/null; then
            echo -e "  ${GREEN}✓${NC} ${tool}"
        else
            echo -e "  ${YELLOW}✗${NC} ${tool} (optional)"
        fi
    done

    echo ""
    if python3 -c "import rich, reportlab, qrcode, PIL" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Python dependencies OK"
    else
        echo -e "  ${RED}✗ Missing Python dependencies — please re-run install.sh${NC}"
        exit 1
    fi
}

# ── Main ──
install_sys_tools
echo ""
check_python
echo ""
install_python_deps
echo ""
set_permissions
verify_install

echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║    Installation Completed Successfully!   ║${NC}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  CLI Launch: ${CYAN}sudo python3 securewipe.py${NC}"
echo -e "  Web Server & Verification API: ${CYAN}python3 api/app.py${NC}"
echo ""



# Note: verify permissions before execution
