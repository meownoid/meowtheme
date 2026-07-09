from __future__ import annotations

from dataclasses import dataclass

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.common import semantic_tokens


DIFF_BACKGROUND_ALPHA = 0.17
DIFF_LINE_NUMBER_BACKGROUND_ALPHA = 0.23

SELECTION_ALPHA = 0.17
SECONDARY_SELECTION_ALPHA = 0.11


@dataclass(frozen=True)
class EditorSyntaxColors:
    attribute: str
    boolean: str
    comment: str
    constant: str
    constructor: str
    function: str
    keyword: str
    number: str
    property: str
    punctuation: str
    string: str
    type: str
    variable: str


@dataclass(frozen=True)
class EditorStatusColors:
    foreground: str
    background: str
    border: str


@dataclass(frozen=True)
class EditorTerminalColors:
    ansi_background: str
    ansi_black: str
    ansi_blue: str
    ansi_bright_black: str
    ansi_bright_blue: str
    ansi_bright_cyan: str
    ansi_bright_green: str
    ansi_bright_magenta: str
    ansi_bright_red: str
    ansi_bright_white: str
    ansi_bright_yellow: str
    ansi_cyan: str
    ansi_dim_black: str
    ansi_dim_blue: str
    ansi_dim_cyan: str
    ansi_dim_green: str
    ansi_dim_magenta: str
    ansi_dim_red: str
    ansi_dim_white: str
    ansi_dim_yellow: str
    ansi_green: str
    ansi_magenta: str
    ansi_red: str
    ansi_white: str
    ansi_yellow: str
    background: str
    bright_foreground: str
    dim_foreground: str
    foreground: str


@dataclass(frozen=True)
class EditorColors:
    accents: tuple[str, str, str]
    background: str
    border: str
    border_focused: str
    border_selected: str
    border_variant: str
    created: EditorStatusColors
    debug_breakpoint: str
    deleted: EditorStatusColors
    diff_added_background: str
    diff_added_line_number_background: str
    diff_modified_background: str
    diff_removed_background: str
    diff_removed_line_number_background: str
    editor_active_line_background: str
    editor_active_line_number: str
    editor_active_wrap_guide: str
    editor_background: str
    editor_document_highlight_read_background: str
    editor_document_highlight_write_background: str
    editor_foreground: str
    editor_gutter_background: str
    editor_highlighted_line_background: str
    editor_indent_guide: str
    editor_indent_guide_active: str
    editor_invisible: str
    editor_line_number: str
    editor_subheader_background: str
    editor_wrap_guide: str
    elevated_surface_background: str
    element_active: str
    element_background: str
    element_disabled: str
    element_hover: str
    element_selected: str
    error: EditorStatusColors
    ghost_element_active: str
    ghost_element_background: str
    ghost_element_disabled: str
    ghost_element_hover: str
    ghost_element_selected: str
    hint: EditorStatusColors
    icon: str
    icon_accent: str
    icon_disabled: str
    icon_muted: str
    icon_placeholder: str
    info: EditorStatusColors
    link_text_hover: str
    modified: EditorStatusColors
    pane_focused_border: str
    pane_group_border: str
    panel_background: str
    panel_focused_border: str
    panel_indent_guide: str
    panel_indent_guide_active: str
    panel_indent_guide_hover: str
    player_background: str
    player_cursor: str
    player_selection: str
    renamed: EditorStatusColors
    scrollbar_thumb_background: str
    scrollbar_thumb_border: str
    scrollbar_thumb_hover_background: str
    scrollbar_track_background: str
    scrollbar_track_border: str
    search_match_background: str
    secondary_selection: str
    selection: str
    status_bar_background: str
    success: EditorStatusColors
    surface: str
    surface_background: str
    syntax: EditorSyntaxColors
    tab_active_background: str
    tab_inactive_background: str
    tab_bar_background: str
    terminal: EditorTerminalColors
    text: str
    text_accent: str
    text_disabled: str
    text_muted: str
    text_placeholder: str
    title_bar_background: str
    title_bar_inactive_background: str
    toolbar_background: str
    warning: EditorStatusColors
    conflict: EditorStatusColors


