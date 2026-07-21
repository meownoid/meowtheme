from __future__ import annotations

import plistlib
from typing import Any

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.editor_colors import alpha_hex, editor_colors


SOURCE_FONT = "Iosevka-Extralight - 18.0"
CONSOLE_FONT = "SFMono-Regular - 11.0"
CONSOLE_PROMPT_FONT = "Iosevka-Term-Extralight - 11.0"

SYNTAX_COLOR_NAMES = (
    "xcode.syntax.attribute",
    "xcode.syntax.character",
    "xcode.syntax.comment",
    "xcode.syntax.comment.doc",
    "xcode.syntax.comment.doc.keyword",
    "xcode.syntax.declaration.other",
    "xcode.syntax.declaration.type",
    "xcode.syntax.identifier.class",
    "xcode.syntax.identifier.class.system",
    "xcode.syntax.identifier.constant",
    "xcode.syntax.identifier.constant.system",
    "xcode.syntax.identifier.function",
    "xcode.syntax.identifier.function.system",
    "xcode.syntax.identifier.macro",
    "xcode.syntax.identifier.macro.system",
    "xcode.syntax.identifier.type",
    "xcode.syntax.identifier.type.system",
    "xcode.syntax.identifier.variable",
    "xcode.syntax.identifier.variable.system",
    "xcode.syntax.keyword",
    "xcode.syntax.mark",
    "xcode.syntax.markup.code",
    "xcode.syntax.number",
    "xcode.syntax.plain",
    "xcode.syntax.preprocessor",
    "xcode.syntax.regex",
    "xcode.syntax.regex.capturename",
    "xcode.syntax.regex.charname",
    "xcode.syntax.regex.number",
    "xcode.syntax.regex.other",
    "xcode.syntax.string",
    "xcode.syntax.url",
)


