from __future__ import annotations

from dataclasses import dataclass
import re


BASE_KEYS = tuple(f"base{i:02X}" for i in range(16))
LIGHT_NEUTRAL_ORDER = {
    "base00": "base07",
    "base01": "base06",
    "base02": "base05",
    "base03": "base04",
    "base04": "base03",
    "base05": "base02",
    "base06": "base01",
    "base07": "base00",
}
HEX_COLOR_RE = re.compile(r"^#?[0-9a-fA-F]{6}$")
SLUG_PART_RE = re.compile(r"[^a-z0-9]+")


class Base16ParseError(ValueError):
    """Raised when a Base16 scheme cannot be parsed into a complete palette."""


@dataclass(frozen=True)
class HexColor:
    hex: str

    @classmethod
    def parse(cls, key: str, raw: str) -> HexColor:
        value = raw.strip()
        if not HEX_COLOR_RE.fullmatch(value):
            raise Base16ParseError(f"{key} must be a 6-digit hex color")
        return cls("#" + value.removeprefix("#").lower())


@dataclass(frozen=True)
class Base16Palette:
    scheme: str
    author: str
    appearance: str
    colors: dict[str, HexColor]

    @property
    def slug(self) -> str:
        slug = SLUG_PART_RE.sub("-", self.scheme.lower()).strip("-")
        if not slug:
            raise Base16ParseError("scheme must contain at least one alphanumeric character")
        return slug

    @property
    def file_stem(self) -> str:
        return self.scheme.replace(" ", "_")

    def base(self, key: str) -> HexColor:
        canonical = canonical_base_key(key)
        try:
            return self.colors[canonical]
        except KeyError as exc:
            raise Base16ParseError(f"unknown base color: {key}") from exc


def parse_base16_scheme(source: str) -> Base16Palette:
    fields = parse_simple_yaml(source)
    scheme = required_any_string(fields, ("scheme", "name"))
    author = required_string(fields, "author")
    appearance = optional_appearance(fields)
    colors: dict[str, HexColor] = {}

    for key in BASE_KEYS:
        if key not in fields:
            raise Base16ParseError(f"missing required key: {key}")
        colors[key] = HexColor.parse(key, fields[key])

    return Base16Palette(scheme=scheme, author=author, appearance=appearance, colors=colors)


def derive_light_palette(palette: Base16Palette) -> Base16Palette:
    colors = {key: palette.base(LIGHT_NEUTRAL_ORDER.get(key, key)) for key in BASE_KEYS}
    return Base16Palette(
        scheme=light_scheme_name(palette.scheme),
        author=palette.author,
        appearance="light",
        colors=colors,
    )


def light_scheme_name(scheme: str) -> str:
    if scheme.endswith("Dark"):
        return scheme.removesuffix("Dark") + "Light"

    if scheme.endswith("-dark"):
        return scheme.removesuffix("-dark") + "-light"

    return scheme + " Light"


def parse_simple_yaml(source: str) -> dict[str, str]:
    fields: dict[str, str] = {}

    for line_number, line in enumerate(source.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise Base16ParseError(f"line {line_number} must be a key/value pair")

        raw_key, raw_value = stripped.split(":", 1)
        key = raw_key.strip()
        value = unquote(strip_inline_comment(raw_value).strip())
        if not key:
            raise Base16ParseError(f"line {line_number} has an empty key")
        fields[canonical_key(key)] = value

    return fields


def required_string(fields: dict[str, str], key: str) -> str:
    if key not in fields:
        raise Base16ParseError(f"missing required key: {key}")
    value = fields[key].strip()
    if not value:
        raise Base16ParseError(f"{key} must not be empty")
    return value


def required_any_string(fields: dict[str, str], keys: tuple[str, ...]) -> str:
    for key in keys:
        if key in fields:
            return required_string(fields, key)
    raise Base16ParseError(f"missing required key: {keys[0]}")


def optional_appearance(fields: dict[str, str]) -> str:
    appearance = fields.get("appearance", fields.get("variant", "dark")).strip().lower()
    if appearance not in {"dark", "light"}:
        raise Base16ParseError("appearance must be dark or light")
    return appearance


def canonical_key(key: str) -> str:
    if key.lower().startswith("base"):
        return canonical_base_key(key)
    return key


def canonical_base_key(key: str) -> str:
    if len(key) != 6 or key[:4].lower() != "base":
        raise Base16ParseError(f"invalid base key: {key}")
    suffix = key[4:].upper()
    canonical = f"base{suffix}"
    if canonical not in BASE_KEYS:
        raise Base16ParseError(f"invalid base key: {key}")
    return canonical


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def strip_inline_comment(value: str) -> str:
    quote: str | None = None
    escaped = False

    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = quote == '"'
            continue
        if char in {'"', "'"}:
            if quote is None:
                quote = char
            elif quote == char:
                quote = None
            continue
        if char == "#" and quote is None:
            return value[:index]

    return value
