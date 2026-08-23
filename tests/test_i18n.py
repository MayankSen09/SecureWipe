"""
SecureWipe — Unit tests for i18n localization parity
"""

import json
import unittest
from pathlib import Path

I18N_DIR = Path(__file__).parent.parent / "i18n"

class TestI18nParity(unittest.TestCase):
    def setUp(self):
        with open(I18N_DIR / "en.json", encoding="utf-8") as f:
            self.en_keys = set(json.load(f).keys())

    def test_french_translation_keys_parity(self):
        with open(I18N_DIR / "fr.json", encoding="utf-8") as f:
            fr_keys = set(json.load(f).keys())
        missing = self.en_keys - fr_keys
        self.assertEqual(len(missing), 0, f"French translation missing keys: {missing}")

    def test_hindi_translation_keys_parity(self):
        with open(I18N_DIR / "hi.json", encoding="utf-8") as f:
            hi_keys = set(json.load(f).keys())
        missing = self.en_keys - hi_keys
        self.assertEqual(len(missing), 0, f"Hindi translation missing keys: {missing}")

if __name__ == "__main__":
    unittest.main()