def render_xcode(palette: Base16Palette) -> str:
    colors = editor_colors(palette)
    foreground = xcode_color(colors.editor_foreground)
    background = xcode_color(colors.editor_background)
    insertion_point = xcode_color(colors.text)

    syntax_colors = {
        "xcode.syntax.attribute": xcode_color(colors.syntax.attribute),
        "xcode.syntax.character": xcode_color(colors.syntax.constant),
        "xcode.syntax.comment": xcode_color(colors.syntax.comment),
        "xcode.syntax.comment.doc": xcode_color(colors.syntax.comment),
        "xcode.syntax.comment.doc.keyword": xcode_color(colors.syntax.comment),
        "xcode.syntax.declaration.other": xcode_color(colors.syntax.variable),
        "xcode.syntax.declaration.type": xcode_color(colors.syntax.type),
        "xcode.syntax.identifier.class": xcode_color(colors.syntax.type),
        "xcode.syntax.identifier.class.system": xcode_color(colors.syntax.type),
        "xcode.syntax.identifier.constant": xcode_color(colors.syntax.constant),
        "xcode.syntax.identifier.constant.system": xcode_color(colors.syntax.type),
        "xcode.syntax.identifier.function": xcode_color(colors.syntax.function),
        "xcode.syntax.identifier.function.system": xcode_color(colors.syntax.function),
        "xcode.syntax.identifier.macro": xcode_color(colors.syntax.keyword),
        "xcode.syntax.identifier.macro.system": xcode_color(colors.syntax.type),
        "xcode.syntax.identifier.type": xcode_color(colors.syntax.type),
        "xcode.syntax.identifier.type.system": xcode_color(colors.syntax.type),
        "xcode.syntax.identifier.variable": xcode_color(colors.syntax.variable),
        "xcode.syntax.identifier.variable.system": xcode_color(colors.syntax.variable),
        "xcode.syntax.keyword": xcode_color(colors.syntax.keyword),
        "xcode.syntax.mark": xcode_color(colors.text_muted),
        "xcode.syntax.markup.code": xcode_color(colors.syntax.string),
        "xcode.syntax.number": xcode_color(colors.syntax.number),
        "xcode.syntax.plain": foreground,
        "xcode.syntax.preprocessor": xcode_color(colors.syntax.keyword),
        "xcode.syntax.regex": xcode_color(colors.syntax.string),
        "xcode.syntax.regex.capturename": xcode_color(colors.syntax.type),
        "xcode.syntax.regex.charname": xcode_color(colors.syntax.type),
        "xcode.syntax.regex.number": xcode_color(colors.syntax.number),
        "xcode.syntax.regex.other": foreground,
        "xcode.syntax.string": xcode_color(colors.syntax.string),
        "xcode.syntax.url": xcode_color(colors.syntax.property),
    }
    syntax_fonts = {name: SOURCE_FONT for name in SYNTAX_COLOR_NAMES}

    payload: dict[str, Any] = {
        "DVTConsoleDebuggerInputTextColor": foreground,
        "DVTConsoleDebuggerInputTextFont": CONSOLE_FONT,
        "DVTConsoleDebuggerOutputTextColor": foreground,
        "DVTConsoleDebuggerOutputTextFont": CONSOLE_FONT,
        "DVTConsoleDebuggerPromptTextColor": xcode_color(colors.syntax.type),
        "DVTConsoleDebuggerPromptTextFont": CONSOLE_PROMPT_FONT,
        "DVTConsoleExectuableInputTextColor": foreground,
        "DVTConsoleExectuableInputTextFont": CONSOLE_FONT,
        "DVTConsoleExectuableOutputTextColor": foreground,
        "DVTConsoleExectuableOutputTextFont": CONSOLE_FONT,
        "DVTConsoleTextBackgroundColor": background,
        "DVTConsoleTextInsertionPointColor": insertion_point,
        "DVTConsoleTextSelectionColor": xcode_color(colors.selection),
        "DVTFontAndColorVersion": 1,
        "DVTLineSpacing": 1.1,
        "DVTMarkupTextBackgroundColor": xcode_color(colors.surface_background),
        "DVTMarkupTextBorderColor": xcode_color(colors.border),
        "DVTMarkupTextCodeFont": "SFMono-Regular - 10.0",
        "DVTMarkupTextEmphasisColor": foreground,
        "DVTMarkupTextEmphasisFont": ".AppleSystemUIFontItalic - 10.0",
        "DVTMarkupTextInlineCodeColor": xcode_color(
            alpha_hex(colors.editor_foreground, 0.7)
        ),
        "DVTMarkupTextLinkColor": xcode_color(colors.syntax.property),
        "DVTMarkupTextLinkFont": ".AppleSystemUIFont - 10.0",
        "DVTMarkupTextNormalColor": foreground,
        "DVTMarkupTextNormalFont": ".AppleSystemUIFont - 10.0",
        "DVTMarkupTextOtherHeadingColor": xcode_color(
            alpha_hex(colors.editor_foreground, 0.5)
        ),
        "DVTMarkupTextOtherHeadingFont": ".AppleSystemUIFont - 14.0",
        "DVTMarkupTextPrimaryHeadingColor": foreground,
        "DVTMarkupTextPrimaryHeadingFont": ".AppleSystemUIFont - 24.0",
        "DVTMarkupTextSecondaryHeadingColor": foreground,
        "DVTMarkupTextSecondaryHeadingFont": ".AppleSystemUIFont - 18.0",
        "DVTMarkupTextStrongColor": foreground,
        "DVTMarkupTextStrongFont": ".AppleSystemUIFontBold - 10.0",
        "DVTScrollbarMarkerAnalyzerColor": xcode_color(colors.syntax.keyword),
        "DVTScrollbarMarkerBreakpointColor": xcode_color(colors.debug_breakpoint),
        "DVTScrollbarMarkerDiffColor": xcode_color(colors.text_muted),
        "DVTScrollbarMarkerDiffConflictColor": xcode_color(colors.error.foreground),
        "DVTScrollbarMarkerErrorColor": xcode_color(colors.error.foreground),
        "DVTScrollbarMarkerRuntimeIssueColor": xcode_color(colors.syntax.keyword),
        "DVTScrollbarMarkerWarningColor": xcode_color(colors.warning.foreground),
        "DVTSourceTextBackground": background,
        "DVTSourceTextBlockDimBackgroundColor": xcode_color(colors.text_muted),
        "DVTSourceTextCurrentLineHighlightColor": xcode_color(
            colors.editor_active_line_background
        ),
        "DVTSourceTextInsertionPointColor": insertion_point,
        "DVTSourceTextInvisiblesColor": xcode_color(
            alpha_hex(colors.editor_invisible, 0.32)
        ),
        "DVTSourceTextSelectionColor": xcode_color(colors.selection),
        "DVTSourceTextSyntaxColors": syntax_colors,
        "DVTSourceTextSyntaxFonts": syntax_fonts,
    }
    return plistlib.dumps(payload, fmt=plistlib.FMT_XML, sort_keys=False).decode("utf-8")


def xcode_color(hex_color: str) -> str:
    value = hex_color.removeprefix("#")
    if len(value) not in {6, 8}:
        raise ValueError("Xcode colors must use 6- or 8-digit hex notation")

    channels = [int(value[index : index + 2], 16) / 255 for index in range(0, len(value), 2)]
    if len(channels) == 3:
        channels.append(1.0)
    return " ".join(f"{channel:.10g}" for channel in channels)
