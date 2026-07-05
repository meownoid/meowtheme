from __future__ import annotations

import json

from meowtheme.base16 import Base16Palette


def semantic_tokens(palette: Base16Palette) -> dict[str, str]:
    return {
        "background": palette.base("base00").hex,
        "surface": palette.base("base01").hex,
        "surfaceRaised": palette.base("base02").hex,
        "muted": palette.base("base03").hex,
        "mutedForeground": palette.base("base04").hex,
        "foreground": palette.base("base05").hex,
        "foregroundStrong": palette.base("base06").hex,
        "foregroundBright": palette.base("base07").hex,
        "red": palette.base("base08").hex,
        "orange": palette.base("base09").hex,
        "yellow": palette.base("base0A").hex,
        "green": palette.base("base0B").hex,
        "cyan": palette.base("base0C").hex,
        "blue": palette.base("base0D").hex,
        "purple": palette.base("base0E").hex,
        "brown": palette.base("base0F").hex,
    }


def scope(name: str, scopes: list[str], foreground: str) -> dict[str, object]:
    return {"name": name, "scope": scopes, "settings": {"foreground": foreground}}


def pretty_json(payload: object) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def without_hash(value: str) -> str:
    return value.removeprefix("#")
