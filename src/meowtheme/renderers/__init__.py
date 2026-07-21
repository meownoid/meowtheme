from __future__ import annotations

from pathlib import Path

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.codex import render_codex
from meowtheme.renderers.codex_desktop import render_codex_desktop
from meowtheme.renderers.common import semantic_tokens
from meowtheme.renderers.editor_colors import editor_colors
from meowtheme.renderers.macos_terminal import render_macos_terminal
from meowtheme.renderers.opencode import render_opencode
from meowtheme.renderers.vim import render_vim
from meowtheme.renderers.xcode import render_xcode
from meowtheme.renderers.zed import render_zed


def artifact_set(palette: Base16Palette) -> dict[str, str]:
    artifacts = {
        f"codex-desktop/{palette.slug}.txt": render_codex_desktop(palette),
        f"codex/{palette.slug}.tmTheme": render_codex(palette),
        f"macos-terminal/{palette.file_stem}.terminal": render_macos_terminal(palette),
        f"opencode/{palette.slug}.json": render_opencode(palette),
        f"vim/{palette.slug}.vim": render_vim(palette),
        f"xcode/{palette.slug}.xccolortheme": render_xcode(palette),
        f"zed/{palette.slug}.json": render_zed(palette),
    }
    return artifacts


def render_all(palette: Base16Palette, out_dir: Path) -> list[Path]:
    written: list[Path] = []
    for relative_path, body in sorted(artifact_set(palette).items()):
        target = out_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        written.append(target)
    return written


def render_all_schemes(palettes: list[Base16Palette], out_dir: Path) -> list[Path]:
    written: list[Path] = []
    for palette in palettes:
        for relative_path, body in sorted(artifact_set(palette).items()):
            target = out_dir / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding="utf-8")
            written.append(target)

    return sorted(written)


__all__ = [
    "artifact_set",
    "render_all",
    "render_all_schemes",
    "render_codex",
    "render_codex_desktop",
    "render_macos_terminal",
    "render_opencode",
    "render_vim",
    "render_xcode",
    "render_zed",
    "editor_colors",
    "semantic_tokens",
]
