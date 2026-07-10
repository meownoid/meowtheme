from __future__ import annotations

import plistlib

from meowtheme.base16 import Base16Palette
from meowtheme.renderers.common import semantic_tokens


def render_macos_terminal(palette: Base16Palette) -> str:
    tokens = semantic_tokens(palette)
    terminal_profile = {
        "ANSIBlackColor": ns_color_archive(tokens["background"]),
        "ANSIBlueColor": ns_color_archive(tokens["blue"]),
        "ANSIBrightBlackColor": ns_color_archive(tokens["muted"]),
        "ANSIBrightBlueColor": ns_color_archive(tokens["blue"]),
        "ANSIBrightCyanColor": ns_color_archive(tokens["cyan"]),
        "ANSIBrightGreenColor": ns_color_archive(tokens["green"]),
        "ANSIBrightMagentaColor": ns_color_archive(tokens["purple"]),
        "ANSIBrightRedColor": ns_color_archive(tokens["red"]),
        "ANSIBrightWhiteColor": ns_color_archive(tokens["foregroundBright"]),
        "ANSIBrightYellowColor": ns_color_archive(tokens["yellow"]),
        "ANSICyanColor": ns_color_archive(tokens["cyan"]),
        "ANSIGreenColor": ns_color_archive(tokens["green"]),
        "ANSIMagentaColor": ns_color_archive(tokens["purple"]),
        "ANSIRedColor": ns_color_archive(tokens["red"]),
        "ANSIWhiteColor": ns_color_archive(tokens["foreground"]),
        "ANSIYellowColor": ns_color_archive(tokens["yellow"]),
        "BackgroundColor": ns_color_archive(tokens["background"]),
        "Bell": False,
        "CursorBlink": True,
        "CursorColor": ns_color_archive(tokens["mutedForeground"]),
        "CursorType": 0,
        "DisableANSIColor": False,
        "ProfileCurrentVersion": 2.09,
        "SelectionColor": ns_color_archive(tokens["muted"]),
        "ShowActiveProcessInTitle": True,
        "ShowCommandKeyInTitle": False,
        "ShowDimensionsInTitle": False,
        "ShowRepresentedURLInTitle": True,
        "ShowRepresentedURLPathInTitle": False,
        "ShowShellCommandInTitle": False,
        "ShowTTYNameInTitle": False,
        "ShowWindowSettingsNameInTitle": False,
        "TextBoldColor": ns_color_archive(tokens["foregroundBright"]),
        "TextColor": ns_color_archive(tokens["foreground"]),
        "VisualBellOnlyWhenMuted": False,
        "columnCount": 120,
        "name": palette.scheme,
        "rowCount": 36,
        "shellExitAction": 2,
        "type": "Window Settings",
    }
    return plistlib.dumps(
        terminal_profile,
        fmt=plistlib.FMT_XML,
        sort_keys=True,
    ).decode("utf-8")


def ns_color_archive(hex_color: str) -> bytes:
    red, green, blue = rgb_components(hex_color)
    rgb = f"{red:.10g} {green:.10g} {blue:.10g}\0".encode("ascii")
    archive = {
        "$version": 100000,
        "$archiver": "NSKeyedArchiver",
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {
                "NSRGB": rgb,
                "NSColorSpace": 2,
                "$class": plistlib.UID(2),
            },
            {
                "$classname": "NSColor",
                "$classes": ["NSColor", "NSObject"],
            },
        ],
    }
    return plistlib.dumps(archive, fmt=plistlib.FMT_BINARY, sort_keys=True)


def rgb_components(hex_color: str) -> tuple[float, float, float]:
    value = hex_color.removeprefix("#")
    red = int(value[0:2], 16) / 255
    green = int(value[2:4], 16) / 255
    blue = int(value[4:6], 16) / 255
    return red, green, blue
