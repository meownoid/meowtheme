from __future__ import annotations

import plistlib
import unittest

from meowtheme.renderers import artifact_set
from meowtheme.renderers.xcode import SOURCE_FONT, render_xcode, xcode_color

from tests.helpers import palette


class XcodeRendererTest(unittest.TestCase):
    def test_artifact_set_includes_xcode_color_theme(self) -> None:
        artifacts = artifact_set(palette())

        self.assertIn("xcode/meowdark.xccolortheme", artifacts)

    def test_renders_editor_and_console_colors(self) -> None:
        payload = plistlib.loads(render_xcode(palette()).encode("utf-8"))

        self.assertEqual(payload["DVTFontAndColorVersion"], 1)
        self.assertEqual(payload["DVTLineSpacing"], 1.1)
        self.assertEqual(
            payload["DVTSourceTextBackground"],
            "0.07058823529 0.07058823529 0.07058823529 1",
        )
        self.assertEqual(
            payload["DVTSourceTextSelectionColor"],
            "0.5098039216 0.6666666667 1 0.168627451",
        )
        self.assertEqual(
            payload["DVTConsoleDebuggerOutputTextColor"],
            "0.8156862745 0.8156862745 0.8156862745 1",
        )

    def test_renders_xcode_syntax_colors_and_fonts(self) -> None:
        payload = plistlib.loads(render_xcode(palette()).encode("utf-8"))
        colors = payload["DVTSourceTextSyntaxColors"]
        fonts = payload["DVTSourceTextSyntaxFonts"]

        self.assertEqual(colors["xcode.syntax.comment"], xcode_color("#686868"))
        self.assertEqual(colors["xcode.syntax.string"], xcode_color("#c3e88d"))
        self.assertEqual(colors["xcode.syntax.keyword"], xcode_color("#c792ea"))
        self.assertEqual(colors["xcode.syntax.identifier.function"], xcode_color("#82aaff"))
        self.assertEqual(colors["xcode.syntax.identifier.type"], xcode_color("#ffcb6b"))
        self.assertEqual(set(fonts), set(colors))
        self.assertTrue(all(font == SOURCE_FONT for font in fonts.values()))

    def test_xcode_color_supports_rgb_and_rgba_hex(self) -> None:
        self.assertEqual(xcode_color("#0000ff"), "0 0 1 1")
        self.assertEqual(xcode_color("#ff000080"), "1 0 0 0.5019607843")


if __name__ == "__main__":
    unittest.main()
