"""
SecureWipe — tests/test_file_eraser_and_carver.py
Unit tests for Module 2 (File Eraser), Module 3 (File Carver), Entropy Engine & Verification.
"""

import os
import sys
import unittest
import tempfile
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.file_eraser import wipe_single_file, wipe_path, strip_file_metadata, FileWipeMode
from core.carver import compute_shannon_entropy, calculate_candidate_confidence, carve_target, verify_wipe_carve, DEFAULT_SIGNATURES


class TestFileEraser(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_file_eraser_")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_wipe_single_file(self):
        file_p = os.path.join(self.test_dir, "secret.txt")
        with open(file_p, "wb") as f:
            f.write(b"CONFIDENTIAL DATA " * 100)

        self.assertTrue(os.path.exists(file_p))
        res = wipe_single_file(file_p, mode=FileWipeMode.NIST_3PASS)

        self.assertEqual(res.status, "SUCCESS")
        self.assertFalse(os.path.exists(file_p))
        self.assertGreater(res.bytes_overwritten, 0)
        self.assertEqual(res.passes_completed, 3)

    def test_wipe_folder_batch(self):
        sub_dir = os.path.join(self.test_dir, "batch_folder")
        os.makedirs(sub_dir, exist_ok=True)
        file1 = os.path.join(sub_dir, "f1.pdf")
        file2 = os.path.join(sub_dir, "f2.png")
        with open(file1, "wb") as f:
            f.write(b"%PDF-1.4 Header Content %%EOF")
        with open(file2, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\nFake PNG Bytes \x49\x45\x4e\x44\xae\x42\x60\x82")

        res = wipe_path(sub_dir, mode=FileWipeMode.ZERO_1PASS)
        self.assertEqual(res.status, "SUCCESS")
        self.assertEqual(res.total_files, 2)
        self.assertEqual(res.successful_files, 2)
        self.assertFalse(os.path.exists(sub_dir))

    def test_metadata_stripping_pdf(self):
        pdf_p = os.path.join(self.test_dir, "doc.pdf")
        with open(pdf_p, "wb") as f:
            f.write(b"%PDF-1.4 /Title (Top Secret) /Author (Agent X) %%EOF")

        stripped = strip_file_metadata(pdf_p)
        self.assertTrue(stripped)
        with open(pdf_p, "rb") as f:
            content = f.read()
            self.assertNotIn(b"/Title", content)
            self.assertNotIn(b"/Author", content)


class TestCarverAndEntropy(unittest.TestCase):

    def test_shannon_entropy_calculation(self):
        zeros = b"\x00" * 1000
        entropy_zeros = compute_shannon_entropy(zeros)
        self.assertEqual(entropy_zeros, 0.0)

        # High entropy random pattern
        import secrets
        rand_bytes = secrets.token_bytes(2048)
        entropy_rand = compute_shannon_entropy(rand_bytes)
        self.assertGreaterEqual(entropy_rand, 7.0)

    def test_confidence_scoring(self):
        sig = DEFAULT_SIGNATURES["jpg"]
        score_high, rating_high = calculate_candidate_confidence(
            header_found=True,
            footer_found=True,
            size_bytes=5000,
            entropy=7.2,
            sig=sig
        )
        self.assertEqual(rating_high, "HIGH")
        self.assertGreaterEqual(score_high, 90)

        score_med, rating_med = calculate_candidate_confidence(
            header_found=True,
            footer_found=False,
            size_bytes=5000,
            entropy=6.5,
            sig=sig
        )
        self.assertEqual(rating_med, "MEDIUM")

    def test_carver_extraction_and_post_wipe_verification(self):
        test_dir = tempfile.mkdtemp(prefix="test_carver_")
        img_p = os.path.join(test_dir, "test_disk.img")

        # Create disk image with embedded JPEG signature
        with open(img_p, "wb") as f:
            f.write(b"\x00" * 1024)
            f.write(b"\xFF\xD8\xFF\xE0\x00\x10JFIF" + b"JPEG_IMAGE_DATA_BLOCK" * 50 + b"\xFF\xD9")
            f.write(b"\x00" * 1024)

        out_dir = os.path.join(test_dir, "carve_out")
        carve_res = carve_target(img_p, out_dir)

        self.assertEqual(carve_res.status, "SUCCESS")
        self.assertGreaterEqual(carve_res.total_recovered, 1)

        # Now zero out the disk image (simulate wipe)
        with open(img_p, "wb") as f:
            f.write(b"\x00" * os.path.getsize(img_p))

        # Re-verify post wipe
        post_wipe_recovered = verify_wipe_carve(img_p)
        self.assertEqual(post_wipe_recovered, 0)

        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
