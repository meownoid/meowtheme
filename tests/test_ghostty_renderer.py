from __future__ import annotations

import unittest

from meowtheme.base16 import derive_light_palette
from meowtheme.renderers import artifact_set
from meowtheme.renderers.ghostty import render_ghostty

from tests.helpers import palette


class GhosttyRendererTest(unittest.TestCase):
    def test_artifact_set_includes_ghostty_theme(self) -> None:
        self.assertIn("ghostty/meowdark", artifact_set(palette()))

    def test_renders_terminal_colors(self) -> None:
        body = render_ghostty(palette())

        self.assertIn("background = #121212\n", body)
        self.assertIn("foreground = #d0d0d0\n", body)
        self.assertIn("cursor-color = #d0d0d0\n", body)
        self.assertIn("cursor-text = #121212\n", body)
        self.assertIn("selection-background = #303030\n", body)
        self.assertIn("palette = 0=#1c1c1c\n", body)
        self.assertIn("palette = 8=#686868\n", body)
        self.assertIn("palette = 15=#ffffff\n", body)

    def test_renders_light_theme(self) -> None:
        body = render_ghostty(derive_light_palette(palette()))

        self.assertIn("background = #ffffff\n", body)
        self.assertIn("foreground = #303030\n", body)
        self.assertIn("palette = 0=#e8e8e8\n", body)


if __name__ == "__main__":
    unittest.main()