def alpha_hex(color: str, alpha: float) -> str:
    alpha_channel = round(alpha * 255)
    return f"{color}{alpha_channel:02x}"


def blend_hex(foreground: str, background: str, alpha: float) -> str:
    foreground_channels = (
        int(foreground[1:3], 16),
        int(foreground[3:5], 16),
        int(foreground[5:7], 16),
    )
    background_channels = (
        int(background[1:3], 16),
        int(background[3:5], 16),
        int(background[5:7], 16),
    )
    channels = (
        round(foreground_channel * alpha + background_channel * (1 - alpha))
        for foreground_channel, background_channel in zip(
            foreground_channels, background_channels, strict=True
        )
    )
    return "#" + "".join(f"{channel:02x}" for channel in channels)


def status(foreground: str, background: str) -> EditorStatusColors:
    return EditorStatusColors(
        foreground=foreground,
        background=background,
        border=foreground,
    )


def editor_colors(palette: Base16Palette) -> EditorColors:
    tokens = semantic_tokens(palette)
    selection = alpha_hex(tokens["blue"], SELECTION_ALPHA)
    secondary_selection = alpha_hex(tokens["blue"], SECONDARY_SELECTION_ALPHA)
    ghost_background = alpha_hex(tokens["foreground"], 0.00)
    syntax_yellow = tokens["brown"] if palette.appearance == "light" else tokens["yellow"]

    return EditorColors(
        accents=(tokens["blue"], tokens["purple"], tokens["cyan"]),
        background=tokens["background"],
        border=tokens["surfaceRaised"],
        border_focused=tokens["blue"],
        border_selected=tokens["blue"],
        border_variant=tokens["surface"],
        conflict=status(tokens["yellow"], tokens["surface"]),
        created=status(tokens["green"], tokens["surface"]),
        debug_breakpoint=tokens["red"],
        deleted=status(tokens["red"], tokens["surface"]),
        diff_added_background=blend_hex(
            tokens["green"], tokens["background"], DIFF_BACKGROUND_ALPHA
        ),
        diff_added_line_number_background=blend_hex(
            tokens["green"], tokens["background"], DIFF_LINE_NUMBER_BACKGROUND_ALPHA
        ),
        diff_modified_background=blend_hex(
            tokens["blue"], tokens["background"], DIFF_BACKGROUND_ALPHA
        ),
        diff_removed_background=blend_hex(
            tokens["red"], tokens["background"], DIFF_BACKGROUND_ALPHA
        ),
        diff_removed_line_number_background=blend_hex(
            tokens["red"], tokens["background"], DIFF_LINE_NUMBER_BACKGROUND_ALPHA
        ),
        editor_active_line_background=tokens["surface"],
        editor_active_line_number=tokens["foreground"],
        editor_active_wrap_guide=tokens["surfaceRaised"],
        editor_background=tokens["background"],
        editor_document_highlight_read_background=secondary_selection,
        editor_document_highlight_write_background=secondary_selection,
        editor_foreground=tokens["foreground"],
        editor_gutter_background=tokens["background"],
        editor_highlighted_line_background=tokens["surface"],
        editor_indent_guide=tokens["surfaceRaised"],
        editor_indent_guide_active=tokens["muted"],
        editor_invisible=tokens["muted"],
        editor_line_number=tokens["muted"],
        editor_subheader_background=tokens["surface"],
        editor_wrap_guide=tokens["surfaceRaised"],
        elevated_surface_background=tokens["surface"],
        element_active=tokens["surfaceRaised"],
        element_background=tokens["surface"],
        element_disabled=tokens["background"],
        element_hover=tokens["surfaceRaised"],
        element_selected=tokens["surfaceRaised"],
        error=status(tokens["red"], tokens["surface"]),
        ghost_element_active=tokens["surfaceRaised"],
        ghost_element_background=ghost_background,
        ghost_element_disabled=tokens["background"],
        ghost_element_hover=tokens["muted"],
        ghost_element_selected=tokens["surfaceRaised"],
        hint=status(tokens["cyan"], tokens["surface"]),
        icon=tokens["foreground"],
        icon_accent=tokens["blue"],
        icon_disabled=tokens["muted"],
        icon_muted=tokens["mutedForeground"],
        icon_placeholder=tokens["muted"],
        info=status(tokens["blue"], tokens["surface"]),
        link_text_hover=tokens["cyan"],
        modified=status(tokens["blue"], tokens["surface"]),
        pane_focused_border=tokens["blue"],
        pane_group_border=tokens["surfaceRaised"],
        panel_background=tokens["surface"],
        panel_focused_border=tokens["blue"],
        panel_indent_guide=tokens["surfaceRaised"],
        panel_indent_guide_active=tokens["muted"],
        panel_indent_guide_hover=tokens["muted"],
        player_background=tokens["background"],
        player_cursor=tokens["mutedForeground"],
        player_selection=selection,
        renamed=status(tokens["purple"], tokens["surface"]),
        scrollbar_thumb_background=tokens["muted"],
        scrollbar_thumb_border=tokens["surfaceRaised"],
        scrollbar_thumb_hover_background=tokens["mutedForeground"],
        scrollbar_track_background=tokens["background"],
        scrollbar_track_border=tokens["surface"],
        search_match_background=tokens["surfaceRaised"],
        secondary_selection=secondary_selection,
        selection=selection,
        status_bar_background=tokens["surface"],
        success=status(tokens["green"], tokens["surface"]),
        surface=tokens["surface"],
        surface_background=tokens["surface"],
        syntax=EditorSyntaxColors(
            attribute=tokens["cyan"],
            boolean=tokens["orange"],
            comment=tokens["muted"],
            constant=tokens["orange"],
            constructor=syntax_yellow,
            function=tokens["blue"],
            keyword=tokens["purple"],
            number=tokens["orange"],
            property=tokens["cyan"],
            punctuation=tokens["foreground"],
            string=tokens["green"],
            type=syntax_yellow,
            variable=tokens["foreground"],
        ),
        tab_active_background=tokens["background"],
        tab_inactive_background=tokens["surface"],
        tab_bar_background=tokens["surface"],
        terminal=EditorTerminalColors(
            ansi_background=tokens["background"],
            ansi_black=tokens["background"],
            ansi_blue=tokens["blue"],
            ansi_bright_black=tokens["muted"],
            ansi_bright_blue=tokens["blue"],
            ansi_bright_cyan=tokens["cyan"],
            ansi_bright_green=tokens["green"],
            ansi_bright_magenta=tokens["purple"],
            ansi_bright_red=tokens["red"],
            ansi_bright_white=tokens["foregroundBright"],
            ansi_bright_yellow=tokens["yellow"],
            ansi_cyan=tokens["cyan"],
            ansi_dim_black=tokens["surface"],
            ansi_dim_blue=tokens["blue"],
            ansi_dim_cyan=tokens["cyan"],
            ansi_dim_green=tokens["green"],
            ansi_dim_magenta=tokens["purple"],
            ansi_dim_red=tokens["red"],
            ansi_dim_white=tokens["mutedForeground"],
            ansi_dim_yellow=tokens["yellow"],
            ansi_green=tokens["green"],
            ansi_magenta=tokens["purple"],
            ansi_red=tokens["red"],
            ansi_white=tokens["foreground"],
            ansi_yellow=tokens["yellow"],
            background=tokens["background"],
            bright_foreground=tokens["foregroundBright"],
            dim_foreground=tokens["mutedForeground"],
            foreground=tokens["foreground"],
        ),
        text=tokens["foreground"],
        text_accent=tokens["blue"],
        text_disabled=tokens["muted"],
        text_muted=tokens["mutedForeground"],
        text_placeholder=tokens["muted"],
        title_bar_background=tokens["surface"],
        title_bar_inactive_background=tokens["surface"],
        toolbar_background=tokens["background"],
        warning=status(tokens["yellow"], tokens["surface"]),
    )
