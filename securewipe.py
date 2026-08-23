#!/usr/bin/env python3
"""
SecureWipe v2.0.0
Open source secure data sanitization utility for storage media.
Compliant with ANSSI Level 1/2 and NIST SP 800-88 Rev.2.

License : GPL v3
Author  : Grujowmi <grujowmi@proton.me>
Usage   :
  Linux   : sudo python3 securewipe.py
  Test    : sudo python3 securewipe.py --test-disk /tmp/testdisk.img
  Mock    : sudo python3 securewipe.py --mock
  Windows : python securewipe.py (Run as Administrator)
"""

import os
import sys
import platform
import argparse
from pathlib import Path

# Add script directory to Python sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ──────────────────────────────────────────────
# SecureWipe Module Imports
# ──────────────────────────────────────────────

from core.i18n  import select_language, t
from core.ui    import (
    check_privileges, print_banner, print_section,
    prompt_operator, print_disk_table, select_disk,
    confirm_wipe, ask_another,
)
from core.crypto_detect import analyse_disk_crypto, crypto_summary
from core.wipe_engine   import run_wipe, select_wipe_mode, WipeMode, WipeStatus
from cert.generator     import generate_certificate

from rich import print as rprint
from rich.prompt import Prompt
from rich.console import Console

console = Console()

IS_WINDOWS = sys.platform == "win32"
IS_LINUX   = sys.platform != "win32"


# ──────────────────────────────────────────────
# Disk Module OS Resolver
# ──────────────────────────────────────────────

def _get_disk_module():
    if IS_WINDOWS:
        from core import disk_windows as dm
    else:
        from core import disk_linux as dm
    return dm


# ──────────────────────────────────────────────
# Output Directory Selector for Certificates
# ──────────────────────────────────────────────

def _prompt_output_dir() -> Path:
    print_section(t("cert_title"))
    raw = Prompt.ask(
        f"  {t('cert_output_prompt')} {t('cert_output_default')}",
        default="",
        console=console,
    ).strip()
    if not raw:
        return SCRIPT_DIR
    p = Path(raw)
    try:
        p.mkdir(parents=True, exist_ok=True)
        return p
    except Exception as e:
        rprint(f"  [yellow]⚠ Invalid folder ({e}) — fallback to script directory.[/yellow]")
        return SCRIPT_DIR


# ──────────────────────────────────────────────
# Single Disk Sanitization Flow
# ──────────────────────────────────────────────

def _wipe_one_disk(operator: dict, dm, test_disk_path: str = None) -> bool:
    """
    Executes disk sanitization workflow:
      detection → selection → crypto analysis → mode → confirmation → wipe → certificate
    Returns True if completed without fatal error.
    """
    from pathlib import Path as _Path

    # ── Disk Detection ──
    print_section(t("disk_title"))
    rprint(f"  [dim]{t('disk_scanning')}[/dim]")
    console.print()

    # Test mode: inject image file as virtual disk
    if test_disk_path:
        p = _Path(test_disk_path)
        if not p.exists():
            rprint(f"  [bold red]File not found: {test_disk_path}[/bold red]")
            return False
        import os as _os
        from core.disk_linux import DiskInfo, DISK_TYPE_HDD, ENC_NONE, _bytes_to_human
        size = p.stat().st_size
        disks = [DiskInfo(
            device=str(p), name=p.name,
            model="[TEST] Image File",
            serial="TEST-0001",
            disk_type=DISK_TYPE_HDD,
            size_bytes=size,
            size_human=_bytes_to_human(size),
            is_system=False,
            encryption=ENC_NONE,
            transport="test",
            vendor="SecureWipe", firmware="",
            mountpoints=[],
        )]
    else:
        disks = dm.list_disks()

    if not disks:
        rprint(f"  [yellow]{t('disk_none_found')}[/yellow]")
        if os.environ.get("SECUREWIPE_MOCK") == "1":
            rprint("  [dim](Mock mode active — SECUREWIPE_MOCK=1)[/dim]")
            disks = dm._mock_disks()
        else:
            return False

    print_disk_table(disks)

    # ── Disk Selection ──
    disk = select_disk(disks)

    # ── Crypto Analysis ──
    rprint(f"\n  [dim]Analyzing encryption...[/dim]")
    crypto_profile = analyse_disk_crypto(disk)

    for warn in crypto_profile.warnings:
        console.print()
        rprint(f"  [yellow]{warn}[/yellow]")

    # ── Wipe Mode Selection ──
    mode, custom_passes, verify_pct, mode_label = select_wipe_mode(disk, crypto_profile)

    # ── Final Confirmation ──
    confirmed = confirm_wipe(disk, mode_label)
    if not confirmed:
        return True   # Operator cancelled

    # ── Wipe Execution ──
    result = run_wipe(
        disk=disk,
        mode=mode,
        custom_passes=custom_passes,
        verify_pct=verify_pct,
        crypto_profile=crypto_profile,
    )

    # ── Certificate Generation ──
    console.print()
    output_dir = _prompt_output_dir()

    rprint(f"  [dim]{t('cert_generating')}[/dim]")
    try:
        pdf_path, txt_path = generate_certificate(
            operator=operator,
            disk=disk,
            result=result,
            mode_label=mode_label,
            verify_pct=verify_pct,
            output_dir=output_dir,
            script_dir=SCRIPT_DIR,
        )
        rprint(f"  {t('cert_success', path=pdf_path)}")
        rprint(f"  {t('cert_log_success', path=txt_path)}")
    except Exception as e:
        rprint(f"  [red]Certificate generation error: {e}[/red]")

    console.print()
    return result.status == WipeStatus.SUCCESS


