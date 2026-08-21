"""
SecureWipe — ui.py
UI components: banner, operator input, rich menus.
Author: TEAM SOLUTION
"""

import sys
import platform
import socket
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.rule import Rule
from rich import print as rprint
from rich.text import Text

from core.i18n import t

console = Console()


# ──────────────────────────────────────────────
# Main Banner
# ──────────────────────────────────────────────

def print_banner():
    """Displays the SecureWipe banner."""
    console.print()
    console.print(Panel(
        Text.from_markup(
            f"[bold cyan]{t('app_title')}[/bold cyan]\n"
            f"[dim]{t('app_subtitle')}[/dim]"
        ),
        border_style="bold blue",
        padding=(1, 4),
    ))
    console.print()


def print_section(title: str):
    """Displays a section divider."""
    console.print()
    console.print(Rule(f"[bold cyan]{title}[/bold cyan]", style="blue"))
    console.print()


# ──────────────────────────────────────────────
# Privilege Check
# ──────────────────────────────────────────────

def check_privileges():
    """Checks for root/admin privileges. Exits cleanly otherwise."""
    is_root = False

    if sys.platform == "win32":
        try:
            import ctypes
            is_root = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            is_root = False
    else:
        import os
        is_root = (os.geteuid() == 0)

    if not is_root:
        console.print()
        rprint(t("err_not_root"))
        console.print()
        sys.exit(1)


# ──────────────────────────────────────────────
# Operator Information Input
# ──────────────────────────────────────────────

def prompt_operator() -> dict:
    """
    Prompts for the operator's name and organization.
    Returns a dict {name, org, machine, os, datetime}.
    """
    print_section(t("prompt_operator_title"))

    # Name
    while True:
        name = Prompt.ask(
            f"  [bold]{t('prompt_operator_name')}[/bold]",
            console=console,
        ).strip()
        if name:
            break
        rprint(f"  {t('prompt_operator_empty')}")

    console.print()
    rprint(f"  [green]✓[/green] [bold]{name}[/bold]")
    console.print()

    return {
        "name": name,
        "org": "",
        "machine": _get_hostname(),
        "os": _get_os_string(),
        "datetime": datetime.now(),
    }


# ──────────────────────────────────────────────
# System Helpers
# ──────────────────────────────────────────────

def _get_hostname() -> str:
    try:
        return socket.gethostname()
    except Exception:
        return "unknown"


def _get_os_string() -> str:
    try:
        if sys.platform == "win32":
            # Windows 11 detection: build >= 22000
            # platform.release() returns "10" even on Win11
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
                build = int(winreg.QueryValueEx(key, "CurrentBuildNumber")[0])
                name  = winreg.QueryValueEx(key, "ProductName")[0]
                ubr   = winreg.QueryValueEx(key, "UBR")[0]
                winreg.CloseKey(key)
                if build >= 22000:
                    name = name.replace("Windows 10", "Windows 11")
                return f"{name} (Build {build}.{ubr}) {platform.machine()}"
            except Exception:
                return f"Windows {platform.version()} ({platform.machine()})"
        else:
            # Linux: read /etc/os-release
            try:
                with open("/etc/os-release") as f:
                    info = {}
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            info[k] = v.strip('"')
                distro = info.get("PRETTY_NAME", platform.system())
            except Exception:
                distro = platform.system()
            return f"{distro} {platform.machine()}"
    except Exception:
        return platform.platform()


# ──────────────────────────────────────────────
# Generic Numbered Menu
# ──────────────────────────────────────────────

def numbered_menu(title: str, options: list[tuple[str, str]], default: int = 1) -> int:
    """
    Displays a numbered menu.
    options = [(label, description), ...]
    Returns the 0-based index of the choice.
    If title is empty, doesn't print a section separator.
    """
    if title:
        print_section(title)
    for i, (label, desc) in enumerate(options, 1):
        rprint(f"  [bold cyan]{i}.[/bold cyan]  [bold]{label}[/bold]")
        if desc:
            rprint(f"       [dim]{desc}[/dim]")
        console.print()

    while True:
        raw = Prompt.ask(
            "  [bold white]Choice / Choix[/bold white]",
            default=str(default),
            console=console,
        ).strip()
        try:
            idx = int(raw)
            if 1 <= idx <= len(options):
                return idx - 1
        except ValueError:
            pass
        rprint(f"  [red]Enter a number between 1 and {len(options)}.[/red]")


# ──────────────────────────────────────────────
# Final Confirmation (prompt to type confirmation word)
# ──────────────────────────────────────────────

