from __future__ import annotations

import json
import unittest

from meowtheme.renderers import artifact_set

from tests.helpers import palette


class OpencodeRendererTest(unittest.TestCase):
    def test_renders_theme_schema_and_core_colors(self) -> None:
        body = artifact_set(palette())["opencode/meowdark.json"]
        payload = json.loads(body)

        self.assertEqual(payload["$schema"], "https://opencode.ai/theme.json")

        theme = payload["theme"]
        self.assertEqual(theme["primary"], "#82aaff")
        self.assertEqual(theme["secondary"], "#c792ea")
        self.assertEqual(theme["accent"], "#89ddff")
        self.assertEqual(theme["error"], "#f07178")
        self.assertEqual(theme["warning"], "#ffcb6b")
        self.assertEqual(theme["success"], "#c3e88d")
        self.assertEqual(theme["info"], "#89ddff")
        self.assertEqual(theme["text"], "#d0d0d0")
        self.assertEqual(theme["textMuted"], "#8a8a8a")
        self.assertEqual(theme["background"], "#121212")
        self.assertEqual(theme["backgroundPanel"], "#1c1c1c")
        self.assertEqual(theme["backgroundElement"], "#303030")
        self.assertEqual(theme["backgroundMenu"], "#303030")
        self.assertEqual(theme["border"], "#686868")
        self.assertEqual(theme["borderActive"], "#82aaff")
        self.assertEqual(theme["borderSubtle"], "#303030")
        self.assertEqual(theme["selectedListItemText"], "#121212")

    def test_renders_diff_markdown_and_syntax_colors(self) -> None:
        body = artifact_set(palette())["opencode/meowdark.json"]
        theme = json.loads(body)["theme"]

        self.assertEqual(theme["diffAdded"], "#c3e88d")
        self.assertEqual(theme["diffRemoved"], "#f07178")
        self.assertEqual(theme["diffContext"], "#8a8a8a")
        self.assertEqual(theme["diffHunkHeader"], "#82aaff")
        self.assertEqual(theme["diffAddedBg"], "#c3e88d24")
        self.assertEqual(theme["diffRemovedBg"], "#f0717824")
        self.assertEqual(theme["diffContextBg"], "#1c1c1c")
        self.assertEqual(theme["markdownHeading"], "#82aaff")
        self.assertEqual(theme["markdownLink"], "#89ddff")
        self.assertEqual(theme["markdownCode"], "#c3e88d")
        self.assertEqual(theme["syntaxComment"], "#686868")
        self.assertEqual(theme["syntaxKeyword"], "#c792ea")
        self.assertEqual(theme["syntaxFunction"], "#82aaff")
        self.assertEqual(theme["syntaxString"], "#c3e88d")
        self.assertEqual(theme["syntaxNumber"], "#f78c6c")
        self.assertEqual(theme["syntaxType"], "#ffcb6b")
        self.assertEqual(theme["syntaxOperator"], "#89ddff")


if __name__ == "__main__":
    unittest.main()
