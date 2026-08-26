"""SecureWipe GUI — Step 2: Disk Selection"""
import sys
import os
import re
import customtkinter as ctk
from gui.theme import *
from core.i18n import t

def _clean(txt):
    return re.sub(r"\[/?\w+\]", "", txt)

class Step2Disk(ctk.CTkFrame):
    def __init__(self, master, **kw):
        super().__init__(master, fg_color="transparent", **kw)
        self._disks = []
        self._selected = None
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text=_clean(t("disk_title")),
            font=FONT_TITLE, text_color=TEXT_PRIMARY).pack(pady=(28,4))

        # Toolbar: Refresh button
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=24, pady=(0,8))
        self._status_lbl = ctk.CTkLabel(toolbar, text=_clean(t("disk_scanning")),
            font=FONT_SMALL, text_color=TEXT_SECOND)
        self._status_lbl.pack(side="left")
        ctk.CTkButton(toolbar, text="↻  Refresh",
            font=FONT_SMALL, height=28, corner_radius=RADIUS_SM,
            fg_color="#ffffff", hover_color=BG_HOVER,
            text_color=TEXT_PRIMARY, border_width=1, border_color=BORDER,
            command=self.refresh).pack(side="right")

        # Scrollable list of disks
        self._scroll = ctk.CTkScrollableFrame(self, fg_color=BG_CARD,
            corner_radius=RADIUS, border_width=1, border_color=BORDER,
            scrollbar_button_color=BLUE_PRIMARY,
            scrollbar_button_hover_color=BLUE_DARK)
        self._scroll.pack(fill="both", expand=True, padx=24, pady=(0,8))

        # Column headers
        hdr = ctk.CTkFrame(self._scroll, fg_color=BLUE_PRIMARY, corner_radius=RADIUS_SM)
        hdr.pack(fill="x", padx=4, pady=(4,2))
        for txt, w in [("#", 40), (_clean(t("disk_col_dev")), 130), (_clean(t("disk_col_model")), 220),
                       (_clean(t("disk_col_serial")), 150), (_clean(t("disk_col_type")), 120),
                       (_clean(t("disk_col_size")), 90), (_clean(t("disk_col_enc")), 90)]:
            ctk.CTkLabel(hdr, text=txt, font=FONT_STEP, text_color="#ffffff",
                width=w, anchor="w").pack(side="left", padx=6, pady=4)

        self._rows_frame = ctk.CTkFrame(self._scroll, fg_color="transparent")
        self._rows_frame.pack(fill="both", expand=True)

        # System disk warning
        self._warn_lbl = ctk.CTkLabel(self, text="", font=FONT_SMALL,
            text_color=RED_DANGER, wraplength=700)
        self._warn_lbl.pack(pady=4)

        self.refresh()

    def refresh(self):
        self._status_lbl.configure(text=_clean(t("disk_scanning")))
        self._selected = None
        for w in self._rows_frame.winfo_children():
            w.destroy()
        self._disks = self._load_disks()
        self._render_rows()
        n = len(self._disks)
        none_txt = _clean(t("disk_none_found"))
        self._status_lbl.configure(
            text=f"{n} disk(s) detected" if n else none_txt)

    def _load_disks(self):
        is_mock = os.environ.get("SECUREWIPE_MOCK") == "1" or "--mock" in sys.argv
        try:
            if is_mock:
                if sys.platform == "win32":
                    from core.disk_windows import _mock_disks
                    return _mock_disks()
                else:
                    from core.disk_linux import _mock_disks
                    return _mock_disks()

            if sys.platform == "win32":
                from core.disk_windows import list_disks, _mock_disks
                disks = list_disks()
                return disks if disks else _mock_disks()
            else:
                from core.disk_linux import list_disks, _mock_disks
                disks = list_disks()
                return disks if disks else _mock_disks()
        except Exception:
            if sys.platform == "win32":
                from core.disk_windows import _mock_disks
                return _mock_disks()
            else:
                from core.disk_linux import _mock_disks
                return _mock_disks()

    def _render_rows(self):
        TYPE_COLORS = {"hdd": "#b45309", "ssd": BLUE_PRIMARY,
                       "nvme": BLUE_DARK, "unknown": TEXT_SECOND}
        ENC_COLORS  = {"luks": GREEN_DARK, "bitlocker": GREEN_DARK,
                       "sed": GREEN_DARK, "none": TEXT_DIM}

        for i, disk in enumerate(self._disks):
            row_bg = "#ffffff" if i % 2 == 0 else "#f5f5f7"
            row = ctk.CTkFrame(self._rows_frame,
                fg_color=row_bg,
                corner_radius=RADIUS_SM, cursor="hand2")
            row.pack(fill="x", padx=4, pady=2)
            row.bind("<Button-1>", lambda e, d=disk, r=row: self._select(d, r))

            num_color = RED_DANGER if disk.is_system else TEXT_SECOND
            sys_tag = " ⚠" if disk.is_system else ""

            for txt, w, color in [
                (str(i+1)+sys_tag,   40,  num_color),
                (disk.device,        130, TEXT_PRIMARY if not disk.is_system else RED_DANGER),
                (disk.model[:28],    220, TEXT_PRIMARY),
                (disk.serial[:18],   150, TEXT_SECOND),
                (disk.disk_type.upper(), 120, TYPE_COLORS.get(disk.disk_type, TEXT_SECOND)),
                (disk.size_human,    90,  TEXT_SECOND),
                (disk.encryption.upper() if disk.encryption != "none" else "—",
                 90, ENC_COLORS.get(disk.encryption, TEXT_SECOND)),
            ]:
                lbl = ctk.CTkLabel(row, text=txt, font=FONT_BODY,
                    text_color=color, width=w, anchor="w")
                lbl.pack(side="left", padx=6, pady=8)
                lbl.bind("<Button-1>", lambda e, d=disk, r=row: self._select(d, r))

    def _select(self, disk, row):
        if disk.is_system:
            self._warn_lbl.configure(
                text=f"⚠  {disk.device} is the system disk — cannot be sanitized from active OS.")
            return
        self._warn_lbl.configure(text="")
        self._selected = disk

        for i, d in enumerate(self._disks):
            child = self._rows_frame.winfo_children()[i]
            if d is disk:
                child.configure(fg_color=BLUE_PRIMARY)
                for lbl in child.winfo_children():
                    lbl.configure(text_color="#ffffff")
            else:
                bg = "#ffffff" if i % 2 == 0 else "#f5f5f7"
                child.configure(fg_color=bg)
                num_color = RED_DANGER if d.is_system else TEXT_SECOND
                cols = [
                    num_color,
                    TEXT_PRIMARY if not d.is_system else RED_DANGER,
                    TEXT_PRIMARY,
                    TEXT_SECOND,
                    TEXT_PRIMARY,
                    TEXT_SECOND,
                    TEXT_SECOND
                ]
                for idx, lbl in enumerate(child.winfo_children()):
                    if idx < len(cols):
                        lbl.configure(text_color=cols[idx])

    def get_selected(self):
        return self._selected

    def validate(self):
        if not self._selected:
            self._warn_lbl.configure(text="Please select a disk before continuing.")
            return False
        return True


