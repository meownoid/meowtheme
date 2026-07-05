from __future__ import annotations

import argparse
from pathlib import Path
import sys

from meowtheme.base16 import Base16ParseError, derive_light_palette, parse_base16_scheme
from meowtheme.renderers import render_all_schemes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="meowtheme")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="generate theme artifacts")
    generate.add_argument("schemes", nargs="+", type=Path, help="Base16 scheme YAML file")
    generate.add_argument("--out", type=Path, default=Path("output"), help="output directory")

    args = parser.parse_args(argv)

    if args.command == "generate":
        return generate_artifacts(args.schemes, args.out)
    parser.error(f"unknown command: {args.command}")
    return 2


def generate_artifacts(scheme_paths: list[Path], out_dir: Path) -> int:
    try:
        palettes = [
            parse_base16_scheme(scheme_path.read_text(encoding="utf-8"))
            for scheme_path in scheme_paths
        ]
        if len(palettes) == 1:
            palettes = [palettes[0], derive_light_palette(palettes[0])]
        written = render_all_schemes(palettes, out_dir)
    except OSError as exc:
        print(f"meowtheme: {exc}", file=sys.stderr)
        return 1
    except Base16ParseError as exc:
        print(f"meowtheme: invalid Base16 scheme: {exc}", file=sys.stderr)
        return 1

    for path in written:
        print(path)
    return 0
