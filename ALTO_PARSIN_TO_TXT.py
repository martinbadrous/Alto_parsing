#!/usr/bin/env python3
"""Batch utilities for exporting ALTO XML files to plain-text tables."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Iterable

from alto_parser import AltoParserError, format_records, iter_strings, parse_alto, write_records

LOGGER = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert ALTO XML files to text files containing text geometry.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--input",
        type=Path,
        help="Path to a single ALTO XML file.",
    )
    group.add_argument(
        "--indir",
        type=Path,
        help="Directory containing ALTO XML files (recursively processed).",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output file when using --input.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        help="Output directory when using --indir (defaults to <indir>/parsed).",
    )
    parser.add_argument(
        "--mode",
        choices=("bounding_box", "top_left"),
        default="bounding_box",
        help="Choose between bounding boxes (x_min, y_min, x_max, y_max) or top-left coordinates.",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Encoding used for the generated text files (default: utf-8).",
    )
    parser.add_argument(
        "--no-text",
        action="store_true",
        help="Omit the actual OCR text from the output rows.",
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

    if args.input and not args.output:
        raise SystemExit("--output is required when --input is provided")

    try:
        if args.indir:
            output_dir = args.outdir or args.indir / "parsed"
            process_directory(
                input_dir=args.indir,
                output_dir=output_dir,
                mode=args.mode,
                include_text=not args.no_text,
                encoding=args.encoding,
                separator=args.separator,
            )
        else:
            process_file(
                input_path=args.input,
                output_path=args.output,
                mode=args.mode,
                include_text=not args.no_text,
                encoding=args.encoding,
                separator=args.separator,
            )
    except AltoParserError as exc:
        LOGGER.error("%s", exc)
        return 1

    return 0


def process_directory(
    *,
    input_dir: Path,
    output_dir: Path,
    mode: str,
    include_text: bool,
    encoding: str,
    separator: str,
) -> None:
    xml_files = sorted(p for p in input_dir.rglob("*.xml") if p.is_file())
    if not xml_files:
        LOGGER.warning("No XML files found in %s", input_dir)
        return

    LOGGER.info("Processing %d files from %s", len(xml_files), input_dir)
    for xml_file in xml_files:
        relative = xml_file.relative_to(input_dir)
        output_path = output_dir / relative.with_suffix(".txt")
        try:
            process_file(
                input_path=xml_file,
                output_path=output_path,
                mode=mode,
                include_text=include_text,
                encoding=encoding,
                separator=separator,
                silent=True,
            )
        except AltoParserError as exc:
            LOGGER.error("Failed to parse %s: %s", xml_file, exc)


def process_file(
    *,
    input_path: Path,
    output_path: Path,
    mode: str,
    include_text: bool,
    encoding: str,
    separator: str,
    silent: bool = False,
) -> None:
    try:
        tree, namespace = parse_alto(input_path)
    except AltoParserError:
        if silent:
            raise
        raise

    records = list(iter_strings(tree, namespace))
    formatted = list(_format(records, mode=mode, include_text=include_text, separator=separator))
    write_records(formatted, output_path=output_path, encoding=encoding)
    if not silent:
        LOGGER.info("Wrote %s (%d rows)", output_path, len(formatted))


def _format(
    records: Iterable,
    *,
    mode: str,
    include_text: bool,
    separator: str,
):
    return format_records(records, mode=mode, include_text=include_text, separator=separator)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())

