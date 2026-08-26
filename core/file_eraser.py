"""
SecureWipe — core/file_eraser.py
Module 2: Secure File & Folder Selective Shredder & Metadata Scrubbing Engine.

Capabilities:
- Selective single file, batch file, or recursive folder sanitization.
- Multi-pass overwrite modes (1-Pass Zero, 1-Pass Random, 3-Pass NIST/ANSSI, Custom N-Pass).
- File metadata scrubbing (EXIF stripping for JPEG/PNG, PDF property purging, Office DOCX/XLSX XML prop purging).
- File system journal remnant warning & free space zeroing helper.
- Fault-tolerant batch processing (continues processing on permission/lock errors).
"""

import os
import sys
import time
import secrets
import stat
import zipfile
import tempfile
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum, auto

# Try to import Pillow for image metadata stripping
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

CHUNK_SIZE = 1024 * 1024  # 1 MiB block buffer


class FileWipeMode(Enum):
    ZERO_1PASS   = auto()  # 1 pass zero overwrite
    RANDOM_1PASS = auto()  # 1 pass random bytes
    NIST_3PASS   = auto()  # Pass 1: Zeros, Pass 2: Ones (0xFF), Pass 3: Random
    CUSTOM_NPASS = auto()  # N alternating passes


@dataclass
class FileWipeItemResult:
    path: str
    status: str            # "SUCCESS" | "FAILED" | "ACCESS_DENIED" | "NOT_FOUND"
    bytes_overwritten: int = 0
    passes_completed: int = 0
    metadata_scrubbed: bool = False
    error_msg: str = ""


@dataclass
class FileWipeResult:
    status: str            # "SUCCESS" | "PARTIAL" | "FAILED"
    mode: FileWipeMode
    target_path: str
    total_files: int = 0
    successful_files: int = 0
    failed_files: int = 0
    total_bytes_written: int = 0
    duration_sec: float = 0.0
    items: List[FileWipeItemResult] = field(default_factory=list)


def _make_writable(path: str):
    """Ensures target file is writable by removing read-only flags."""
    try:
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
    except Exception:
        pass


def strip_file_metadata(file_path: str) -> bool:
    """
    Strips sensitive embedded metadata (EXIF data, document properties) from target file.
    Returns True if metadata was successfully stripped.
    """
    if not os.path.isfile(file_path):
        return False

    ext = os.path.splitext(file_path)[1].lower()
    _make_writable(file_path)

    # 1. Image EXIF stripping (JPEG, PNG, TIFF)
    if ext in (".jpg", ".jpeg", ".png", ".tiff") and HAS_PIL:
        try:
            with Image.open(file_path) as img:
                data = list(img.getdata())
                img_without_exif = Image.new(img.mode, img.size)
                img_without_exif.putdata(data)
                img_without_exif.save(file_path)
            return True
        except Exception:
            pass

    # 2. PDF metadata purging (Overwriting header tags)
    if ext == ".pdf":
        try:
            with open(file_path, "r+b") as f:
                content = f.read()
                tags = [b"/Title", b"/Author", b"/Subject", b"/Keywords", b"/Creator", b"/Producer", b"/CreationDate", b"/ModDate"]
                modified = False
                for tag in tags:
                    idx = 0
                    while True:
                        idx = content.find(tag, idx)
                        if idx == -1:
                            break
                        f.seek(idx)
                        f.write(b"/" + b"X" * (len(tag) - 1))
                        idx += len(tag)
                        modified = True
                if modified:
                    f.flush()
                    os.fsync(f.fileno())
                    return True
        except Exception:
            pass

    # 3. Office OpenXML document property purging (.docx, .xlsx, .pptx)
    if ext in (".docx", ".xlsx", ".pptx"):
        try:
            if zipfile.is_zipfile(file_path):
                tmp_fd, tmp_path = tempfile.mkstemp()
                os.close(tmp_fd)
                with zipfile.ZipFile(file_path, 'r') as zin:
                    with zipfile.ZipFile(tmp_path, 'w') as zout:
                        for item in zin.infolist():
                            # Omit docProps/core.xml and docProps/app.xml
                            if item.filename in ("docProps/core.xml", "docProps/app.xml"):
                                dummy_xml = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"></cp:coreProperties>'
                                zout.writestr(item.filename, dummy_xml)
                            else:
                                zout.writestr(item, zin.read(item.filename))
                os.replace(tmp_path, file_path)
                return True
        except Exception:
            pass

    return False


