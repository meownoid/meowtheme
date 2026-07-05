from __future__ import annotations

import json
import unittest

from meowtheme.base16 import derive_light_palette
from meowtheme.renderers.codex_desktop import CODEX_DESKTOP_THEME_PREFIX, render_codex_desktop

from tests.helpers import palette


class CodexDesktopRendererTest(unittest.TestCase):
    def test_renders_prefixed_compact_json_theme(self) -> None:
        body = render_codex_desktop(palette())

        self.assertTrue(body.startswith(CODEX_DESKTOP_THEME_PREFIX))
        self.assertTrue(body.endswith("\n"))

        payload = json.loads(body.removeprefix(CODEX_DESKTOP_THEME_PREFIX))
        self.assertEqual(payload["codeThemeId"], "one")
        self.assertEqual(payload["variant"], "dark")
        self.assertEqual(payload["theme"]["contrast"], 60)
        self.assertEqual(payload["theme"]["surface"], "#121212")
        self.assertEqual(payload["theme"]["ink"], "#d0d0d0")
        self.assertEqual(payload["theme"]["accent"], "#82aaff")
        self.assertEqual(
            payload["theme"]["semanticColors"],
            {"diffAdded": "#c3e88d", "diffRemoved": "#f07178", "skill": "#c792ea"},
        )

    def test_light_palette_uses_lower_contrast(self) -> None:
        payload = json.loads(
            render_codex_desktop(derive_light_palette(palette())).removeprefix(
                CODEX_DESKTOP_THEME_PREFIX
            )
        )

        self.assertEqual(payload["variant"], "light")
        self.assertEqual(payload["theme"]["contrast"], 45)


if __name__ == "__main__":
    unittest.main()
