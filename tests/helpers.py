from __future__ import annotations

from meowtheme.base16 import Base16Palette, parse_base16_scheme


SCHEME = """
scheme: MeowDark
author: meow
appearance: dark
base00: "121212"
base01: "1c1c1c"
base02: "303030"
base03: "686868"
base04: "8a8a8a"
base05: "d0d0d0"
base06: "e8e8e8"
base07: "ffffff"
base08: "f07178"
base09: "f78c6c"
base0A: "ffcb6b"
base0B: "c3e88d"
base0C: "89ddff"
base0D: "82aaff"
base0E: "c792ea"
base0F: "ab7967"
"""


def palette() -> Base16Palette:
    return parse_base16_scheme(SCHEME)
