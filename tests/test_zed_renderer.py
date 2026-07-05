from __future__ import annotations

import json
import unittest

from meowtheme.renderers.zed import render_zed

from tests.helpers import palette


class ZedRendererTest(unittest.TestCase):
    def test_renders_theme_metadata_and_style_colors(self) -> None:
        payload = json.loads(render_zed(palette()))

        self.assertEqual(payload["name"], "MeowDark")
        self.assertEqual(payload["author"], "meow")
        self.assertEqual(len(payload["themes"]), 1)

        theme = payload["themes"][0]
        style = theme["style"]

        self.assertEqual(theme["name"], "MeowDark")
        self.assertEqual(theme["appearance"], "dark")
        self.assertEqual(style["background"], "#121212")
        self.assertEqual(style["editor.foreground"], "#d0d0d0")
        self.assertEqual(style["editor.background"], "#121212")
        self.assertEqual(style["players"][0]["selection"], "#82aaff2b")
        self.assertEqual(style["terminal.ansi.green"], "#c3e88d")

    def test_renders_syntax_colors(self) -> None:
        payload = json.loads(render_zed(palette()))
        syntax = payload["themes"][0]["style"]["syntax"]

        self.assertEqual(syntax["comment"], {"color": "#686868", "font_style": "italic"})
        self.assertEqual(syntax["string"], {"color": "#c3e88d"})
        self.assertEqual(syntax["keyword"], {"color": "#c792ea"})
        self.assertEqual(syntax["function"], {"color": "#82aaff"})
        self.assertEqual(syntax["type"], {"color": "#ffcb6b"})


if __name__ == "__main__":
    unittest.main()
