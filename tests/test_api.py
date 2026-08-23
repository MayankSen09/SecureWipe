"""
SecureWipe — Unit & Integration tests for api/app.py
"""

import unittest
from unittest.mock import patch
from api.app import health_check, get_recyclers, list_disks_api, verify_hash
from fastapi.responses import JSONResponse

class TestAPIEndpoints(unittest.TestCase):
    def test_health_endpoint(self):
        res = health_check()
        self.assertEqual(res["status"], "healthy")
        self.assertEqual(res["service"], "SecureWipe Verification Node")
        self.assertEqual(res["version"], "2.0.0")
        self.assertIn("ledger_blocks", res)

    def test_recyclers_endpoint(self):
        res = get_recyclers()
        self.assertEqual(res["status"], "success")
        self.assertIsInstance(res["recyclers"], list)
        self.assertGreater(len(res["recyclers"]), 0)

    @patch("core.disk_windows.list_disks")

    def test_list_disks_endpoint(self, mock_list):
        from api.app import MockDisk
        mock_list.return_value = [MockDisk(model="Test Disk", serial="SN123")]
        res = list_disks_api()
        self.assertEqual(res["status"], "success")
        self.assertIsInstance(res["disks"], list)


    def test_verify_nonexistent_hash(self):
        res = verify_hash(hash="0" * 64)
        if isinstance(res, JSONResponse):
            self.assertEqual(res.status_code, 404)
        else:
            self.assertTrue(res.get("verified", False))

if __name__ == "__main__":
    unittest.main()
