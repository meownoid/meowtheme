from __future__ import annotations

from dataclasses import dataclass

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.editor_colors import editor_colors


@dataclass(frozen=True)
class Highlight:
    group: str
    guifg: str | None = None
    guibg: str | None = None
    gui: str | None = None
    guisp: str | None = None


def render_vim(palette: Base16Palette) -> str:
    colors = editor_colors(palette)
    highlights = [
        Highlight("Normal", guifg=colors.editor_foreground, guibg=colors.editor_background),
        Highlight("ColorColumn", guibg=colors.editor_active_wrap_guide),
        Highlight("Conceal", guifg=colors.editor_invisible),
        Highlight("Cursor", guifg=colors.editor_background, guibg=colors.text_accent),
        Highlight("CursorColumn", guibg=colors.editor_active_line_background),
        Highlight("CursorLine", guibg=colors.editor_active_line_background),
        Highlight(
            "CursorLineFold",
            guifg=colors.editor_active_line_number,
            guibg=colors.editor_gutter_background,
        ),
        Highlight("CursorLineNr", guifg=colors.editor_active_line_number),
        Highlight("CursorLineSign", guibg=colors.editor_gutter_background),
        Highlight("CurSearch", guifg=colors.text, guibg=colors.search_match_background),
        Highlight("Directory", guifg=colors.syntax.function),
        Highlight("Error", guifg=colors.error.foreground, guibg=colors.error.background),
        Highlight("FoldColumn", guifg=colors.editor_line_number, guibg=colors.editor_background),
        Highlight("Folded", guifg=colors.text_muted, guibg=colors.surface),
        Highlight("IncSearch", guifg=colors.text, guibg=colors.search_match_background),
        Highlight("LineNr", guifg=colors.editor_line_number),
        Highlight("LineNrAbove", guifg=colors.editor_line_number),
        Highlight("LineNrBelow", guifg=colors.editor_line_number),
        Highlight("MatchParen", guifg=colors.text, guibg=colors.search_match_background),
        Highlight("NonText", guifg=colors.editor_invisible),
        Highlight("Pmenu", guifg=colors.text, guibg=colors.panel_background),
        Highlight("PmenuBorder", guifg=colors.pane_group_border, guibg=colors.panel_background),
        Highlight("PmenuExtra", guifg=colors.text_muted, guibg=colors.panel_background),
        Highlight("PmenuExtraSel", guifg=colors.text, guibg=colors.element_selected),
        Highlight("PmenuKind", guifg=colors.syntax.type, guibg=colors.panel_background),
        Highlight("PmenuKindSel", guifg=colors.syntax.type, guibg=colors.element_selected),
        Highlight("PmenuMatch", guifg=colors.syntax.function, guibg=colors.panel_background),
        Highlight("PmenuMatchSel", guifg=colors.syntax.function, guibg=colors.element_selected),
        Highlight("PmenuSbar", guibg=colors.scrollbar_track_background),
        Highlight("PmenuSel", guifg=colors.text, guibg=colors.element_selected),
        Highlight("PmenuThumb", guibg=colors.scrollbar_thumb_background),
        Highlight("Question", guifg=colors.syntax.function),
        Highlight(
            "QuickFixLine",
            guifg=colors.text,
            guibg=colors.editor_highlighted_line_background,
        ),
        Highlight("Search", guifg=colors.text, guibg=colors.search_match_background),
        Highlight("SignColumn", guibg=colors.editor_gutter_background),
        Highlight("SpecialKey", guifg=colors.editor_invisible),
        Highlight("SpellBad", gui="undercurl", guisp=colors.error.foreground),
        Highlight("SpellCap", gui="undercurl", guisp=colors.warning.foreground),
        Highlight("SpellLocal", gui="undercurl", guisp=colors.info.foreground),
        Highlight("SpellRare", gui="undercurl", guisp=colors.hint.foreground),
        Highlight("StatusLine", guifg=colors.text, guibg=colors.status_bar_background),
        Highlight("StatusLineNC", guifg=colors.text_muted, guibg=colors.status_bar_background),
        Highlight("VertSplit", guifg=colors.pane_group_border),
        Highlight("Visual", guibg=colors.element_selected),
        Highlight("WarningMsg", guifg=colors.warning.foreground),
        Highlight("WinSeparator", guifg=colors.pane_group_border),
        Highlight("Comment", guifg=colors.syntax.comment, gui="italic"),
        Highlight("Constant", guifg=colors.syntax.constant),
        Highlight("String", guifg=colors.syntax.string),
        Highlight("Character", guifg=colors.syntax.string),
        Highlight("Number", guifg=colors.syntax.number),
        Highlight("Boolean", guifg=colors.syntax.boolean),
        Highlight("Float", guifg=colors.syntax.number),
        Highlight("Identifier", guifg=colors.syntax.variable),
        Highlight("Function", guifg=colors.syntax.function),
        Highlight("Statement", guifg=colors.syntax.keyword),
        Highlight("Conditional", guifg=colors.syntax.keyword),
        Highlight("Repeat", guifg=colors.syntax.keyword),
        Highlight("Label", guifg=colors.syntax.keyword),
        Highlight("Operator", guifg=colors.syntax.punctuation),
        Highlight("Keyword", guifg=colors.syntax.keyword),
        Highlight("Exception", guifg=colors.syntax.keyword),
        Highlight("PreProc", guifg=colors.syntax.attribute),
        Highlight("Include", guifg=colors.syntax.keyword),
        Highlight("Define", guifg=colors.syntax.keyword),
        Highlight("Macro", guifg=colors.syntax.attribute),
        Highlight("PreCondit", guifg=colors.syntax.attribute),
        Highlight("Type", guifg=colors.syntax.type),
        Highlight("StorageClass", guifg=colors.syntax.keyword),
        Highlight("Structure", guifg=colors.syntax.type),
        Highlight("Typedef", guifg=colors.syntax.type),
        Highlight("Special", guifg=colors.syntax.property),
        Highlight("SpecialChar", guifg=colors.syntax.string),
        Highlight("Tag", guifg=colors.syntax.attribute),
        Highlight("Delimiter", guifg=colors.syntax.punctuation),
        Highlight("SpecialComment", guifg=colors.syntax.comment, gui="italic"),
        Highlight("Debug", guifg=colors.debug_breakpoint),
        Highlight("Underlined", guifg=colors.text_accent, gui="underline"),
        Highlight("Ignore", guifg=colors.text_disabled),
        Highlight("Title", guifg=colors.syntax.function, gui="bold"),
        Highlight("Bold", guifg=colors.syntax.type, gui="bold"),
        Highlight("Italic", guifg=colors.syntax.function, gui="italic"),
        Highlight("BoldItalic", guifg=colors.syntax.type, gui="bold,italic"),
        Highlight("ErrorMsg", guifg=colors.error.foreground),
        Highlight("Todo", guifg=colors.warning.foreground, guibg=colors.warning.background),
        Highlight("Added", guifg=colors.created.foreground),
        Highlight("Changed", guifg=colors.modified.foreground),
        Highlight("Removed", guifg=colors.deleted.foreground),
        Highlight("DiffAdd", guifg=colors.created.foreground, guibg=colors.created.background),
        Highlight("DiffChange", guifg=colors.modified.foreground, guibg=colors.modified.background),
        Highlight("DiffDelete", guifg=colors.deleted.foreground, guibg=colors.deleted.background),
        Highlight("DiffText", guifg=colors.info.foreground, guibg=colors.info.background),
        Highlight("markdownH1", guifg=colors.syntax.function, gui="bold"),
        Highlight("markdownH2", guifg=colors.syntax.function, gui="bold"),
        Highlight("markdownH3", guifg=colors.syntax.function, gui="bold"),
        Highlight("markdownH4", guifg=colors.syntax.function, gui="bold"),
        Highlight("markdownH5", guifg=colors.syntax.function, gui="bold"),
        Highlight("markdownH6", guifg=colors.syntax.function, gui="bold"),
        Highlight("markdownHeadingDelimiter", guifg=colors.syntax.punctuation),
        Highlight("markdownRule", guifg=colors.syntax.attribute),
        Highlight("markdownListMarker", guifg=colors.syntax.punctuation),
        Highlight("markdownOrderedListMarker", guifg=colors.syntax.punctuation),
        Highlight("markdownBlockquote", guifg=colors.syntax.comment, gui="italic"),
        Highlight("markdownLinkText", guifg=colors.syntax.function, gui="italic"),
        Highlight("markdownAutomaticLink", guifg=colors.syntax.property),
        Highlight("markdownUrl", guifg=colors.syntax.property),
        Highlight("markdownUrlTitle", guifg=colors.syntax.string),
        Highlight("markdownCode", guifg=colors.syntax.string),
        Highlight("markdownCodeBlock", guifg=colors.syntax.string),
        Highlight("markdownItalic", guifg=colors.syntax.function, gui="italic"),
        Highlight("markdownBold", guifg=colors.syntax.type, gui="bold"),
        Highlight("markdownBoldItalic", guifg=colors.syntax.type, gui="bold,italic"),
        Highlight("markdownStrike", guifg=colors.syntax.comment, gui="strikethrough"),
        Highlight("htmlH1", guifg=colors.syntax.function, gui="bold"),
        Highlight("htmlH2", guifg=colors.syntax.function, gui="bold"),
        Highlight("htmlH3", guifg=colors.syntax.function, gui="bold"),
        Highlight("htmlH4", guifg=colors.syntax.function, gui="bold"),
        Highlight("htmlH5", guifg=colors.syntax.function, gui="bold"),
        Highlight("htmlH6", guifg=colors.syntax.function, gui="bold"),
        Highlight("htmlLink", guifg=colors.syntax.function, gui="underline"),
        Highlight("htmlBold", guifg=colors.syntax.type, gui="bold"),
        Highlight("htmlItalic", guifg=colors.syntax.function, gui="italic"),
        Highlight("htmlBoldItalic", guifg=colors.syntax.type, gui="bold,italic"),
        Highlight("htmlStrike", guifg=colors.syntax.comment, gui="strikethrough"),
    ]

    lines = [
        f'" {palette.scheme} Vim color scheme generated by meowtheme.',
        "highlight clear",
        "if exists('syntax_on')",
        "  syntax reset",
        "endif",
        "if has('termguicolors')",
        "  set termguicolors",
        "endif",
        f"set background={palette.appearance}",
        f"let g:colors_name = '{palette.slug}'",
        "",
    ]
    lines.extend(render_highlight(highlight) for highlight in highlights)
    return "\n".join(lines) + "\n"


def render_highlight(highlight: Highlight) -> str:
    settings = []
    if highlight.guifg is not None:
        settings.append(f"guifg={highlight.guifg}")
    if highlight.guibg is not None:
        settings.append(f"guibg={highlight.guibg}")
    if highlight.gui is not None:
        settings.append(f"gui={highlight.gui}")
    if highlight.guisp is not None:
        settings.append(f"guisp={highlight.guisp}")
    return f"highlight {highlight.group} {' '.join(settings)}"
