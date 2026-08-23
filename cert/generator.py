"""
SecureWipe — cert/generator.py
PDF Sanitization Audit Certificate Generation.

Features:
  - SecureWipe logo / header styling
  - Comprehensive sanitization execution metadata
  - Diagonal watermark "SECUREWIPE — CERTIFIED"
  - Embedded SHA-256 verification QR code
  - Sequential report identifier
  - Parallel raw .log output creation
"""


import hashlib
import json
import os
import sys
import re
import platform
import tempfile
from datetime import datetime
from pathlib import Path

# ──────────────────────────────────────────────
# SecureWipe Color Palette
# ──────────────────────────────────────────────

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm, mm
    from reportlab.lib.colors import (
        HexColor, white, black, Color,
        lightgrey, grey, darkblue,
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        HRFlowable, KeepTogether,
    )
    from reportlab.pdfgen import canvas
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
    import qrcode
    import qrcode.image.pil

    COLOR_DARK_BG   = HexColor("#0a0e1a")
    COLOR_BLUE      = HexColor("#2a6abf")
    COLOR_CYAN      = HexColor("#4a90d9")
    COLOR_RED       = HexColor("#e74c3c")
    COLOR_GREEN     = HexColor("#27ae60")
    COLOR_LIGHT_BG  = HexColor("#f0f4f8")
    COLOR_MID_GREY  = HexColor("#8090a0")
    COLOR_TEXT      = HexColor("#1a1a2e")
    COLOR_SECTION   = HexColor("#1a3a6a")
    COLOR_ROW_ALT   = HexColor("#e8f0f8")
    COLOR_BORDER    = HexColor("#2a5a9a")
except (ImportError, Exception):
    A4 = (595.27, 841.89)
    cm = 28.3465
    mm = 2.83465
    white = black = lightgrey = grey = darkblue = None
    COLOR_DARK_BG = COLOR_BLUE = COLOR_CYAN = COLOR_RED = COLOR_GREEN = None
    COLOR_LIGHT_BG = COLOR_MID_GREY = COLOR_TEXT = COLOR_SECTION = COLOR_ROW_ALT = COLOR_BORDER = None

from core.i18n import t
from core.wipe_engine import WipeResult, WipeStatus, WipeMode


# ──────────────────────────────────────────────
# Sequential Report ID Generation
# ──────────────────────────────────────────────

def _get_next_report_id(script_dir: Path) -> str:
    """
    Generates a unique timestamp-based identifier: YYYYMMDDHHmm
    Example: 202603281902 — portable across platforms.
    """
    return datetime.now().strftime("%Y%m%d%H%M")


# ──────────────────────────────────────────────
# QR Code Generation
# ──────────────────────────────────────────────

