from __future__ import annotations

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.common import pretty_json
from meowtheme.renderers.editor_colors import editor_colors


def render_chrome(palette: Base16Palette) -> str:
    colors = editor_colors(palette)
    payload = {
        "manifest_version": 3,
        "name": palette.scheme,
        "version": "0.1.0",
        "theme": {
            "colors": {
                "bookmark_text": rgb(colors.text),
                "button_background": rgb(colors.element_background),
                "frame": rgb(colors.background),
                "frame_inactive": rgb(colors.title_bar_inactive_background),
                "ntp_background": rgb(colors.background),
                "ntp_text": rgb(colors.text),
                "tab_background_text": rgb(colors.text_muted),
                "tab_text": rgb(colors.text),
                "toolbar": rgb(colors.surface),
            }
        },
    }
    return pretty_json(payload)


def rgb(hex_color: str) -> list[int]:
    color = hex_color.removeprefix("#")
    return [int(color[index : index + 2], 16) for index in range(0, 6, 2)]
