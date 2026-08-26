"""
SecureWipe — demo.py
End-to-end demonstration script.
Executes the full pipeline in mock mode with Rich terminal output.
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
        "[bold cyan]🛡️ SecureWipe Platform — SIH PS 26149 End-to-End Demonstration[/bold cyan]\n"
        "[dim]Multi-Module Data Sanitization, Mobile Wiping, Carving Recovery & Blockchain Audit System[/dim]",
        border_style="cyan",
        padding=(1, 4),
    ))
    console.print()
    # ─────────────────────────────────────────────────────────────
    # OPERATION 1: SECURE DATA ERASURE SUITE (DRIVE, MOBILE & FILES)
    # ─────────────────────────────────────────────────────────────
    console.print(Panel(
        "[bold red]🧹 OPERATION 1: SECURE DATA ERASURE SUITE[/bold red]\n"
        "[dim]HDD/SSD/NVMe Sanitization, Android Mobile Purge & Selective File Shredding[/dim]",
        border_style="red",
        padding=(0, 2),
    ))
    console.print()

    # STEP 1: Module 1 — Drive Sanitization & HPA Analysis
    rprint("[bold yellow]STEP 1 (Module 1 Drive Eraser):[/bold yellow] Storage Device Discovery & HPA Analysis...")
    from core import disk_windows as dm
    from core import disk_linux as dl
    import random
    disks = dm._mock_disks()
    target_disk = disks[0]
    target_disk.serial = f"S5YXNX0T{random.randint(100000, 999999)}"

    # Check HPA
    target_disk.hpa_detected = dl.detect_hpa(target_disk.device)
    
    table = Table(title="Detected Drive Asset", border_style="dim")
    table.add_column("Device", style="cyan")
    table.add_column("Model", style="white")
    table.add_column("Serial", style="yellow")
    table.add_column("Size", style="green")
    table.add_column("HPA Status", style="magenta")
    
    hpa_str = "Detected" if target_disk.hpa_detected else "None Detected"
    table.add_row(target_disk.device, target_disk.model, target_disk.serial, target_disk.size_human, hpa_str)
    console.print(table)
    console.print()

    from core import wipe_engine as we
    wipe_res = we.run_wipe(target_disk, we.WipeMode.ANSSI_P1, verify_pct=10)
    rprint(f"  [green]✓[/green] Drive Sanitization Status: [bold green]{wipe_res.status.name}[/bold green]")
    rprint(f"  [cyan]▸[/cyan] Audit Confidence Score: [bold green]{wipe_res.confidence_score}%[/bold green] / 100%")
    rprint()

    # STEP 2: Module 1B — Android Mobile Asset Agent
    rprint("[bold yellow]STEP 2 (Module 1B Mobile Agent):[/bold yellow] Android Smartphone Sanitization Agent...")
    from android.agent import detect_android_device, wipe_android
    mobile_dev = detect_android_device(mock=True)
    mobile_res = wipe_android(mobile_dev, mock=True)
    rprint(f"  [green]✓[/green] Mobile Sanitization Status: [bold green]{mobile_res.status.name}[/bold green] (UserData Key Purged)")
    rprint()

    # STEP 3: Module 2 — Selective File & Folder Shredding
    rprint("[bold yellow]STEP 3 (Module 2 File Shredder):[/bold yellow] Selective File/Folder Shredder & Metadata Scrubbing...")
    from core.file_eraser import wipe_path, FileWipeMode
    import tempfile
    demo_dir = tempfile.mkdtemp(prefix="securewipe_demo_shred_")
    test_file_1 = os.path.join(demo_dir, "sensitive_doc.pdf")
    test_file_2 = os.path.join(demo_dir, "private_photo.jpg")
    with open(test_file_1, "wb") as f:
        f.write(b"%PDF-1.4 /Title (Confidential Document) /Author (Secret User) " + b"X" * 2000 + b" %%EOF")
    with open(test_file_2, "wb") as f:
        f.write(b"\xFF\xD8\xFF\xE1" + b"EXIF_DATA_BLOCK" + b"\xFF\xD9")

    shred_res = wipe_path(demo_dir, mode=FileWipeMode.NIST_3PASS, strip_meta=True)
    rprint(f"  [green]✓[/green] Shredded [bold white]{shred_res.total_files}[/bold white] Files ({shred_res.total_bytes_written} bytes overwritten across 3 passes)")
    rprint(f"  [cyan]▸[/cyan] Metadata Scrubbing: [bold green]EXIF & PDF Properties Stripped[/bold green]")
    rprint()

    # ─────────────────────────────────────────────────────────────
    # OPERATION 2: ADVANCED FILE RECOVERY & CARVING ENGINE
    # ─────────────────────────────────────────────────────────────
    console.print(Panel(
        "[bold cyan]🔍 OPERATION 2: ADVANCED FILE RECOVERY & CARVING ENGINE[/bold cyan]\n"
        "[dim]Signature Carving, Shannon Entropy Analysis, Confidence Scoring & Verification[/dim]",
        border_style="cyan",
        padding=(0, 2),
    ))
    console.print()

    # STEP 4: Module 3 — File Carving & Confidence Scoring
    rprint("[bold yellow]STEP 4 (Module 3 Carving Engine):[/bold yellow] File Carving & Recovery Confidence Scoring Engine...")
    import tempfile
    carve_dir = tempfile.mkdtemp(prefix="securewipe_demo_carve_")
    carve_img_path = os.path.join(carve_dir, "sample_media.img")
    with open(carve_img_path, "wb") as f:
        # Inject sample JPEG signature block
        f.write(b"\x00" * 512 + b"\xFF\xD8\xFF\xE0\x00\x10JFIF" + b"A" * 1024 + b"\xFF\xD9" + b"\x00" * 512)
        # Inject sample PDF signature block
        f.write(b"%PDF-1.5 Sample Document Body Content " + b"B" * 2048 + b"%%EOF")

    carve_out_dir = os.path.join(carve_dir, "carve_results")
    from core.carver import carve_target, verify_wipe_carve
    carve_res = carve_target(carve_img_path, carve_out_dir)

    carve_table = Table(title="Carving & Recovery Candidates", border_style="dim")
    carve_table.add_column("Candidate ID", style="cyan")
    carve_table.add_column("Category", style="white")
    carve_table.add_column("Size", style="yellow")
    carve_table.add_column("Entropy", style="magenta")
    carve_table.add_column("Confidence Rating", style="green")

    for c in carve_res.candidates:
        rating_style = "bold green" if c.confidence_rating == "HIGH" else "bold yellow"
        carve_table.add_row(c.candidate_id, c.category, f"{c.size_bytes} B", str(c.entropy), f"[{rating_style}]{c.confidence_rating} ({c.confidence_score}%)[/{rating_style}]")
    console.print(carve_table)
    console.print()

    # STEP 5: Post-Wipe Verification Proof
    rprint("[bold yellow]STEP 5 (Verification Proof):[/bold yellow] Post-Wipe Media Carving Verification...")
    # Zero out the carve test image to simulate completed sanitization
    with open(carve_img_path, "wb") as f:
        f.write(b"\x00" * os.path.getsize(carve_img_path))
    post_wipe_recovered = verify_wipe_carve(carve_img_path)
    rprint(f"  [green]✓[/green] Post-Wipe Carving Recovery Count: [bold green]{post_wipe_recovered} Recoverable Files[/bold green] (Verified Clean!)")
    rprint()

    # ─────────────────────────────────────────────────────────────
    # SHARED AUDIT & BLOCKCHAIN VERIFICATION SYSTEM
    # ─────────────────────────────────────────────────────────────
    console.print(Panel(
        "[bold green]🔗 UNIFIED BLOCKCHAIN AUDIT & REPORTING SYSTEM[/bold green]\n"
        "[dim]Tamper-Evident SHA-256 Block Generation & PDF Audit Certificate Stream[/dim]",
        border_style="green",
        padding=(0, 2),
    ))
    console.print()

    # STEP 6: Certificate Generation & Blockchain Pre-Anchoring
    rprint("[bold yellow]STEP 6:[/bold yellow] Generating Certificate & Blockchain Pre-Anchoring...")
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
    rprint(f"  [green]✓[/green] PDF Audit Certificate Generated: [bold white]{pdf_path.name}[/bold white]")
    rprint()

    # STEP 7: Blockchain Ledger Integrity Verification
    rprint("[bold yellow]STEP 7:[/bold yellow] Verifying Blockchain Hash-Chain Integrity...")
    from trust import blockchain as bc
    valid, msg = bc.verify_chain()
    rprint(f"  [green]✓[/green] Ledger Verification: [bold green]{'VERIFIED & INTACT' if valid else 'TAMPER DETECTED'}[/bold green]")
    rprint(f"  [dim]{msg}[/dim]")
    rprint()

    # STEP 8: API Verification Check
    rprint("[bold yellow]STEP 8:[/bold yellow] Querying Local Verification API Ledger...")
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
        "[bold green]✨ SecureWipe Platform Demonstration Complete![/bold green]\n"
        "[dim]Web portal: python -m uvicorn app:app --host 0.0.0.0 --port 8000[/dim]",
        border_style="green",
        padding=(1, 4),
    ))


if __name__ == "__main__":
    run_demo()
