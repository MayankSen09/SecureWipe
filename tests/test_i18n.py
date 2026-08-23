"""
SecureWipe — Unit tests for i18n localization
"""

import json
import unittest
from pathlib import Path
from core.i18n import t, get_lang

I18N_DIR = Path(__file__).parent.parent / "i18n"

class TestI18n(unittest.TestCase):
    def setUp(self):
        with open(I18N_DIR / "en.json", encoding="utf-8") as f:
            self.en_keys = set(json.load(f).keys())

    def test_english_keys_exist(self):
        self.assertGreater(len(self.en_keys), 0)
        self.assertIn("report_title_main", self.en_keys)

    def test_translation_lookup(self):
        self.assertEqual(get_lang(), "en")
        title = t("report_title_main")
        self.assertIsNotNone(title)
        self.assertNotIn("MISSING", title)

if __name__ == "__main__":
    unittest.main()
