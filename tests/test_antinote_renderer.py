from __future__ import annotations

import json
import unittest

from meowtheme.base16 import derive_light_palette
from meowtheme.renderers.antinote import render_antinote

from tests.helpers import palette


class AntinoteRendererTest(unittest.TestCase):
    def test_renders_supported_theme_schema(self) -> None:
        payload = json.loads(render_antinote(palette()))

        self.assertEqual(payload["name"], "meowdark")
        self.assertIs(payload["isDarkTheme"], True)
        self.assertEqual(payload["background"], "#121212")
        self.assertEqual(payload["typeMain"], "#d0d0d0")
        self.assertEqual(payload["accent1Main"], "#82aaff")
        self.assertEqual(payload["typeHighlight"], "#ffcb6b2b")

    def test_renders_light_theme(self) -> None:
        payload = json.loads(render_antinote(derive_light_palette(palette())))

        self.assertEqual(payload["name"], "meowlight")
        self.assertIs(payload["isDarkTheme"], False)
        self.assertEqual(payload["background"], "#ffffff")


if __name__ == "__main__":
    unittest.main()
