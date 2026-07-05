from __future__ import annotations

import json
import unittest
from xml.etree import ElementTree
import zipfile
import io

from meowtheme.base16 import derive_light_palette
from meowtheme.renderers.jetbrains import (
    JETBRAINS_PLUGIN_SLUG,
    render_jetbrains,
    render_jetbrains_plugin,
    render_jetbrains_theme,
)

from tests.helpers import palette


class JetBrainsRendererTest(unittest.TestCase):
    def test_renders_theme_json_metadata_and_ui_colors(self) -> None:
        payload = json.loads(render_jetbrains_theme(palette()))

        self.assertEqual(payload["name"], "MeowDark")
        self.assertEqual(payload["author"], "meow")
        self.assertIs(payload["dark"], True)
        self.assertEqual(payload["editorScheme"], "/MeowDark.xml")
        self.assertEqual(payload["ui"]["Button.foreground"], "#d0d0d0")
        self.assertEqual(payload["ui"]["Button.focusedBorderColor"], "#82aaff")
        self.assertEqual(payload["ui"]["Tree.selectionBackground"], "#303030")

    def test_renders_editor_scheme_xml(self) -> None:
        root = ElementTree.fromstring(render_jetbrains(palette(), "JetBrains IDEs"))

        self.assertEqual(root.attrib["name"], "MeowDark")
        self.assertEqual(root.attrib["parent_scheme"], "Darcula")
        self.assertEqual(option_value(root, "CARET_COLOR"), "82aaff")
        self.assertEqual(option_value(root, "CONSOLE_BACKGROUND_KEY"), "121212")
        self.assertEqual(attribute_foreground(root, "DEFAULT_STRING"), "c3e88d")
        self.assertEqual(attribute_foreground(root, "DEFAULT_FUNCTION_CALL"), "82aaff")

    def test_light_editor_scheme_uses_default_parent(self) -> None:
        root = ElementTree.fromstring(render_jetbrains(derive_light_palette(palette()), "IDE"))

        self.assertEqual(root.attrib["parent_scheme"], "Default")

    def test_renders_plugin_zip_with_nested_jar(self) -> None:
        plugin = render_jetbrains_plugin([palette(), derive_light_palette(palette())])

        with zipfile.ZipFile(io.BytesIO(plugin)) as outer_zip:
            outer_names = outer_zip.namelist()
            self.assertEqual(
                outer_names,
                [f"{JETBRAINS_PLUGIN_SLUG}/lib/{JETBRAINS_PLUGIN_SLUG}.jar"],
            )
            jar = outer_zip.read(outer_names[0])

        with zipfile.ZipFile(io.BytesIO(jar)) as jar_zip:
            names = set(jar_zip.namelist())
            self.assertIn("META-INF/plugin.xml", names)
            self.assertIn("MeowDark.theme.json", names)
            self.assertIn("MeowDark.xml", names)
            self.assertIn("MeowLight.theme.json", names)
            self.assertIn("MeowLight.xml", names)
            plugin_xml = jar_zip.read("META-INF/plugin.xml").decode("utf-8")

        self.assertIn('themeProvider id="meowtheme.jetbrains.meowdark"', plugin_xml)
        self.assertIn('themeProvider id="meowtheme.jetbrains.meowlight"', plugin_xml)


def option_value(root: ElementTree.Element, name: str) -> str:
    option = root.find(f"./colors/option[@name='{name}']")
    if option is None:
        raise AssertionError(f"missing option: {name}")
    value = option.attrib.get("value")
    if value is None:
        raise AssertionError(f"missing value for option: {name}")
    return value


def attribute_foreground(root: ElementTree.Element, name: str) -> str:
    option = root.find(f"./attributes/option[@name='{name}']/value/option[@name='FOREGROUND']")
    if option is None:
        raise AssertionError(f"missing foreground attribute: {name}")
    value = option.attrib.get("value")
    if value is None:
        raise AssertionError(f"missing foreground value: {name}")
    return value


if __name__ == "__main__":
    unittest.main()
