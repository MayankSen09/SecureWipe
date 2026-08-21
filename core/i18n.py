"""
SecureWipe — i18n module
FR/EN translation management with automatic locale detection.
Author: TEAM SOLUTION
"""

import json
import locale
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint

console = Console()

# Path to the i18n directory (relative to this file)
I18N_DIR = Path(__file__).parent.parent / "i18n"

SUPPORTED_LANGS = {
    "1": "fr",
    "2": "en",
}

def _load(lang: str) -> dict:
    """Loads the translation file for the given language."""
    path = I18N_DIR / f"{lang}.json"
    if not path.exists():
        console.print(f"[red]Translation file not found: {path}[/red]")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

_translations: dict = _load("en")
_current_lang: str = "en"


def t(key: str, **kwargs) -> str:
    """
    Returns the translated string for the given key.
    Supports {variable} placeholders via kwargs.
    """
    val = _translations.get(key, f"[MISSING:{key}]")
    if kwargs:
        try:
            val = val.format(**kwargs)
        except KeyError:
            pass
    return val


def _detect_system_lang() -> str:
    """Detects the system language and returns 'fr' or 'en'."""
    try:
        # Check LANG environment variable first
        env_lang = os.environ.get("LANG", "") or os.environ.get("LANGUAGE", "")
        if env_lang.lower().startswith("fr"):
            return "fr"

        # Fallback to Python locale
        loc = locale.getdefaultlocale()
        if loc and loc[0] and loc[0].lower().startswith("fr"):
            return "fr"

        # Windows: read user default UI language
        if sys.platform == "win32":
            import ctypes
            lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            # 0x040C = French, 0x0C0C = French Canadian, etc.
            if (lang_id & 0xFF) == 0x0C:
                return "fr"

    except Exception:
        pass

    return "en"


def select_language() -> str:
    """
    Displays the language selection menu.
    Detects system locale, offers confirmation, or manual selection menu.
    Returns the chosen language code ('fr' or 'en').
    """
    global _translations, _current_lang

    # Load EN by default for initial menu
    _translations = _load("en")
    _current_lang = "en"

    detected = _detect_system_lang()
    detected_name = "Français" if detected == "fr" else "English"

    console.print()
    console.print(Panel(
        "[bold cyan]SecureWipe[/bold cyan]",
        subtitle="[dim]Secure Storage Sanitization[/dim]",
        border_style="cyan",
        padding=(0, 4),
    ))
    console.print()

    # Display detected language and prompt for choice
    rprint(f"  [dim]Langue détectée / Detected language:[/dim] [bold cyan]{detected_name}[/bold cyan]")
    console.print()

    # Propose options
    rprint("  [bold]1.[/bold]  Français")
    rprint("  [bold]2.[/bold]  English")
    console.print()

    while True:
        choice = Prompt.ask(
            "  [bold white]Sélection / Selection[/bold white]",
            default="1" if detected == "fr" else "2",
            console=console,
        ).strip()

        if choice in SUPPORTED_LANGS:
            chosen = SUPPORTED_LANGS[choice]
            break
        # Accept direct "fr"/"en"
        elif choice.lower() in ("fr", "français", "francais"):
            chosen = "fr"
            break
        elif choice.lower() in ("en", "english"):
            chosen = "en"
            break
        else:
            rprint("  [red]Choix invalide / Invalid choice. Entrez 1 ou 2.[/red]")

    # Load selected language
    _translations = _load(chosen)
    _current_lang = chosen

    console.print()
    rprint(f"  [green]✓[/green] {t('lang_name')} sélectionné / selected.")
    console.print()

    return chosen


def get_lang() -> str:
    """Returns current active language code."""
    return _current_lang
