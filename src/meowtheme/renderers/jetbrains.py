from __future__ import annotations

from collections.abc import Mapping
import io
from xml.sax.saxutils import escape as xml_escape
import zipfile

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.common import pretty_json, without_hash
from meowtheme.renderers.editor_colors import EditorColors, editor_colors


JETBRAINS_PLUGIN_SLUG = "meowtheme-jetbrains-theme"
JETBRAINS_PLUGIN_ARCHIVE = f"jetbrains/{JETBRAINS_PLUGIN_SLUG}.zip"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def render_jetbrains_theme(palette: Base16Palette) -> str:
    colors = editor_colors(palette)
    return pretty_json(
        {
            "name": palette.scheme,
            "author": palette.author,
            "dark": palette.appearance == "dark",
            "editorScheme": f"/{palette.file_stem}.xml",
            "ui": jetbrains_ui_colors(colors),
        }
    )


def render_jetbrains_plugin(palettes: list[Base16Palette]) -> bytes:
    jar_entries: dict[str, bytes] = {
        "META-INF/plugin.xml": render_jetbrains_plugin_xml(palettes).encode("utf-8"),
    }
    for palette in palettes:
        jar_entries[f"{palette.file_stem}.theme.json"] = render_jetbrains_theme(palette).encode(
            "utf-8"
        )
        jar_entries[f"{palette.file_stem}.xml"] = render_jetbrains(
            palette, "JetBrains IDEs"
        ).encode("utf-8")

    jar = zip_entries(jar_entries)
    return zip_entries({f"{JETBRAINS_PLUGIN_SLUG}/lib/{JETBRAINS_PLUGIN_SLUG}.jar": jar})


def render_jetbrains_plugin_xml(palettes: list[Base16Palette]) -> str:
    vendor = xml_escape(palettes[0].author if palettes else "meowtheme")
    providers = "\n".join(
        f'    <themeProvider id="meowtheme.jetbrains.{xml_escape(palette.slug)}" '
        f'path="/{xml_escape(palette.file_stem)}.theme.json"/>'
        for palette in palettes
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<idea-plugin>\n"
        "  <id>meowtheme.jetbrains.theme</id>\n"
        "  <name>MeowTheme</name>\n"
        f"  <vendor>{vendor}</vendor>\n"
        "  <version>1.0.0</version>\n"
        "  <depends>com.intellij.modules.platform</depends>\n"
        "  <description><![CDATA[MeowTheme color themes generated from Base16 by meowtheme.]]></description>\n"
        '  <extensions defaultExtensionNs="com.intellij">\n'
        f"{providers}\n"
        "  </extensions>\n"
        "</idea-plugin>\n"
    )


def zip_entries(entries: Mapping[str, bytes]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, mode="w") as archive:
        for name, body in sorted(entries.items()):
            info = zipfile.ZipInfo(name, ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, body)
    return output.getvalue()


