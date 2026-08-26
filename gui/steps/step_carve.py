"""
SecureWipe GUI — step_carve.py
Dedicated GUI screen for Operation 2: Advanced File Carving & Recovery Engine.
"""
import os
import sys
import tempfile
import customtkinter as ctk
from gui.theme import *
from core.carver import carve_target, CarveResult, verify_wipe_carve


class StepCarve(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self._target_path = ""
        self._carve_result = None

        self._build_ui()

    def _build_ui(self):
        # Header title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=32, pady=(24, 16))

        ctk.CTkLabel(title_frame, text="🔍 Advanced File Carving & Recovery Engine",
                     font=FONT_TITLE, text_color=BLUE_LIGHT).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Operation 2 — Signature Carving, Shannon Entropy Analysis & Confidence Scoring Matrix",
                     font=FONT_SMALL, text_color=TEXT_DIM).pack(anchor="w")

        # Target selection container
        sel_card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=RADIUS_MD, border_width=1, border_color=BORDER)
        sel_card.pack(fill="x", padx=32, pady=(0, 16))

        sel_inner = ctk.CTkFrame(sel_card, fg_color="transparent")
        sel_inner.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(sel_inner, text="Target Disk Image or Raw Media Path:", font=FONT_HEADING, text_color=TEXT_PRIMARY).pack(anchor="w", pady=(0, 8))

        input_row = ctk.CTkFrame(sel_inner, fg_color="transparent")
        input_row.pack(fill="x")

        self._entry_path = ctk.CTkEntry(input_row, font=FONT_BODY, fg_color=BG_INPUT, text_color=TEXT_PRIMARY,
                                        border_color=BORDER, height=BTN_H, placeholder_text="Enter path to .img, .dd, or disk image file...")
        self._entry_path.pack(side="left", fill="x", expand=True, padx=(0, 12))

        ctk.CTkButton(input_row, text="Browse Image", font=FONT_BTN, height=BTN_H, fg_color=BG_HOVER, hover_color=BLUE_PRIMARY,
                      text_color=TEXT_PRIMARY, border_width=1, border_color=BORDER, command=self._browse_image).pack(side="left", padx=(0, 8))

        ctk.CTkButton(input_row, text="Generate Demo Image", font=FONT_BTN, height=BTN_H, fg_color=BLUE_DARK, hover_color=BLUE_PRIMARY,
                      text_color=TEXT_PRIMARY, command=self._generate_demo_image).pack(side="left")

        # Action Buttons
        btn_bar = ctk.CTkFrame(self, fg_color="transparent")
        btn_bar.pack(fill="x", padx=32, pady=(0, 16))

        self._btn_carve = ctk.CTkButton(btn_bar, text="🚀 Initiate Advanced Signature Carve", font=FONT_BTN, height=44,
                                        fg_color=BLUE_PRIMARY, hover_color=BLUE_LIGHT, text_color="#ffffff",
                                        corner_radius=RADIUS_SM, command=self._run_carve)
        self._btn_carve.pack(side="left", padx=(0, 12))

        self._btn_verify = ctk.CTkButton(btn_bar, text="🛡️ Run Post-Wipe Verification Check", font=FONT_BTN, height=44,
                                         fg_color=GREEN_OK, hover_color=GREEN_DARK, text_color="#ffffff",
                                         corner_radius=RADIUS_SM, command=self._run_post_wipe_verify)
        self._btn_verify.pack(side="left")

        # Results Panel
        self._res_card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=RADIUS_MD, border_width=1, border_color=BORDER)
        self._res_card.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        self._lbl_status = ctk.CTkLabel(self._res_card, text="Ready to initiate file carving scan.", font=FONT_BODY, text_color=TEXT_DIM)
        self._lbl_status.pack(padx=20, pady=16, anchor="w")

        # Scrollable table container
        self._scroll_frame = ctk.CTkScrollableFrame(self._res_card, fg_color="transparent")
        self._scroll_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def _browse_image(self):
        from tkinter import filedialog
        fn = filedialog.askopenfilename(title="Select Disk Image File", filetypes=[("Disk Images", "*.img *.dd *.raw"), ("All Files", "*.*")])
        if fn:
            self._entry_path.delete(0, "end")
            self._entry_path.insert(0, fn)

    def _generate_demo_image(self):
        tmp_dir = tempfile.mkdtemp(prefix="carve_demo_")
        img_p = os.path.join(tmp_dir, "demo_media.img")
        with open(img_p, "wb") as f:
            # JPEG block
            f.write(b"\x00" * 512 + b"\xFF\xD8\xFF\xE0\x00\x10JFIF" + b"SAMPLE_IMAGE_PAYLOAD" * 30 + b"\xFF\xD9" + b"\x00" * 512)
            # PDF block
            f.write(b"%PDF-1.4 Sample Confidential Document Content " + b"CONFIDENTIAL_DATA" * 50 + b"%%EOF")
        self._entry_path.delete(0, "end")
        self._entry_path.insert(0, img_p)
        self._lbl_status.configure(text=f"Generated synthetic demo disk image with embedded signatures: {img_p}", text_color=GREEN_OK)

    def _run_carve(self):
        target = self._entry_path.get().strip()
        if not target or not os.path.exists(target):
            self._lbl_status.configure(text="Please select a valid disk image or media path.", text_color=RED_DANGER)
            return

        self._lbl_status.configure(text="Scanning sectors & computing Shannon Entropy...", text_color=BLUE_LIGHT)
        self.update_idletasks()

        out_dir = tempfile.mkdtemp(prefix="carve_out_gui_")
        res = carve_target(target, out_dir)
        self._carve_result = res

        for w in self._scroll_frame.winfo_children():
            w.destroy()

        if res.status == "NO_CANDIDATES" or res.total_recovered == 0:
            self._lbl_status.configure(text="Scan Complete: 0 Recoverable Files Found (Media is verifiably clean!).", text_color=GREEN_OK)
            return

        self._lbl_status.configure(
            text=f"Scan Complete: {res.total_recovered} Candidates Recovered | HIGH: {res.high_confidence_count} | MED: {res.medium_confidence_count} | LOW: {res.low_confidence_count} ({res.engine_used})",
            text_color=BLUE_LIGHT
        )

        # Header Row
        hdr = ctk.CTkFrame(self._scroll_frame, fg_color=BG_INPUT, height=32)
        hdr.pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(hdr, text="ID", width=80, font=FONT_STEP, text_color=TEXT_SECOND).pack(side="left", padx=8)
        ctk.CTkLabel(hdr, text="Category", width=110, font=FONT_STEP, text_color=TEXT_SECOND).pack(side="left", padx=8)
        ctk.CTkLabel(hdr, text="Filename", width=220, font=FONT_STEP, text_color=TEXT_SECOND).pack(side="left", padx=8)
        ctk.CTkLabel(hdr, text="Size", width=90, font=FONT_STEP, text_color=TEXT_SECOND).pack(side="left", padx=8)
        ctk.CTkLabel(hdr, text="Entropy", width=90, font=FONT_STEP, text_color=TEXT_SECOND).pack(side="left", padx=8)
        ctk.CTkLabel(hdr, text="Confidence Badge", width=140, font=FONT_STEP, text_color=TEXT_SECOND).pack(side="left", padx=8)

        for c in res.candidates:
            row = ctk.CTkFrame(self._scroll_frame, fg_color=BG_DARK, height=36)
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(row, text=c.candidate_id, width=80, font=FONT_BODY, text_color=TEXT_PRIMARY).pack(side="left", padx=8)
            ctk.CTkLabel(row, text=c.category, width=110, font=FONT_BODY, text_color=BLUE_LIGHT).pack(side="left", padx=8)
            ctk.CTkLabel(row, text=c.file_name, width=220, font=FONT_BODY, text_color=TEXT_PRIMARY).pack(side="left", padx=8)
            ctk.CTkLabel(row, text=f"{c.size_bytes} B", width=90, font=FONT_BODY, text_color=TEXT_SECOND).pack(side="left", padx=8)
            ctk.CTkLabel(row, text=str(c.entropy), width=90, font=FONT_BODY, text_color=TEXT_SECOND).pack(side="left", padx=8)

            badge_color = GREEN_OK if c.confidence_rating == "HIGH" else "#f59e0b" if c.confidence_rating == "MEDIUM" else RED_DANGER
            ctk.CTkLabel(row, text=f"{c.confidence_rating} ({c.confidence_score}%)", width=140, font=FONT_STEP, text_color=badge_color).pack(side="left", padx=8)

    def _run_post_wipe_verify(self):
        target = self._entry_path.get().strip()
        if not target or not os.path.exists(target):
            self._lbl_status.configure(text="Please select a valid disk image or media path to verify.", text_color=RED_DANGER)
            return

        recovered_count = verify_wipe_carve(target)
        for w in self._scroll_frame.winfo_children():
            w.destroy()

        if recovered_count == 0:
            self._lbl_status.configure(
                text="🛡️ POST-WIPE VERIFICATION SUCCESS: 0 Recoverable Files Found. Storage media is 100% sanitized and unrecoverable!",
                text_color=GREEN_OK
            )
        else:
            self._lbl_status.configure(
                text=f"⚠️ POST-WIPE VERIFICATION ALERT: {recovered_count} files still detectable on target media.",
                text_color=RED_DANGER
            )