# ──────────────────────────────────────────────
# OS Compatibility Check
# ──────────────────────────────────────────────

def _check_os():
    if sys.platform not in ("linux", "linux2", "win32", "darwin"):
        rprint(t("err_os_unsupported", os=sys.platform))
        sys.exit(1)
    if sys.platform == "darwin":
        rprint("[yellow]⚠ macOS is not officially supported. Use at your own risk.[/yellow]")


# ──────────────────────────────────────────────
# Entry Point & CLI Parsing
# ──────────────────────────────────────────────

def _parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="securewipe",
        description="SecureWipe — Secure Media Sanitization (ANSSI/NIST)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python3 securewipe.py
  sudo python3 securewipe.py --test-disk /tmp/testdisk.img
  sudo python3 securewipe.py --mock
        """
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Force terminal mode (no GUI).",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Force graphical interface mode (CustomTkinter).",
    )
    parser.add_argument(
        "--test-disk",
        metavar="FILE",
        help="Use an image file as a virtual disk (Linux/WSL test mode). "
             "Ex: sudo python3 securewipe.py --test-disk /tmp/testdisk.img",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Load mock disks for testing the UI (Windows and Linux).",
    )
    return parser.parse_args()


def _gui_available() -> bool:
    """Checks if CustomTkinter is available and a display environment exists."""
    try:
        import customtkinter
        if IS_LINUX and not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
            return False
        return True
    except ImportError:
        return False


def _ask_mode() -> str:
    """Prompts user to select GUI or CLI mode at startup."""
    console.print()
    rprint("  [bold cyan]SecureWipe v2.0.0[/bold cyan]")
    console.print()
    rprint("  [bold]1.[/bold]  Graphical Interface (GUI)")
    rprint("  [bold]2.[/bold]  Terminal Interface  (CLI)")
    console.print()
    from rich.prompt import Prompt
    choice = Prompt.ask("  Mode", choices=["1","2"], default="1").strip()
    return "gui" if choice == "1" else "cli"


def main():
    args = _parse_args()

    if args.test_disk:
        os.environ["SECUREWIPE_DEV"] = args.test_disk
    if args.mock:
        os.environ["SECUREWIPE_MOCK"] = "1"

    if getattr(args, "gui", False):
        mode = "gui"
    elif getattr(args, "cli", False):
        mode = "cli"
    elif _gui_available():
        mode = _ask_mode()
    else:
        mode = "cli"
        console.print()
        rprint("  [dim]GUI unavailable (CustomTkinter missing or no display) — falling back to terminal mode.[/dim]")

    if mode == "gui":
        from core.i18n import _detect_system_lang
        lang = _detect_system_lang()
        from gui.app import run_gui
        run_gui(lang=lang)
        return

    try:
        # 1. OS Check
        _check_os()

        # 2. Privilege Check
        if not args.mock and os.environ.get("SECUREWIPE_MOCK") != "1":
            check_privileges()

        # 3. Language Selection
        select_language()

        # 4. Banner
        print_banner()

        # 5. Operator Identification
        operator = prompt_operator()

        # 6. Disk Module Load
        dm = _get_disk_module()

        # 7. Multi-disk Sanitization Loop
        test_disk_path = getattr(args, "test_disk", None)
        while True:
            success = _wipe_one_disk(operator, dm, test_disk_path=test_disk_path)

            if not ask_another():
                break

        # 8. Session Complete
        console.print()
        rprint(f"  {t('session_goodbye')}")
        console.print()

    except KeyboardInterrupt:
        console.print()
        rprint("\n  [yellow]SecureWipe interrupted.[/yellow]")
        sys.exit(0)
    except SystemExit:
        raise
    except Exception as e:
        console.print()
        rprint(f"  [bold red]Unexpected error: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

