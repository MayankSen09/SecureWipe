"""
SecureWipe — i18n module
Internationalization module providing English locale dictionary loading.
"""

import json
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint

console = Console()

I18N_DIR = Path(__file__).parent.parent / "i18n"

SUPPORTED_LANGS = {
    "1": "en",
}

def _load(lang: str = "en") -> dict:
    """Loads translation dictionary for specified language (defaults to English)."""
    path = I18N_DIR / f"{lang}.json"
    if not path.exists():
        path = I18N_DIR / "en.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

_translations: dict = _load("en")
_current_lang: str = "en"


def t(key: str, **kwargs) -> str:
    """
    Returns translated string for the given key.
    Supports placeholder formatting via kwargs.
    """
    val = _translations.get(key, f"[MISSING:{key}]")
    if kwargs:
        try:
            val = val.format(**kwargs)
        except KeyError:
            pass
    return val


def select_language() -> str:
    """
    Initializes language selection (defaults to English).
    Returns chosen language code ('en').
    """
    global _translations, _current_lang

    _translations = _load("en")
    _current_lang = "en"

    return "en"


def get_lang() -> str:
    """Returns current active language code."""
    return _current_lang

