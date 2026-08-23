"""
SecureWipe — Unit tests for core/confidence.py
"""

import unittest
from core.confidence import compute_score

class TestConfidenceScore(unittest.TestCase):
    def test_full_success(self):
        # ATA success (50) + sampling pass (30) + no HPA (20) = 100
        score = compute_score(
            ata_success=True,
            sampling_pass=True,
            hpa_detected=False,
        )
        self.assertEqual(score, 100)

    def test_crypto_erase_only(self):
        # Crypto erase (50) + no sampling (0) + no HPA (20) = 70
        score = compute_score(
            crypto_erase=True,
            sampling_pass=False,
            hpa_detected=False,
        )
        self.assertEqual(score, 70)

    def test_hpa_detected_not_wiped(self):
        # ATA success (50) + sampling pass (30) + HPA detected & not wiped (0) = 80
        score = compute_score(
            ata_success=True,
            sampling_pass=True,
            hpa_detected=True,
            hpa_wiped=False,
        )
        self.assertEqual(score, 80)

    def test_hpa_detected_and_wiped(self):
        # ATA success (50) + sampling pass (30) + HPA detected & wiped (20) = 100
        score = compute_score(
            ata_success=True,
            sampling_pass=True,
            hpa_detected=True,
            hpa_wiped=True,
        )
        self.assertEqual(score, 100)

    def test_minimum_score_zero(self):
        # ATA fail (0) + sampling fail (0) + HPA detected & not wiped (0) = 0
        score = compute_score(
            ata_success=False,
            sampling_pass=False,
            hpa_detected=True,
            hpa_wiped=False,
        )
        self.assertEqual(score, 0)

    def test_score_bounded_to_hundred(self):
        # Both ATA and crypto erase true + sampling pass + no HPA -> capped at 100
        score = compute_score(
            ata_success=True,
            crypto_erase=True,
            sampling_pass=True,
            hpa_detected=False,
        )
        self.assertLessEqual(score, 100)
        self.assertGreaterEqual(score, 0)

if __name__ == "__main__":
    unittest.main()

