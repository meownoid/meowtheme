from __future__ import annotations

import json
import unittest

from meowtheme.renderers.vscode import render_vscode

from tests.helpers import palette


class VSCodeRendererTest(unittest.TestCase):
    def test_renders_theme_metadata_and_workbench_colors(self) -> None:
        payload = json.loads(render_vscode(palette()))

        self.assertEqual(payload["name"], "MeowDark")
        self.assertEqual(payload["type"], "dark")
        self.assertEqual(payload["colors"]["editor.background"], "#121212")
        self.assertEqual(payload["colors"]["editor.foreground"], "#d0d0d0")
        self.assertEqual(payload["colors"]["editorCursor.foreground"], "#82aaff")
        self.assertEqual(payload["colors"]["editor.selectionBackground"], "#82aaff2b")
        self.assertEqual(payload["colors"]["terminal.ansiGreen"], "#c3e88d")

    def test_renders_token_colors(self) -> None:
        payload = json.loads(render_vscode(palette()))

        by_name = {item["name"]: item for item in payload["tokenColors"]}

        self.assertEqual(by_name["Comment"]["scope"], ["comment"])
        self.assertEqual(by_name["Comment"]["settings"]["foreground"], "#686868")
        self.assertEqual(by_name["String"]["settings"]["foreground"], "#c3e88d")
        self.assertEqual(by_name["Keyword"]["settings"]["foreground"], "#c792ea")
        self.assertEqual(by_name["Function"]["settings"]["foreground"], "#82aaff")


if __name__ == "__main__":
    unittest.main()