def wipe_single_file(
    file_path: str,
    mode: FileWipeMode = FileWipeMode.NIST_3PASS,
    custom_passes: int = 3,
    strip_meta: bool = True,
) -> FileWipeItemResult:
    """
    Overwrites and safely deletes a single file.
    """
    if not os.path.exists(file_path):
        return FileWipeItemResult(path=file_path, status="NOT_FOUND", error_msg="File does not exist.")

    if not os.path.isfile(file_path):
        return FileWipeItemResult(path=file_path, status="FAILED", error_msg="Target is a directory, not a file.")

    _make_writable(file_path)
    file_size = os.path.getsize(file_path)

    # Step 1: Optional Metadata Scrub
    meta_scrubbed = False
    if strip_meta and file_size > 0:
        meta_scrubbed = strip_file_metadata(file_path)
        file_size = os.path.getsize(file_path)

    # Step 2: Build pass patterns
    if mode == FileWipeMode.ZERO_1PASS:
        pass_patterns = [b"\x00"]
    elif mode == FileWipeMode.RANDOM_1PASS:
        pass_patterns = ["RANDOM"]
    elif mode == FileWipeMode.NIST_3PASS:
        pass_patterns = [b"\x00", b"\xFF", "RANDOM"]
    else:  # CUSTOM_NPASS
        pass_patterns = [b"\x00" if i % 2 == 0 else "RANDOM" for i in range(max(1, custom_passes))]

    total_bytes_written = 0
    passes_completed = 0

    try:
        # Overwrite content if file size > 0
        if file_size > 0:
            with open(file_path, "r+b") as f:
                for pattern in pass_patterns:
                    f.seek(0)
                    written = 0
                    while written < file_size:
                        chunk_len = min(CHUNK_SIZE, file_size - written)
                        if pattern == "RANDOM":
                            buf = secrets.token_bytes(chunk_len)
                        elif isinstance(pattern, bytes):
                            buf = pattern * chunk_len
                        else:
                            buf = b"\x00" * chunk_len

                        f.write(buf)
                        written += len(buf)

                    f.flush()
                    os.fsync(f.fileno())
                    total_bytes_written += written
                    passes_completed += 1

                # Step 3: Truncate file to 0 bytes
                f.seek(0)
                f.truncate(0)

        # Step 4: Obfuscate filename before deleting
        folder, old_name = os.path.split(file_path)
        obfuscated_name = secrets.token_hex(12) + ".tmp"
        obfuscated_path = os.path.join(folder, obfuscated_name)
        try:
            os.rename(file_path, obfuscated_path)
            target_to_delete = obfuscated_path
        except Exception:
            target_to_delete = file_path

        # Step 5: Unlink file
        os.remove(target_to_delete)

        return FileWipeItemResult(
            path=file_path,
            status="SUCCESS",
            bytes_overwritten=total_bytes_written,
            passes_completed=passes_completed or len(pass_patterns),
            metadata_scrubbed=meta_scrubbed,
        )

    except PermissionError as pe:
        return FileWipeItemResult(path=file_path, status="ACCESS_DENIED", error_msg=f"Permission denied: {pe}")
    except Exception as e:
        return FileWipeItemResult(path=file_path, status="FAILED", error_msg=str(e))


def wipe_path(
    target_path: str,
    mode: FileWipeMode = FileWipeMode.NIST_3PASS,
    custom_passes: int = 3,
    strip_meta: bool = True,
    progress_cb: Optional[Callable[[int, int, str], None]] = None,
) -> FileWipeResult:
    """
    Securely overwrites and deletes a file or recursively processes a folder batch.
    """
    start_time = time.time()
    result = FileWipeResult(
        status="FAILED",
        mode=mode,
        target_path=target_path,
    )

    if not os.path.exists(target_path):
        result.items.append(FileWipeItemResult(path=target_path, status="NOT_FOUND", error_msg="Path does not exist."))
        return result

    # Enumerate files
    files_to_wipe: List[str] = []
    if os.path.isfile(target_path):
        files_to_wipe.append(target_path)
    else:
        for root, dirs, files in os.walk(target_path, topdown=False):
            for file_name in files:
                full_p = os.path.join(root, file_name)
                # Skip symlinks outside root if needed
                if not os.path.islink(full_p):
                    files_to_wipe.append(full_p)

    result.total_files = len(files_to_wipe)
    if result.total_files == 0 and os.path.isdir(target_path):
        try:
            os.rmdir(target_path)
            result.status = "SUCCESS"
        except Exception as e:
            result.status = "FAILED"
        return result

    for idx, f_path in enumerate(files_to_wipe):
        if progress_cb:
            progress_cb(idx + 1, result.total_files, f_path)

        res_item = wipe_single_file(f_path, mode=mode, custom_passes=custom_passes, strip_meta=strip_meta)
        result.items.append(res_item)

        if res_item.status == "SUCCESS":
            result.successful_files += 1
            result.total_bytes_written += res_item.bytes_overwritten
        else:
            result.failed_files += 1

    # Remove empty subdirectories if target was a directory
    if os.path.isdir(target_path):
        for root, dirs, files in os.walk(target_path, topdown=False):
            for d in dirs:
                try:
                    os.rmdir(os.path.join(root, d))
                except Exception:
                    pass
        try:
            os.rmdir(target_path)
        except Exception:
            pass

    result.duration_sec = time.time() - start_time
    if result.successful_files == result.total_files:
        result.status = "SUCCESS"
    elif result.successful_files > 0:
        result.status = "PARTIAL"
    else:
        result.status = "FAILED"

    return result


def wipe_free_space(target_directory: str, max_bytes: Optional[int] = None) -> tuple[bool, int, str]:
    """
    Fills unallocated space in target directory with zero bytes to eliminate residual file system remnants.
    Returns (success, bytes_written, error_msg).
    """
    if not os.path.exists(target_directory):
        return False, 0, "Directory does not exist."

    tmp_file = os.path.join(target_directory, f".wipe_freespace_{secrets.token_hex(6)}.tmp")
    written = 0
    error = ""

    try:
        with open(tmp_file, "wb") as f:
            zero_chunk = b"\x00" * CHUNK_SIZE
            while True:
                if max_bytes and written >= max_bytes:
                    break
                try:
                    to_write = CHUNK_SIZE if not max_bytes else min(CHUNK_SIZE, max_bytes - written)
                    f.write(zero_chunk[:to_write])
                    written += to_write
                except OSError:  # Disk full (ENOSPC)
                    break
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        error = str(e)
    finally:
        if os.path.exists(tmp_file):
            try:
                os.remove(tmp_file)
            except Exception:
                pass

    return (not error), written, error