def render_jetbrains(palette: Base16Palette, product: str) -> str:
    colors = editor_colors(palette)
    name = xml_escape(palette.scheme)
    product_comment = xml_escape(f"Generated for {product} from Base16 by meowtheme.")
    parent_scheme = "Default" if palette.appearance == "light" else "Darcula"
    options: Mapping[str, str] = {
        **jetbrains_terminal_color_options(colors),
        "CARET_COLOR": colors.text_accent,
        "CARET_ROW_COLOR": colors.editor_highlighted_line_background,
        "CONSOLE_BACKGROUND_KEY": colors.terminal.background,
        "GUTTER_BACKGROUND": colors.editor_gutter_background,
        "INDENT_GUIDE": colors.editor_indent_guide,
        "LINE_NUMBER_ON_CARET_ROW_COLOR": colors.editor_active_line_number,
        "LINE_NUMBERS_COLOR": colors.editor_line_number,
        "NOTIFICATION_BACKGROUND": colors.surface,
        "READONLY_BACKGROUND": colors.surface,
        "RIGHT_MARGIN_COLOR": colors.editor_wrap_guide,
        "SELECTION_BACKGROUND": colors.element_selected,
        "SELECTION_FOREGROUND": colors.terminal.bright_foreground,
    }
    attributes: Mapping[str, Mapping[str, str]] = {
        **jetbrains_terminal_attributes(colors),
        **jetbrains_syntax_attributes(colors),
        "TEXT": {
            "BACKGROUND": colors.editor_background,
            "FOREGROUND": colors.editor_foreground,
        },
    }
    option_xml = "\n".join(
        f'    <option name="{xml_escape(key)}" value="{without_hash(value)}" />'
        for key, value in sorted(options.items())
    )
    attribute_xml = "\n".join(
        render_attribute(key, value) for key, value in sorted(attributes.items())
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"<!-- {product_comment} -->\n"
        f'<scheme name="{name}" version="142" parent_scheme="{parent_scheme}">\n'
        "  <colors>\n"
        f"{option_xml}\n"
        "  </colors>\n"
        "  <attributes>\n"
        f"{attribute_xml}\n"
        "  </attributes>\n"
        "</scheme>\n"
    )


def jetbrains_terminal_color_options(colors: EditorColors) -> Mapping[str, str]:
    return {
        "BLOCK_TERMINAL_DEFAULT_BACKGROUND": colors.terminal.background,
        "BLOCK_TERMINAL_DEFAULT_FOREGROUND": colors.terminal.foreground,
    }


def jetbrains_terminal_attributes(colors: EditorColors) -> Mapping[str, Mapping[str, str]]:
    terminal = colors.terminal
    classic_console_colors = {
        "CONSOLE_NORMAL_OUTPUT": terminal.foreground,
        "CONSOLE_ERROR_OUTPUT": colors.error.foreground,
        "CONSOLE_SYSTEM_OUTPUT": terminal.dim_foreground,
        "CONSOLE_USER_INPUT": terminal.bright_foreground,
        "CONSOLE_BLACK_OUTPUT": terminal.ansi_black,
        "CONSOLE_RED_OUTPUT": terminal.ansi_red,
        "CONSOLE_GREEN_OUTPUT": terminal.ansi_green,
        "CONSOLE_YELLOW_OUTPUT": terminal.ansi_yellow,
        "CONSOLE_BLUE_OUTPUT": terminal.ansi_blue,
        "CONSOLE_MAGENTA_OUTPUT": terminal.ansi_magenta,
        "CONSOLE_CYAN_OUTPUT": terminal.ansi_cyan,
        "CONSOLE_GRAY_OUTPUT": terminal.ansi_white,
        "CONSOLE_DARKGRAY_OUTPUT": terminal.ansi_bright_black,
        "CONSOLE_RED_BRIGHT_OUTPUT": terminal.ansi_bright_red,
        "CONSOLE_GREEN_BRIGHT_OUTPUT": terminal.ansi_bright_green,
        "CONSOLE_YELLOW_BRIGHT_OUTPUT": terminal.ansi_bright_yellow,
        "CONSOLE_BLUE_BRIGHT_OUTPUT": terminal.ansi_bright_blue,
        "CONSOLE_MAGENTA_BRIGHT_OUTPUT": terminal.ansi_bright_magenta,
        "CONSOLE_CYAN_BRIGHT_OUTPUT": terminal.ansi_bright_cyan,
        "CONSOLE_WHITE_OUTPUT": terminal.ansi_bright_white,
    }
    block_terminal_colors = {
        "BLOCK_TERMINAL_BLACK": terminal.ansi_black,
        "BLOCK_TERMINAL_RED": terminal.ansi_red,
        "BLOCK_TERMINAL_GREEN": terminal.ansi_green,
        "BLOCK_TERMINAL_YELLOW": terminal.ansi_yellow,
        "BLOCK_TERMINAL_BLUE": terminal.ansi_blue,
        "BLOCK_TERMINAL_MAGENTA": terminal.ansi_magenta,
        "BLOCK_TERMINAL_CYAN": terminal.ansi_cyan,
        "BLOCK_TERMINAL_WHITE": terminal.ansi_white,
        "BLOCK_TERMINAL_BLACK_BRIGHT": terminal.ansi_bright_black,
        "BLOCK_TERMINAL_RED_BRIGHT": terminal.ansi_bright_red,
        "BLOCK_TERMINAL_GREEN_BRIGHT": terminal.ansi_bright_green,
        "BLOCK_TERMINAL_YELLOW_BRIGHT": terminal.ansi_bright_yellow,
        "BLOCK_TERMINAL_BLUE_BRIGHT": terminal.ansi_bright_blue,
        "BLOCK_TERMINAL_MAGENTA_BRIGHT": terminal.ansi_bright_magenta,
        "BLOCK_TERMINAL_CYAN_BRIGHT": terminal.ansi_bright_cyan,
        "BLOCK_TERMINAL_WHITE_BRIGHT": terminal.ansi_bright_white,
    }
    return {
        key: {"FOREGROUND": value}
        for key, value in {**classic_console_colors, **block_terminal_colors}.items()
    }


