from __future__ import annotations

import json
import re
import unittest

from meowtheme.renderers import artifact_set

from tests.helpers import palette


OPENCODE_THEME_KEYS = {
    "primary",
    "secondary",
    "accent",
    "error",
    "warning",
    "success",
    "info",
    "text",
    "textMuted",
    "background",
    "backgroundPanel",
    "backgroundElement",
    "border",
    "borderActive",
    "borderSubtle",
    "diffAdded",
    "diffRemoved",
    "diffContext",
    "diffHunkHeader",
    "diffHighlightAdded",
    "diffHighlightRemoved",
    "diffAddedBg",
    "diffRemovedBg",
    "diffContextBg",
    "diffLineNumber",
    "diffAddedLineNumberBg",
    "diffRemovedLineNumberBg",
    "markdownText",
    "markdownHeading",
    "markdownLink",
    "markdownLinkText",
    "markdownCode",
    "markdownBlockQuote",
    "markdownEmph",
    "markdownStrong",
    "markdownHorizontalRule",
    "markdownListItem",
    "markdownListEnumeration",
    "markdownImage",
    "markdownImageText",
    "markdownCodeBlock",
    "syntaxComment",
    "syntaxKeyword",
    "syntaxFunction",
    "syntaxVariable",
    "syntaxString",
    "syntaxNumber",
    "syntaxType",
    "syntaxOperator",
    "syntaxPunctuation",
}

HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")
REFERENCE_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")


def is_opencode_color_value(value: object) -> bool:
    if isinstance(value, int):
        return 0 <= value <= 255
    if isinstance(value, str):
        return (
            value == "none"
            or bool(HEX_COLOR_PATTERN.fullmatch(value))
            or bool(REFERENCE_PATTERN.fullmatch(value))
        )
    if isinstance(value, dict):
        return set(value) == {"dark", "light"} and all(
            is_opencode_color_value(mode_value) for mode_value in value.values()
        )
    return False


class OpencodeRendererTest(unittest.TestCase):
    def test_renders_schema_supported_theme_keys_and_color_values(self) -> None:
        body = artifact_set(palette())["opencode/meowdark.json"]
        payload = json.loads(body)
        theme = payload["theme"]

        invalid_keys = sorted(set(theme) - OPENCODE_THEME_KEYS)
        invalid_values = {
            key: value for key, value in theme.items() if not is_opencode_color_value(value)
        }

        self.assertEqual(
            {"invalid_keys": invalid_keys, "invalid_values": invalid_values},
            {"invalid_keys": [], "invalid_values": {}},
        )

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
        self.assertEqual(theme["border"], "#686868")
        self.assertEqual(theme["borderActive"], "#82aaff")
        self.assertEqual(theme["borderSubtle"], "#303030")

    def test_renders_diff_markdown_and_syntax_colors(self) -> None:
        body = artifact_set(palette())["opencode/meowdark.json"]
        theme = json.loads(body)["theme"]

        self.assertEqual(theme["diffAdded"], "#c3e88d")
        self.assertEqual(theme["diffRemoved"], "#f07178")
        self.assertEqual(theme["diffContext"], "#8a8a8a")
        self.assertEqual(theme["diffHunkHeader"], "#82aaff")
        self.assertEqual(theme["diffAddedBg"], "#303627")
        self.assertEqual(theme["diffRemovedBg"], "#382223")
        self.assertEqual(theme["diffContextBg"], "#1c1c1c")
        self.assertEqual(theme["diffAddedLineNumberBg"], "#3b432e")
        self.assertEqual(theme["diffRemovedLineNumberBg"], "#452829")
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
