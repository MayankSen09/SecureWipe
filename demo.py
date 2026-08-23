"""
SecureWipe — demo.py
Script de démonstration bout-en-bout.
Exécute l'ensemble du pipeline en mode mock avec affichage Rich.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Config encodage Windows & PYTHONPATH
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

os.environ["SECUREWIPE_MOCK"] = "1"

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

console = Console()

def run_demo():
    console.print()
    console.print(Panel(
        "[bold cyan]🛡️ SecureWipe — End-to-End Demonstration[/bold cyan]\n"
        "[dim]Secure Data Wiping & Blockchain Verification[/dim]",
        border_style="cyan",
        padding=(1, 4),
    ))
    console.print()

    # STEP 1: Storage Discovery & HPA Check
    rprint("[bold yellow]STEP 1:[/bold yellow] Storage Device Discovery & HPA Analysis...")
    from core import disk_windows as dm
    from core import disk_linux as dl
    import random
    disks = dm._mock_disks()
    target_disk = disks[0]
    target_disk.serial = f"S5YXNX0T{random.randint(100000, 999999)}"

    # Check HPA
    target_disk.hpa_detected = dl.detect_hpa(target_disk.device)
    
    table = Table(title="Detected Asset", border_style="dim")
    table.add_column("Device", style="cyan")
    table.add_column("Model", style="white")
    table.add_column("Serial", style="yellow")
    table.add_column("Size", style="green")
    table.add_column("HPA Status", style="magenta")
    
    hpa_str = "Detected" if target_disk.hpa_detected else "None Detected"
    table.add_row(target_disk.device, target_disk.model, target_disk.serial, target_disk.size_human, hpa_str)
    console.print(table)
    console.print()

    # STEP 2: Sanitization Execution
    rprint("[bold yellow]STEP 2:[/bold yellow] Executing NIST SP 800-88 / ANSSI P1 Wipe...")
    from core import wipe_engine as we
    wipe_res = we.run_wipe(target_disk, we.WipeMode.ANSSI_P1, verify_pct=10)
    rprint(f"  [green]✓[/green] Sanitization Status: [bold green]{wipe_res.status.name}[/bold green]")
    rprint()

    # STEP 3: Confidence Score Engine
    rprint("[bold yellow]STEP 3:[/bold yellow] Computing Wipe Confidence Score...")
    rprint(f"  [cyan]▸[/cyan] Calculated Confidence Score: [bold green]{wipe_res.confidence_score}%[/bold green] / 100%")
    rprint()

    # STEP 4: Certificate Generation & Blockchain Pre-Anchoring
    rprint("[bold yellow]STEP 4:[/bold yellow] Generating Certificate & Blockchain Pre-Anchoring...")
    from cert import generator as cg
    op_info = {
        "name": "Audit Inspector",
        "machine": "Audit-Workstation-01",
        "os": f"SecureWipe OS ({sys.platform})",
        "datetime": datetime.now(),
    }
    pdf_path, txt_path = cg.generate_certificate(
        operator=op_info,
        disk=target_disk,
        result=wipe_res,
        mode_label="ANSSI Palier 1 (1-pass zeros)",
        verify_pct=10,
        output_dir=SCRIPT_DIR,
        script_dir=SCRIPT_DIR,
    )
    rprint(f"  [green]✓[/green] PDF Certificate Generated: [bold white]{pdf_path.name}[/bold white]")
    rprint()

    # STEP 5: Blockchain Ledger Integrity Verification
    rprint("[bold yellow]STEP 5:[/bold yellow] Verifying Blockchain Hash-Chain Integrity...")
    from trust import blockchain as bc
    valid, msg = bc.verify_chain()
    rprint(f"  [green]✓[/green] Ledger Verification: [bold green]{'VERIFIED & INTACT' if valid else 'TAMPER DETECTED'}[/bold green]")
    rprint(f"  [dim]{msg}[/dim]")
    rprint()

    # STEP 6: API Verification Check
    rprint("[bold yellow]STEP 6:[/bold yellow] Querying Local Verification API Ledger...")
    import json
    chain_file = SCRIPT_DIR / "trust" / "chain.json"
    latest_hash = None
    if chain_file.exists():
        with open(chain_file, "r", encoding="utf-8") as f:
            chain = json.load(f)
            if chain:
                latest = chain[-1]
                latest_hash = latest['block_hash']
                rprint(f"  [cyan]▸[/cyan] Anchored Asset S/N: [bold yellow]{latest.get('serial')}[/bold yellow]")
                rprint(f"  [cyan]▸[/cyan] Anchored Score    : [bold green]{latest.get('confidence_score')}%[/bold green]")
    console.print()

    # Show the hash prominently so it can be copy-pasted into the web portal
    if latest_hash:
        verify_url = f"http://localhost:8000/verify?hash={latest_hash}"
        console.print(Panel(
            f"[bold cyan]📋 BLOCKCHAIN BLOCK HASH (copy this to verify)[/bold cyan]\n\n"
            f"[bold white]{latest_hash}[/bold white]\n\n"
            f"[dim]Verify at: [underline]{verify_url}[/underline][/dim]\n"
            f"[dim]Or open http://localhost:8000 → paste hash → click Verify Hash[/dim]",
            border_style="cyan",
            padding=(1, 2),
            title="[bold]Hash Ready for Verification[/bold]",
        ))
        console.print()

    console.print(Panel(
        "[bold green]✨ SecureWipe Demonstration Complete![/bold green]\n"
        "[dim]Web portal: uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload[/dim]",
        border_style="green",
        padding=(1, 4),
    ))

if __name__ == "__main__":
    run_demo()
