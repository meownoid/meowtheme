from __future__ import annotations

import plistlib
import unittest

from meowtheme.renderers.macos_terminal import render_macos_terminal

from tests.helpers import palette


class MacOSTerminalRendererTest(unittest.TestCase):
    def test_renders_terminal_profile_metadata_and_window_settings(self) -> None:
        payload = plistlib.loads(render_macos_terminal(palette()).encode("utf-8"))

        self.assertEqual(payload["name"], "MeowDark")
        self.assertEqual(payload["type"], "Window Settings")
        self.assertEqual(payload["ProfileCurrentVersion"], 2.09)
        self.assertEqual(payload["columnCount"], 120)
        self.assertEqual(payload["rowCount"], 36)
        self.assertIs(payload["Bell"], False)
        self.assertIs(payload["CursorBlink"], True)

    def test_renders_expected_color_archives(self) -> None:
        payload = plistlib.loads(render_macos_terminal(palette()).encode("utf-8"))

        self.assertEqual(
            ns_rgb(payload["BackgroundColor"]), "0.07058823529 0.07058823529 0.07058823529"
        )
        self.assertEqual(ns_rgb(payload["TextColor"]), "0.8156862745 0.8156862745 0.8156862745")
        self.assertEqual(
            ns_rgb(payload["ANSIGreenColor"]), "0.7647058824 0.9098039216 0.5529411765"
        )
        self.assertEqual(ns_rgb(payload["ANSIBlueColor"]), "0.5098039216 0.6666666667 1")


def ns_rgb(archive: bytes) -> str:
    payload = plistlib.loads(archive)
    ns_color = payload["$objects"][1]
    return ns_color["NSRGB"].decode("ascii").rstrip("\0")


if __name__ == "__main__":
    unittest.main()
