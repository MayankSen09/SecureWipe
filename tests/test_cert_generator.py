"""
SecureWipe — Unit tests for cert/generator.py
"""

import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from api.app import MockDisk
from cert.generator import generate_certificate, _get_next_report_id
from core.wipe_engine import WipeResult, WipeStatus, WipeMode

class TestCertGenerator(unittest.TestCase):
    def test_report_id_generation(self):
        rep_id = _get_next_report_id(Path("."))
        self.assertIsInstance(rep_id, str)
        self.assertGreaterEqual(len(rep_id), 12)

    def test_generate_certificate_pipeline(self):
        tmp_dir = Path(tempfile.mkdtemp())
        disk = MockDisk(model="Test NVMe SSD", serial="SN-TEST-12345")
        operator = {
            "name": "Test Operator",
            "org": "Test Security Lab",
            "datetime": datetime.now(),
            "machine": "TestNode",
            "os": "win32"
        }
        result = WipeResult(
            status=WipeStatus.SUCCESS,
            mode=WipeMode.NIST_PURGE,
            device=disk.device,
            duration_sec=25.0,
            passes_done=1,
            verify_ok=True,
            confidence_score=100,
            standard="NIST SP 800-88",
            hpa_detected=False,
            hpa_wiped=False
        )

        pdf_path, txt_path = generate_certificate(
            operator=operator,
            disk=disk,
            result=result,
            mode_label="NIST SP 800-88 Purge",
            verify_pct=10,
            output_dir=tmp_dir,
            script_dir=Path(__file__).parent.parent
        )

        self.assertTrue(pdf_path.exists())
        self.assertTrue(txt_path.exists())
        self.assertGreater(pdf_path.stat().st_size, 1000)

        # Cleanup test files
        try:
            pdf_path.unlink(missing_ok=True)
            txt_path.unlink(missing_ok=True)
        except Exception:
            pass

if __name__ == "__main__":
    unittest.main()
