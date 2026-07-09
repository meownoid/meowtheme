from __future__ import annotations

import json
import unittest

from meowtheme.renderers import artifact_set
from meowtheme.renderers.chrome import render_chrome

from tests.helpers import palette


class ChromeRendererTest(unittest.TestCase):
    def test_renders_theme_manifest_metadata(self) -> None:
        payload = json.loads(render_chrome(palette()))

        self.assertEqual(payload["manifest_version"], 3)
        self.assertEqual(payload["version"], "0.1.0")
        self.assertEqual(payload["name"], "MeowDark")
        self.assertEqual(payload["theme"]["colors"]["frame"], [18, 18, 18])

    def test_renders_theme_colors(self) -> None:
        payload = json.loads(render_chrome(palette()))
        colors = payload["theme"]["colors"]

        self.assertEqual(colors["toolbar"], [28, 28, 28])
        self.assertEqual(colors["tab_text"], [208, 208, 208])
        self.assertEqual(colors["tab_background_text"], [138, 138, 138])
        self.assertEqual(colors["bookmark_text"], [208, 208, 208])
        self.assertEqual(colors["ntp_background"], [18, 18, 18])
        self.assertEqual(colors["ntp_text"], [208, 208, 208])
        self.assertEqual(colors["button_background"], [28, 28, 28])

    def test_artifact_set_outputs_unpacked_extension_manifest(self) -> None:
        artifacts = artifact_set(palette())

        self.assertIn("chrome/meowdark/manifest.json", artifacts)


if __name__ == "__main__":
    unittest.main()
