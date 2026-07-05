from __future__ import annotations

import json

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.common import semantic_tokens


CODEX_DESKTOP_THEME_PREFIX = "codex-theme-v1:"
CODEX_DESKTOP_CODE_THEME_ID = "one"
CODEX_DESKTOP_CONTRAST = {"dark": 60, "light": 45}


def render_codex_desktop(palette: Base16Palette) -> str:
    tokens = semantic_tokens(palette)
    payload = {
        "codeThemeId": CODEX_DESKTOP_CODE_THEME_ID,
        "theme": {
            "accent": tokens["blue"],
            "contrast": CODEX_DESKTOP_CONTRAST[palette.appearance],
            "fonts": {"code": "Menlo, ui-monospace, SFMono-Regular", "ui": "Inter"},
            "ink": tokens["foreground"],
            "opaqueWindows": True,
            "semanticColors": {
                "diffAdded": tokens["green"],
                "diffRemoved": tokens["red"],
                "skill": tokens["purple"],
            },
            "surface": tokens["background"],
        },
        "variant": palette.appearance,
    }
    return CODEX_DESKTOP_THEME_PREFIX + json.dumps(payload, separators=(",", ":")) + "\n"
