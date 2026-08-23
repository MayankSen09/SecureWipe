"""
SecureWipe — Unit tests for trust/blockchain.py
"""

import unittest
from trust.blockchain import is_valid_sha256, verify_chain

class TestBlockchainLedger(unittest.TestCase):
    def test_valid_sha256_hashes(self):
        valid_hash = "a" * 64
        self.assertTrue(is_valid_sha256(valid_hash))
        self.assertTrue(is_valid_sha256("0x" + valid_hash))
        self.assertTrue(is_valid_sha256("1234567890abcdef" * 4))

    def test_invalid_sha256_hashes(self):
        self.assertFalse(is_valid_sha256("invalid_hash"))
        self.assertFalse(is_valid_sha256("a" * 63))
        self.assertFalse(is_valid_sha256("g" * 64))
        self.assertFalse(is_valid_sha256(12345))

    def test_chain_verification_status(self):
        is_valid, msg = verify_chain()
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(msg, str)

if __name__ == "__main__":
    unittest.main()
