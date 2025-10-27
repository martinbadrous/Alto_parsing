#!/usr/bin/env python3
"""Convenience CLI for processing a single ALTO file."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from ALTO_PARSIN_TO_TXT import process_file


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a single ALTO file to text output.")
    parser.add_argument("input", type=Path, help="Path to the ALTO XML file to parse.")
    parser.add_argument("output", type=Path, help="Destination text file.")
    parser.add_argument(
        "--mode",
        choices=("bounding_box", "top_left"),
        default="bounding_box",
        help="Choose between bounding boxes (x_min, y_min, x_max, y_max) or top-left coordinates.",
    )
    parser.add_argument(
        "--no-text",
        action="store_true",
        help="Omit the OCR text from the output rows.",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Encoding used for the generated text file (default: utf-8).",
    )
    parser.add_argument(
        "--separator",
        default="\t",
        help="Field separator used between columns (default: tab).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging for troubleshooting.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    process_file(
        input_path=args.input,
        output_path=args.output,
        mode=args.mode,
        include_text=not args.no_text,
        encoding=args.encoding,
        separator=args.separator,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())

