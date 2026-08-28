from __future__ import annotations

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.common import pretty_json, semantic_tokens
from meowtheme.renderers.editor_colors import SELECTION_ALPHA, alpha_hex


def render_antinote(palette: Base16Palette) -> str:
    tokens = semantic_tokens(palette)
    payload = {
        "accent1Main": tokens["blue"],
        "accent1Secondary": tokens["cyan"],
        "accent1Tertiary": tokens["green"],
        "accent2Main": tokens["purple"],
        "accent2Secondary": tokens["purple"],
        "accent3Main": tokens["green"],
        "accent3Secondary": tokens["green"],
        "accent4Main": tokens["orange"],
        "accent4Secondary": tokens["orange"],
        "accent5Main": tokens["red"],
        "accent5Secondary": tokens["red"],
        "background": tokens["background"],
        "backgroundFade": tokens["surface"],
        "gridBold": tokens["muted"],
        "gridClear": tokens["surfaceRaised"],
        "gridSuperlight": tokens["surface"],
        "isDarkTheme": palette.appearance == "dark",
        "name": palette.slug,
        "typeHighlight": alpha_hex(tokens["yellow"], SELECTION_ALPHA),
        "typeHyperLight": tokens["surfaceRaised"],
        "typeLight": tokens["mutedForeground"],
        "typeMain": tokens["foreground"],
        "typeReverse": tokens["background"],
        "typeSubtle": tokens["blue"],
        "typeSubtlePlus": tokens["cyan"],
        "typeSuperlight": tokens["muted"],
    }
    return pretty_json(payload)
