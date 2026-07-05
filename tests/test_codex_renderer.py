from __future__ import annotations

import plistlib
import unittest

from meowtheme.renderers.codex import render_codex

from tests.helpers import palette


class CodexRendererTest(unittest.TestCase):
    def test_renders_tmtheme_metadata_and_editor_settings(self) -> None:
        payload = plistlib.loads(render_codex(palette()).encode("utf-8"))

        self.assertEqual(payload["name"], "MeowDark")
        self.assertEqual(payload["author"], "meow")
        self.assertEqual(
            payload["settings"][0]["settings"],
            {
                "background": "#121212",
                "caret": "#82aaff",
                "foreground": "#d0d0d0",
                "invisibles": "#686868",
                "lineHighlight": "#1c1c1c",
                "selection": "#82aaff2b",
            },
        )

    def test_renders_core_token_scopes(self) -> None:
        settings = plistlib.loads(render_codex(palette()).encode("utf-8"))["settings"]

        by_name = {item["name"]: item for item in settings[1:]}

        self.assertEqual(by_name["Comment"]["scope"], "comment")
        self.assertEqual(by_name["Comment"]["settings"]["foreground"], "#686868")
        self.assertEqual(by_name["Comment"]["settings"]["fontStyle"], "italic")
        self.assertEqual(by_name["String"]["settings"]["foreground"], "#c3e88d")
        self.assertEqual(by_name["Function"]["settings"]["foreground"], "#82aaff")
        self.assertEqual(by_name["Invalid"]["settings"]["foreground"], "#f07178")


if __name__ == "__main__":
    unittest.main()