def confirm_wipe(disk, method_name: str) -> bool:
    """
    Displays summary and prompts to type CONFIRM/CONFIRMER.
    Returns True if confirmed.
    """
    print_section(t("confirm_title"))

    # Windows volumes warning: only target disk drive letters
    drive_letters = getattr(disk, "drive_letters", []) or getattr(disk, "mountpoints", [])
    vol_warning = ""
    if drive_letters and sys.platform == "win32":
        letters_str = ", ".join(drive_letters)
        vol_warning = (
            f"\n\n[yellow]{t('confirm_vol_warning', letters=letters_str)}[/yellow]"
            f"\n[dim]{t('confirm_vol_close')}[/dim]"
            f"\n[dim]{t('confirm_vol_isolated')}[/dim]"
        )

    console.print(Panel(
        Text.from_markup(
            f"{t('confirm_line1')}\n\n"
            f"{t('confirm_disk', dev=disk.device, model=disk.model, serial=disk.serial)}\n"
            f"{t('confirm_size', size=disk.size_human)}\n"
            f"{t('confirm_method', method=method_name)}"
            f"{vol_warning}\n\n"
            f"{t('confirm_warn')}"
        ),
        border_style="bold red",
        padding=(1, 2),
    ))
    console.print()

    answer = Prompt.ask(
        f"  {t('confirm_prompt')}",
        default="",
        console=console,
    ).strip()

    if answer == t("confirm_word"):
        return True

    rprint(f"  {t('confirm_abort')}")
    console.print()
    return False


# ──────────────────────────────────────────────
# Ask if continuing with another disk
# ──────────────────────────────────────────────

def ask_another() -> bool:
    """Asks if the user wants to wipe another disk."""
    console.print()
    answer = Prompt.ask(
        f"  {t('session_another')}",
        default="n",
        console=console,
    ).strip().lower()
    return answer in ("o", "y", "oui", "yes")


# ──────────────────────────────────────────────
# Display list of disks
# ──────────────────────────────────────────────

from core.disk_linux import (
    DiskInfo, DISK_TYPE_HDD, DISK_TYPE_SSD, DISK_TYPE_NVME,
    ENC_NONE, ENC_LUKS, ENC_BITLOCKER, ENC_SED,
)
from rich.table import Table


def print_disk_table(disks: list) -> None:
    """Displays the table of detected disks."""
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="blue",
        show_lines=True,
        expand=False,
    )
    table.add_column(t("disk_col_num"),    style="bold", width=4,  justify="center")
    table.add_column(t("disk_col_dev"),    style="bold cyan", width=16)
    table.add_column(t("disk_col_model"),  width=30)
    table.add_column(t("disk_col_serial"), width=20)
    table.add_column(t("disk_col_type"),   width=16, justify="center")
    table.add_column(t("disk_col_size"),   width=12, justify="right")
    table.add_column(t("disk_col_enc"),    width=12, justify="center")

    for i, disk in enumerate(disks, 1):
        # Type
        type_map = {
            DISK_TYPE_HDD:  f"[yellow]{t('disk_type_hdd')}[/yellow]",
            DISK_TYPE_SSD:  f"[cyan]{t('disk_type_ssd')}[/cyan]",
            DISK_TYPE_NVME: f"[bright_cyan]{t('disk_type_nvme')}[/bright_cyan]",
        }
        dtype = type_map.get(disk.disk_type, t("disk_type_unknown"))

        # Encryption
        enc_map = {
            ENC_LUKS:      "[green]LUKS[/green]",
            ENC_BITLOCKER: "[green]BitLocker[/green]",
            ENC_SED:       "[green]SED[/green]",
            ENC_NONE:      "[dim]—[/dim]",
        }
        enc = enc_map.get(disk.encryption, "[dim]—[/dim]")

        # Number with warning if system disk
        num_str = f"[bold]{i}[/bold]"
        dev_str = disk.device
        if disk.is_system:
            num_str += f"\n{t('disk_system_warning')}"
            dev_str  = f"[bold red]{disk.device}[/bold red]"

        table.add_row(
            num_str,
            dev_str,
            disk.model,
            disk.serial,
            dtype,
            disk.size_human,
            enc,
        )

    console.print(table)


def select_disk(disks: list) -> DiskInfo:
    """
    Displays the disk table and prompts user to pick a disk.
    Blocks if the system disk is selected.
    Returns the chosen DiskInfo.
    """
    while True:
        raw = Prompt.ask(
            f"\n  [bold white]{t('disk_select')} (1-{len(disks)})[/bold white]",
            console=console,
        ).strip()

        try:
            idx = int(raw) - 1
            if not (0 <= idx < len(disks)):
                raise ValueError
        except ValueError:
            rprint(f"  {t('disk_invalid_choice', max=len(disks))}")
            continue

        disk = disks[idx]

        if disk.is_system:
            console.print()
            rprint(t("disk_system_blocked", dev=disk.device))
            console.print()
            continue

        return disk