def jetbrains_ui_colors(colors: EditorColors) -> Mapping[str, str]:
    return {
        "*.background": colors.surface_background,
        "Button.background": colors.element_background,
        "Button.default.focusedBorderColor": colors.border_focused,
        "Button.focusedBorderColor": colors.border_focused,
        "Button.foreground": colors.text,
        "CheckBox.foreground": colors.text,
        "Component.borderColor": colors.border,
        "Component.disabledBorderColor": colors.border_variant,
        "Component.focusColor": colors.border_focused,
        "DefaultTabs.background": colors.tab_bar_background,
        "DefaultTabs.inactiveColoredFileBackground": colors.ghost_element_background,
        "DefaultTabs.inactiveMaskColor": colors.ghost_element_background,
        "DefaultTabs.selectedBackground": colors.tab_active_background,
        "DefaultTabs.selectedForeground": colors.text,
        "DefaultTabs.underlineColor": colors.border_selected,
        "DefaultTabs.underlinedTabBackground": colors.tab_active_background,
        "EditorTabs.background": colors.tab_bar_background,
        "EditorTabs.inactiveColoredFileBackground": colors.ghost_element_background,
        "EditorTabs.inactiveMaskColor": colors.ghost_element_background,
        "EditorTabs.selectedBackground": colors.tab_active_background,
        "EditorTabs.selectedForeground": colors.text,
        "EditorTabs.underlineColor": colors.border_selected,
        "EditorTabs.underlinedTabBackground": colors.tab_active_background,
        "Label.disabledForeground": colors.text_disabled,
        "Label.foreground": colors.text,
        "List.background": colors.panel_background,
        "List.foreground": colors.text,
        "List.selectionBackground": colors.element_selected,
        "List.selectionForeground": colors.text,
        "List.selectionInactiveBackground": colors.element_selected,
        "List.selectionInactiveForeground": colors.text,
        "MainToolbar.background": colors.toolbar_background,
        "Menu.background": colors.surface_background,
        "Menu.foreground": colors.text,
        "NavBar.background": colors.surface_background,
        "Panel.background": colors.panel_background,
        "Popup.Advertiser.background": colors.surface_background,
        "Popup.Advertiser.foreground": colors.text_muted,
        "Popup.background": colors.surface_background,
        "Popup.foreground": colors.text,
        "ProgressBar.foreground": colors.text_accent,
        "RadioButton.foreground": colors.text,
        "ScrollBar.Mac.Transparent.thumbColor": colors.scrollbar_thumb_background,
        "ScrollBar.Mac.Transparent.thumbBorderColor": colors.scrollbar_thumb_border,
        "SearchEverywhere.Advertiser.background": colors.surface_background,
        "SearchEverywhere.Header.background": colors.surface_background,
        "SearchEverywhere.List.background": colors.surface_background,
        "SearchEverywhere.List.selectionBackground": colors.element_selected,
        "SearchEverywhere.Tab.selectedBackground": colors.tab_active_background,
        "Separator.separatorColor": colors.border,
        "SidePanel.background": colors.panel_background,
        "StatusBar.background": colors.status_bar_background,
        "Table.background": colors.panel_background,
        "Table.foreground": colors.text,
        "Table.selectionBackground": colors.element_selected,
        "Table.selectionForeground": colors.text,
        "Table.selectionInactiveBackground": colors.element_selected,
        "Table.selectionInactiveForeground": colors.text,
        "TextField.background": colors.background,
        "TextField.foreground": colors.text,
        "TitlePane.background": colors.title_bar_background,
        "TitlePane.inactiveBackground": colors.title_bar_inactive_background,
        "ToolBar.background": colors.toolbar_background,
        "Toolbar.background": colors.toolbar_background,
        "ToolWindow.Header.background": colors.panel_background,
        "ToolWindow.Header.inactiveBackground": colors.panel_background,
        "ToolWindow.HeaderTab.hoverBackground": colors.element_hover,
        "ToolWindow.HeaderTab.hoverInactiveBackground": colors.element_hover,
        "ToolWindow.HeaderTab.inactiveBackground": colors.panel_background,
        "ToolWindow.HeaderTab.selectedBackground": colors.tab_active_background,
        "ToolWindow.HeaderTab.selectedForeground": colors.text,
        "ToolWindow.HeaderTab.underlineColor": colors.border_selected,
        "ToolWindow.HeaderTab.underlinedTabBackground": colors.tab_active_background,
        "ToolWindow.background": colors.panel_background,
        "Tree.background": colors.panel_background,
        "Tree.foreground": colors.text,
        "Tree.hash": colors.panel_indent_guide,
        "Tree.hoverBackground": colors.element_hover,
        "Tree.selectionBackground": colors.element_selected,
        "Tree.selectionForeground": colors.text,
        "Tree.selectionInactiveBackground": colors.element_selected,
        "Tree.selectionInactiveForeground": colors.text,
    }


