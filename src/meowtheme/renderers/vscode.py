from __future__ import annotations

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.common import pretty_json, scope
from meowtheme.renderers.editor_colors import editor_colors


def render_vscode(palette: Base16Palette) -> str:
    colors = editor_colors(palette)
    payload = {
        "name": palette.scheme,
        "type": palette.appearance,
        "colors": {
            "activityBar.background": colors.surface,
            "activityBar.foreground": colors.text,
            "debugIcon.breakpointForeground": colors.debug_breakpoint,
            "editor.background": colors.editor_background,
            "editor.foreground": colors.editor_foreground,
            "editor.lineHighlightBackground": colors.editor_active_line_background,
            "editor.selectionBackground": colors.selection,
            "editorLineNumber.activeForeground": colors.editor_active_line_number,
            "editorLineNumber.foreground": colors.editor_line_number,
            "editorCursor.foreground": colors.text_accent,
            "editorError.foreground": colors.error.foreground,
            "editorWarning.foreground": colors.warning.foreground,
            "focusBorder": colors.border_focused,
            "sideBar.background": colors.surface,
            "sideBar.foreground": colors.text,
            "statusBar.background": colors.status_bar_background,
            "terminal.ansiBlack": colors.terminal.ansi_black,
            "terminal.ansiBlue": colors.terminal.ansi_blue,
            "terminal.ansiBrightBlack": colors.terminal.ansi_bright_black,
            "terminal.ansiBrightBlue": colors.terminal.ansi_bright_blue,
            "terminal.ansiBrightCyan": colors.terminal.ansi_bright_cyan,
            "terminal.ansiBrightGreen": colors.terminal.ansi_bright_green,
            "terminal.ansiBrightMagenta": colors.terminal.ansi_bright_magenta,
            "terminal.ansiBrightRed": colors.terminal.ansi_bright_red,
            "terminal.ansiBrightWhite": colors.terminal.ansi_bright_white,
            "terminal.ansiBrightYellow": colors.terminal.ansi_bright_yellow,
            "terminal.ansiCyan": colors.terminal.ansi_cyan,
            "terminal.ansiGreen": colors.terminal.ansi_green,
            "terminal.ansiMagenta": colors.terminal.ansi_magenta,
            "terminal.ansiRed": colors.terminal.ansi_red,
            "terminal.ansiWhite": colors.terminal.ansi_white,
            "terminal.ansiYellow": colors.terminal.ansi_yellow,
        },
        "tokenColors": [
            scope("Comment", ["comment"], colors.syntax.comment),
            scope("String", ["string"], colors.syntax.string),
            scope("Number", ["constant.numeric"], colors.syntax.number),
            scope(
                "Boolean",
                ["constant.language.boolean", "constant.language"],
                colors.syntax.boolean,
            ),
            scope("Keyword", ["keyword"], colors.syntax.keyword),
            scope("Function", ["entity.name.function"], colors.syntax.function),
            scope("Type", ["entity.name.type", "support.type"], colors.syntax.type),
            scope("Variable", ["variable"], colors.syntax.variable),
        ],
    }
    return pretty_json(payload)