def _make_qr_image(content: str, tmp_dir: Path) -> Path:
    """Generates a local PNG QR code and returns its filesystem path."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=4,
        border=2,
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    path = tmp_dir / "qr_cert.png"
    img.save(str(path))
    return path


# ──────────────────────────────────────────────
# Watermark + Page Header/Footer (Canvas Overlay)
# ──────────────────────────────────────────────

class _CertCanvas(canvas.Canvas):
    """Custom Canvas with diagonal watermark, header, and footer on each page."""

    def __init__(self, filename, report_id: str, **kwargs):
        super().__init__(filename, **kwargs)
        self._report_id = report_id
        self._page_num  = 0

    def showPage(self):
        self._page_num += 1
        self._draw_watermark()
        self._draw_header()
        self._draw_footer()
        super().showPage()

    def save(self):
        self._page_num += 1
        self._draw_watermark()
        self._draw_header()
        self._draw_footer()
        super().save()

    def _draw_watermark(self):
        """Semi-transparent diagonal watermark."""
        self.saveState()
        self.setFont("Helvetica-Bold", 42)
        self.setFillColor(Color(0.7, 0.8, 0.9, alpha=0.08))
        w, h = A4
        self.translate(w / 2, h / 2)
        self.rotate(45)
        text = "SECUREWIPE — CERTIFIED — DO NOT FALSIFY"
        self.drawCentredString(0, 30, text)
        self.drawCentredString(0, -30, text)
        self.drawCentredString(0, 90, text)
        self.drawCentredString(0, -90, text)
        self.restoreState()

    def _draw_header(self):
        """Dark header bar at top of each page."""
        self.saveState()
        w, h = A4
        # Bande de fond
        self.setFillColor(COLOR_DARK_BG)
        self.rect(0, h - 1.5*cm, w, 1.5*cm, fill=1, stroke=0)
        # Texte gauche
        self.setFillColor(COLOR_CYAN)
        self.setFont("Helvetica-Bold", 9)
        self.drawString(1*cm, h - 1.0*cm, "SecureWipe")
        # Texte droite
        self.setFillColor(white)
        self.setFont("Helvetica", 7)
        self.drawRightString(w - 1*cm, h - 1.0*cm,
            f"{t('report_title_main')}  |  {self._report_id}")
        self.restoreState()

    def _draw_footer(self):
        """Footer with page numbers and horizontal separator line."""
        self.saveState()
        w, h = A4
        # Ligne
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.5)
        self.line(1*cm, 1.2*cm, w - 1*cm, 1.2*cm)
        # Texte
        self.setFillColor(COLOR_MID_GREY)
        self.setFont("Helvetica", 7)
        self.drawString(1*cm, 0.7*cm,
            f"{self._report_id}  |  SecureWipe v2.0.0  |  GPL v3")
        self.drawRightString(w - 1*cm, 0.7*cm,
            f"Page {self._page_num}")
        self.restoreState()


# ──────────────────────────────────────────────
# PDF Content Assembly
# ──────────────────────────────────────────────

def _styles():
    styles = getSampleStyleSheet()
    base = dict(fontName="Helvetica", textColor=COLOR_TEXT, leading=14)

    return {
        "title": ParagraphStyle("title",
            fontName="Helvetica-Bold", fontSize=18,
            textColor=white, alignment=TA_CENTER, leading=22,
        ),
        "subtitle": ParagraphStyle("subtitle",
            fontName="Helvetica", fontSize=9,
            textColor=COLOR_CYAN, alignment=TA_CENTER, leading=12,
        ),
        "section": ParagraphStyle("section",
            fontName="Helvetica-Bold", fontSize=10,
            textColor=white, alignment=TA_LEFT, leading=14,
        ),
        "label": ParagraphStyle("label",
            fontName="Helvetica-Bold", fontSize=8.5,
            textColor=COLOR_SECTION, alignment=TA_LEFT, leading=12,
        ),
        "value": ParagraphStyle("value",
            fontName="Helvetica", fontSize=8.5,
            textColor=COLOR_TEXT, alignment=TA_LEFT, leading=12,
        ),
        "mono": ParagraphStyle("mono",
            fontName="Courier", fontSize=7.5,
            textColor=COLOR_TEXT, alignment=TA_LEFT, leading=11,
            wordWrap="CJK",
        ),
        "result_ok": ParagraphStyle("result_ok",
            fontName="Helvetica-Bold", fontSize=13,
            textColor=COLOR_GREEN, alignment=TA_CENTER, leading=18,
        ),
        "result_fail": ParagraphStyle("result_fail",
            fontName="Helvetica-Bold", fontSize=13,
            textColor=COLOR_RED, alignment=TA_CENTER, leading=18,
        ),
        "warn": ParagraphStyle("warn",
            fontName="Helvetica-Oblique", fontSize=8,
            textColor=COLOR_RED, alignment=TA_LEFT, leading=11,
        ),
        "footer_note": ParagraphStyle("footer_note",
            fontName="Helvetica", fontSize=7,
            textColor=COLOR_MID_GREY, alignment=TA_CENTER, leading=10,
        ),
    }


def _section_header(title: str, st: dict):
    """Returns a styled table for section headers."""
    tbl = Table([[Paragraph(f"  {title}", st["section"])]], colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_SECTION),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("ROUNDEDCORNERS", [3]),
    ]))
    return tbl


import html

def _info_table(rows: list[tuple], st: dict):
    """
    Two-column label/value table.
    rows = [(label, value), ...]
    """
    data = [
        [Paragraph(html.escape(str(lbl)), st["label"]), Paragraph(html.escape(str(val)), st["value"])]
        for lbl, val in rows
    ]
    tbl = Table(data, colWidths=[5.5*cm, 11.5*cm])
    style = [
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [white, COLOR_ROW_ALT]),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, COLOR_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    tbl.setStyle(TableStyle(style))
    return tbl


# ──────────────────────────────────────────────
# Raw Report Data (for SHA-256 + Log)
# ──────────────────────────────────────────────

def _build_report_data(
    report_id: str,
    operator: dict,
    disk,
    result: WipeResult,
    mode_label: str,
    verify_pct: int,
) -> dict:
    """Builds raw report data dictionary (JSON serializable)."""
    ts = operator["datetime"]
    tz = "UTC" if not hasattr(ts, "astimezone") else \
        ts.astimezone().strftime("%Z")

    res_str = t("report_success") if result.status == WipeStatus.SUCCESS \
              else t("report_failure")

    verify_str = f"{verify_pct}%" if result.verify_ok is not None else "N/A"
    if result.verify_ok is True:
        verify_str += f" — {t('report_success')}"
    elif result.verify_ok is False:
        verify_str += f" — {t('report_failure')}"

    dur = int(result.duration_sec)
    duration_str = f"{dur // 3600}h {(dur % 3600) // 60}min {dur % 60}s"

    return {
        t("report_id"):          report_id,
        t("report_date"):        ts.strftime("%Y-%m-%d  %H:%M:%S") + f"  ({tz})",
        t("report_operator"):    operator["name"],
        t("report_machine"):     operator["machine"],
        t("report_os"):          operator["os"],
        t("report_device"):      disk.device,
        t("report_model"):       disk.model,
        t("report_serial"):      disk.serial,
        t("report_type"):        disk.disk_type.upper(),
        t("report_size"):        f"{disk.size_human}  ({disk.size_bytes:,} B)",
        t("report_encryption"):  disk.encryption.upper(),
        t("report_method"):      mode_label,
        t("report_standard"):    result.standard,
        t("report_passes"):      str(result.passes_done),
        t("report_verify_pct"):  verify_str,
        t("report_result"):      res_str,
        t("report_duration"):    duration_str,
        "Confidence Score":      f"{result.confidence_score}%",
        "HPA Status":            ("Detected (Unwiped)" if result.hpa_detected and not result.hpa_wiped else ("Detected & Wiped" if result.hpa_wiped else "None Detected")),
    }


# ──────────────────────────────────────────────
# Primary PDF Generation
# ──────────────────────────────────────────────

def generate_certificate(
    operator: dict,
    disk,
    result: WipeResult,
    mode_label: str,
    verify_pct: int,
    output_dir: Path,
    script_dir: Path,
) -> tuple[Path, Path]:
    """
    Generates the PDF Certificate and raw TXT log file.
    Returns (pdf_path, txt_path).
    """
    report_id  = _get_next_report_id(script_dir)
    ts         = operator["datetime"]
    ts_str     = ts.strftime("%Y-%m-%d_%H-%M-%S")
    serial_safe = re.sub(r'[^\w\-]', '_', disk.serial)

    pdf_name = f"SW-{ts_str}_{serial_safe}.pdf"
    txt_name = f"SW-{ts_str}_{serial_safe}.log"
    pdf_path = output_dir / pdf_name
    txt_path = output_dir / txt_name

    # ── Report Data ──
    report_data = _build_report_data(report_id, operator, disk, result, mode_label, verify_pct)

    # ── SHA-256 Digest ──
    content_str = json.dumps(report_data, ensure_ascii=False, sort_keys=True)
    sha256 = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
    report_data[t("report_sha256")] = sha256

    # ── Blockchain Pre-Anchoring ──
    from trust.blockchain import prepare_block, anchor
    block_info = prepare_block({
        "report_id": report_id,
        "device": disk.device,
        "serial": disk.serial,
        "method": mode_label,
        "confidence_score": result.confidence_score,
        "timestamp": ts.timestamp(),
        "sha256": sha256,
    })
    block_hash = block_info["block_hash"]
    report_data["Blockchain Block Hash"] = block_hash

    # ── QR code pointing to Certificate Verification page ──
    base_url = os.environ.get("VERIFY_BASE_URL", "https://secure-wipe-psi.vercel.app")
    verify_url = f"{base_url}/verify?hash={block_hash}"
    tmp_dir = Path(tempfile.mkdtemp())
    qr_path = _make_qr_image(verify_url, tmp_dir)

    # ── Styles ──
    st = _styles()

    # ── PDF Elements Construction ──
    story = []
    w_page, h_page = A4
    margin = 1.5 * cm

    # ── Title Block ──
    result_ok = result.status == WipeStatus.SUCCESS

    # Logo Path
    logo_path = script_dir / "cert" / "template" / "logo.png"

    from reportlab.platypus import Image as RLImage

    # Logo + Title side-by-side
    logo_loaded = False
    if logo_path.exists():
        try:
            logo_img = RLImage(str(logo_path), width=3.2*cm, height=3.2*cm)
            title_cell = [
                Spacer(1, 0.3*cm),
                Paragraph(t("report_title_main"), st["title"]),
                Spacer(1, 0.15*cm),
                Paragraph("ANSSI · NIST SP 800-88 Rev.2 · GPL v3", st["subtitle"]),
                Spacer(1, 0.3*cm),
            ]
            header_data = [[logo_img, title_cell]]
            header_tbl = Table(header_data, colWidths=[3.6*cm, 13.4*cm])
            header_tbl.setStyle(TableStyle([
                ("BACKGROUND",    (0, 0), (-1, -1), COLOR_DARK_BG),
                ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN",         (0, 0), (0, -1),  "CENTER"),
                ("TOPPADDING",    (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING",   (0, 0), (0, -1),  4),
                ("RIGHTPADDING",  (1, 0), (1, -1),  8),
            ]))
            story.append(header_tbl)
            logo_loaded = True
        except Exception:
            logo_loaded = False

    if not logo_loaded:
        title_data = [[Paragraph(t("report_title_main"), st["title"])]]

        title_tbl = Table(title_data, colWidths=[17*cm])
        title_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), COLOR_DARK_BG),
            ("TOPPADDING",    (0, 0), (-1, -1), 14),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(title_tbl)
        sub_data = [[Paragraph("ANSSI · NIST SP 800-88 Rev.2 · GPL v3", st["subtitle"])]]
        sub_tbl = Table(sub_data, colWidths=[17*cm])
        sub_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), COLOR_DARK_BG),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(sub_tbl)

    story.append(Spacer(1, 0.2*cm))

    # ── Global Result ──
    res_style = st["result_ok"] if result_ok else st["result_fail"]
    res_text  = f"✓  {t('report_success')}" if result_ok else f"✗  {t('report_failure')}"
    res_color = COLOR_GREEN if result_ok else COLOR_RED

    res_data = [[Paragraph(res_text, res_style)]]
    res_tbl  = Table(res_data, colWidths=[17*cm])
    res_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#eafaf1") if result_ok else HexColor("#fdedec")),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEABOVE",    (0, 0), (-1, 0), 2, res_color),
        ("LINEBELOW",    (0, -1), (-1, -1), 2, res_color),
    ]))
    story.append(res_tbl)
    story.append(Spacer(1, 0.2*cm))

    # ── CONTEXT Section ──
    story.append(_section_header(t("report_section_context"), st))
    story.append(Spacer(1, 0.08*cm))
    ctx_rows = [
        (t("report_id"),       report_data[t("report_id")]),
        (t("report_date"),     report_data[t("report_date")]),
        (t("report_operator"), report_data[t("report_operator")]),
        (t("report_machine"),  report_data[t("report_machine")]),
        (t("report_os"),       report_data[t("report_os")]),
    ]
    story.append(_info_table(ctx_rows, st))
    story.append(Spacer(1, 0.2*cm))

    # ── MEDIA / SUPPORT Section ──
    story.append(_section_header(t("report_section_support"), st))
    story.append(Spacer(1, 0.08*cm))
    sup_rows = [
        (t("report_device"),     report_data[t("report_device")]),
        (t("report_model"),      report_data[t("report_model")]),
        (t("report_serial"),     report_data[t("report_serial")]),
        (t("report_type"),       report_data[t("report_type")]),
        (t("report_size"),       report_data[t("report_size")]),
        (t("report_encryption"), report_data[t("report_encryption")]),
    ]
    story.append(_info_table(sup_rows, st))
    story.append(Spacer(1, 0.2*cm))

    # ── METHOD Section ──
    story.append(_section_header(t("report_section_method"), st))
    story.append(Spacer(1, 0.08*cm))
    meth_rows = [
        (t("report_method"),     report_data[t("report_method")]),
        (t("report_standard"),   report_data[t("report_standard")]),
        (t("report_passes"),     report_data[t("report_passes")]),
        (t("report_verify_pct"), report_data[t("report_verify_pct")]),
        (t("report_result"),     report_data[t("report_result")]),
        (t("report_duration"),   report_data[t("report_duration")]),
    ]
    story.append(_info_table(meth_rows, st))
    story.append(Spacer(1, 0.2*cm))

    # ── INTEGRITY Section + QR Code ──
    story.append(_section_header(t("report_section_integrity"), st))
    story.append(Spacer(1, 0.08*cm))

    sha_para = Paragraph(
        f"<b>{t('report_sha256')} :</b>",
        st["label"]
    )
    sha_val  = Paragraph(f'<font name="Courier" size="7">{sha256}</font>', st["value"])
    
    hash_para = Paragraph("<b>Blockchain Block Hash :</b>", st["label"])
    hash_val = Paragraph(f'<font name="Courier" size="6.5">{block_hash}</font>', st["value"])
    
    score_para = Paragraph(f"<b>Wipe Confidence Score : {result.confidence_score}%</b>", st["label"])
    
    note_para = Paragraph(t("cert_qr_note"), st["footer_note"])

    from reportlab.platypus import Image as RLImage
    qr_img = RLImage(str(qr_path), width=3*cm, height=3*cm)

    integ_data = [[
        [sha_para, Spacer(1, 0.1*cm), sha_val, Spacer(1, 0.15*cm), hash_para, Spacer(1, 0.1*cm), hash_val, Spacer(1, 0.15*cm), score_para, Spacer(1, 0.2*cm), note_para],
        qr_img,
    ]]
    integ_tbl = Table(integ_data, colWidths=[13*cm, 4*cm])
    integ_tbl.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("BACKGROUND",    (0, 0), (-1, -1), COLOR_LIGHT_BG),
        ("LINEBELOW",     (0, -1), (-1, -1), 0.5, COLOR_BORDER),
    ]))
    story.append(integ_tbl)
    story.append(Spacer(1, 0.2*cm))

    # ── Footer Certification Note ──
    cert_text = t("report_certified")
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(cert_text, st["footer_note"]))
    story.append(Paragraph(
        f"Generated by SecureWipe v2.0.0 — {ts.strftime('%Y-%m-%d %H:%M:%S')}",
        st["footer_note"],
    ))

    # ── Render PDF ──
    def make_canvas(filename, **kw):
        return _CertCanvas(filename, report_id=report_id, **kw)

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=2.2*cm,
        bottomMargin=1.8*cm,
        title=f"SecureWipe — {t('report_title_main')} — {report_id}",
        author="SecureWipe Engine",
        subject=f"Secure Sanitization {disk.serial}",
        creator="SecureWipe v2.0.0",
    )
    doc.build(story, canvasmaker=make_canvas)

    # ── Blockchain Anchor ──
    try:
        anchor(pdf_path, block_info)
    except Exception as e:
        print(f"Blockchain anchoring warning: {e}")

    # ── Temp Cleanup ──
    try:
        import shutil
        shutil.rmtree(str(tmp_dir))
    except Exception:
        pass

    # ── Log brut TXT ──
    _write_log_txt(txt_path, report_data, sha256, result)

    return pdf_path, txt_path


# ──────────────────────────────────────────────
# Raw TXT Log
# ──────────────────────────────────────────────

def _write_log_txt(
    path: Path,
    report_data: dict,
    sha256: str,
    result: WipeResult,
) -> None:
    """Writes raw sanitization log in plaintext format."""
    separator = "=" * 72

    lines = [
        separator,
        "  SECUREWIPE — SANITIZATION AUDIT LOG",
        separator,
        "",
    ]

    for key, val in report_data.items():
        if key == t("report_sha256"):
            continue
        lines.append(f"  {key:<30} : {val}")

    lines += [
        "",
        separator,
        f"  Certificate SHA-256: {sha256}",
        separator,
        "",
    ]

    if result.error_msg:
        lines.append(f"  ERROR: {result.error_msg}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")

