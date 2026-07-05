from __future__ import annotations

import plistlib
from typing import Any

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.editor_colors import editor_colors


def render_codex(palette: Base16Palette) -> str:
    colors = editor_colors(palette)
    payload: dict[str, Any] = {
        "name": palette.scheme,
        "author": palette.author,
        "settings": [
            {
                "settings": {
                    "background": colors.editor_background,
                    "caret": colors.text_accent,
                    "foreground": colors.editor_foreground,
                    "invisibles": colors.editor_invisible,
                    "lineHighlight": colors.editor_active_line_background,
                    "selection": colors.selection,
                }
            },
            scope("Comment", "comment", colors.syntax.comment, font_style="italic"),
            scope("String", "string", colors.syntax.string),
            scope("Number", "constant.numeric", colors.syntax.number),
            scope(
                "Boolean",
                "constant.language.boolean, constant.language",
                colors.syntax.boolean,
            ),
            scope("Constant", "constant.language, constant.character", colors.syntax.constant),
            scope("Keyword", "keyword, storage", colors.syntax.keyword),
            scope("Function", "entity.name.function, support.function", colors.syntax.function),
            scope("Type", "entity.name.type, support.type, support.class", colors.syntax.type),
            scope("Variable", "variable, variable.parameter", colors.syntax.variable),
            scope("Property", "variable.other.property, support.variable", colors.syntax.property),
            scope("Attribute", "entity.other.attribute-name", colors.syntax.attribute),
            scope("Punctuation", "punctuation", colors.syntax.punctuation),
            scope("Invalid", "invalid", colors.error.foreground),
        ],
    }
    return plistlib.dumps(payload, sort_keys=False).decode("utf-8")


def scope(
    name: str,
    selector: str,
    foreground: str,
    *,
    font_style: str | None = None,
) -> dict[str, object]:
    settings = {"foreground": foreground}
    if font_style is not None:
        settings["fontStyle"] = font_style
    return {"name": name, "scope": selector, "settings": settings}