def jetbrains_syntax_attributes(colors: EditorColors) -> Mapping[str, Mapping[str, str]]:
    syntax = colors.syntax
    foregrounds = {
        "DEFAULT_ATTRIBUTE": syntax.attribute,
        "DEFAULT_BLOCK_COMMENT": syntax.comment,
        "DEFAULT_BRACES": syntax.punctuation,
        "DEFAULT_BRACKETS": syntax.punctuation,
        "DEFAULT_CLASS_NAME": syntax.type,
        "DEFAULT_CLASS_REFERENCE": syntax.type,
        "DEFAULT_COMMA": syntax.punctuation,
        "DEFAULT_CONSTANT": syntax.constant,
        "DEFAULT_DOC_COMMENT": syntax.comment,
        "DEFAULT_DOC_COMMENT_TAG": syntax.attribute,
        "DEFAULT_DOC_COMMENT_TAG_VALUE": syntax.string,
        "DEFAULT_DOC_MARKUP": syntax.comment,
        "DEFAULT_DOT": syntax.punctuation,
        "DEFAULT_ENTITY": syntax.constant,
        "DEFAULT_FUNCTION_CALL": syntax.function,
        "DEFAULT_FUNCTION_DECLARATION": syntax.function,
        "DEFAULT_GLOBAL_VARIABLE": syntax.variable,
        "DEFAULT_IDENTIFIER": syntax.variable,
        "DEFAULT_INSTANCE_FIELD": syntax.property,
        "DEFAULT_INSTANCE_METHOD": syntax.function,
        "DEFAULT_INTERFACE_NAME": syntax.type,
        "DEFAULT_INVALID_STRING_ESCAPE": colors.error.foreground,
        "DEFAULT_KEYWORD": syntax.keyword,
        "DEFAULT_LABEL": syntax.keyword,
        "DEFAULT_LINE_COMMENT": syntax.comment,
        "DEFAULT_LOCAL_VARIABLE": syntax.variable,
        "DEFAULT_METADATA": syntax.attribute,
        "DEFAULT_NUMBER": syntax.number,
        "DEFAULT_OPERATION_SIGN": syntax.punctuation,
        "DEFAULT_PARAMETER": syntax.variable,
        "DEFAULT_PARENTHS": syntax.punctuation,
        "DEFAULT_PREDEFINED_SYMBOL": syntax.constant,
        "DEFAULT_REASSIGNED_LOCAL_VARIABLE": syntax.variable,
        "DEFAULT_REASSIGNED_PARAMETER": syntax.variable,
        "DEFAULT_SEMICOLON": syntax.punctuation,
        "DEFAULT_STATIC_FIELD": syntax.property,
        "DEFAULT_STATIC_METHOD": syntax.function,
        "DEFAULT_STRING": syntax.string,
        "DEFAULT_TAG": syntax.type,
        "DEFAULT_VALID_STRING_ESCAPE": syntax.attribute,
        "PY.ANNOTATION": syntax.type,
        "PY.BRACES": syntax.punctuation,
        "PY.BRACKETS": syntax.punctuation,
        "PY.BUILTIN_NAME": syntax.type,
        "PY.CLASS_DEFINITION": syntax.type,
        "PY.COMMA": syntax.punctuation,
        "PY.DECORATOR": syntax.attribute,
        "PY.DOC_COMMENT": syntax.comment,
        "PY.DOC_COMMENT_TAG": syntax.attribute,
        "PY.DOT": syntax.punctuation,
        "PY.FSTRING_FORMAT_SPEC_NUMBER": syntax.number,
        "PY.FSTRING_FORMAT_SPEC_SPECIAL_CHAR": syntax.attribute,
        "PY.FSTRING_FRAGMENT_BRACES": syntax.attribute,
        "PY.FSTRING_FRAGMENT_COLON": syntax.attribute,
        "PY.FSTRING_FRAGMENT_TYPE_CONVERSION": syntax.attribute,
        "PY.FUNC_DEFINITION": syntax.function,
        "PY.FUNCTION_CALL": syntax.function,
        "PY.INVALID_STRING_ESCAPE": colors.error.foreground,
        "PY.KEYWORD": syntax.keyword,
        "PY.KEYWORD_ARGUMENT": syntax.property,
        "PY.LINE_COMMENT": syntax.comment,
        "PY.LOCAL_VARIABLE": syntax.variable,
        "PY.METHOD_CALL": syntax.function,
        "PY.NESTED_FUNC_DEFINITION": syntax.function,
        "PY.NUMBER": syntax.number,
        "PY.OPERATION_SIGN": syntax.punctuation,
        "PY.PARAMETER": syntax.variable,
        "PY.PARENTHS": syntax.punctuation,
        "PY.PREDEFINED_DEFINITION": syntax.constant,
        "PY.PREDEFINED_USAGE": syntax.constant,
        "PY.SELF_PARAMETER": syntax.variable,
        "PY.STRING.B": syntax.string,
        "PY.STRING.U": syntax.string,
        "PY.TYPE_PARAMETER": syntax.type,
        "PY.VALID_STRING_ESCAPE": syntax.attribute,
    }
    return {key: {"FOREGROUND": value} for key, value in foregrounds.items()}


def render_attribute(name: str, options: Mapping[str, str]) -> str:
    option_xml = "\n".join(
        f'        <option name="{xml_escape(key)}" value="{without_hash(value)}" />'
        for key, value in sorted(options.items())
    )
    return (
        f'    <option name="{xml_escape(name)}">\n'
        "      <value>\n"
        f"{option_xml}\n"
        "      </value>\n"
        "    </option>"
    )
