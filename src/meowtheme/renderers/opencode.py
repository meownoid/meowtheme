from __future__ import annotations

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.common import pretty_json
from meowtheme.renderers.editor_colors import alpha_hex, editor_colors


OPENCODE_THEME_SCHEMA = "https://opencode.ai/theme.json"


def render_opencode(palette: Base16Palette) -> str:
    colors = editor_colors(palette)
    theme = {
        "primary": colors.text_accent,
        "secondary": colors.syntax.keyword,
        "accent": colors.syntax.property,
        "error": colors.error.foreground,
        "warning": colors.warning.foreground,
        "success": colors.success.foreground,
        "info": colors.syntax.property,
        "text": colors.text,
        "textMuted": colors.text_muted,
        "selectedListItemText": colors.background,
        "background": colors.background,
        "backgroundPanel": colors.surface_background,
        "backgroundElement": colors.element_active,
        "backgroundMenu": colors.element_active,
        "border": colors.editor_invisible,
        "borderActive": colors.border_focused,
        "borderSubtle": colors.border,
        "diffAdded": colors.created.foreground,
        "diffRemoved": colors.deleted.foreground,
        "diffContext": colors.text_muted,
        "diffHunkHeader": colors.info.foreground,
        "diffHighlightAdded": colors.success.foreground,
        "diffHighlightRemoved": colors.error.foreground,
        "diffAddedBg": alpha_hex(colors.created.foreground, 0.14),
        "diffRemovedBg": alpha_hex(colors.deleted.foreground, 0.14),
        "diffContextBg": colors.surface_background,
        "diffLineNumber": colors.text_muted,
        "diffAddedLineNumberBg": alpha_hex(colors.created.foreground, 0.20),
        "diffRemovedLineNumberBg": alpha_hex(colors.deleted.foreground, 0.20),
        "markdownText": colors.text,
        "markdownHeading": colors.syntax.function,
        "markdownLink": colors.syntax.property,
        "markdownLinkText": colors.syntax.function,
        "markdownCode": colors.syntax.string,
        "markdownBlockQuote": colors.warning.foreground,
        "markdownEmph": colors.warning.foreground,
        "markdownStrong": colors.text,
        "markdownHorizontalRule": colors.text_muted,
        "markdownListItem": colors.syntax.function,
        "markdownListEnumeration": colors.syntax.property,
        "markdownImage": colors.syntax.function,
        "markdownImageText": colors.syntax.property,
        "markdownCodeBlock": colors.text,
        "syntaxComment": colors.syntax.comment,
        "syntaxKeyword": colors.syntax.keyword,
        "syntaxFunction": colors.syntax.function,
        "syntaxVariable": colors.syntax.variable,
        "syntaxString": colors.syntax.string,
        "syntaxNumber": colors.syntax.number,
        "syntaxType": colors.syntax.type,
        "syntaxOperator": colors.syntax.property,
        "syntaxPunctuation": colors.syntax.punctuation,
    }
    return pretty_json({"$schema": OPENCODE_THEME_SCHEMA, "theme": theme})
