"""Utilities for parsing ALTO XML files and exporting text geometry.

This module exposes a lightweight API that is reused by the command line
scripts in the repository.  The goal is to convert the ALTO `<String>`
elements into structured records that can then be formatted as top-left
coordinates or bounding boxes.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional, Sequence
import xml.etree.ElementTree as ET

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class AltoString:
    """Container holding the useful attributes of an ALTO `<String>` element."""

    content: str
    hpos: int
    vpos: int
    width: int
    height: int

    @property
    def bottom_right(self) -> tuple[int, int]:
        """Return the bottom-right coordinate of the string's bounding box."""

        return self.hpos + self.width, self.vpos + self.height


class AltoParserError(RuntimeError):
    """Raised when an ALTO document cannot be parsed."""


def parse_alto(path: Path) -> tuple[ET.ElementTree, str]:
    """Parse *path* and return the XML tree alongside its namespace.

    Parameters
    ----------
    path:
        Path to the ALTO XML file.
    """

    try:
        tree = ET.parse(path)
    except (OSError, ET.ParseError) as exc:  # pragma: no cover - defensive branch
        raise AltoParserError(f"Unable to parse '{path}': {exc}") from exc

    root = tree.getroot()
    namespace = _detect_namespace(root)
    return tree, namespace


def _detect_namespace(root: ET.Element) -> str:
    tag = root.tag
    if tag.startswith("{") and "}" in tag:
        return tag.split("}")[0].strip("{")

    # Fallback: inspect xmlns declaration stored in the attributes of the root
    for value in root.attrib.values():
        if value.startswith("{") and value.endswith("}"):
            return value.strip("{}")

    raise AltoParserError("Unable to determine the XML namespace of the document")


def iter_strings(tree: ET.ElementTree, namespace: str) -> Iterator[AltoString]:
    """Yield :class:`AltoString` records for all `<String>` nodes.

    The ALTO specification allows for hyphenated words split across lines.  In
    that case `SUBS_TYPE="HypPart1"` will contain the full word.  We keep the
    behaviour from the legacy scripts by preferring `SUBS_CONTENT` when
    available.
    """

    string_path = f".//{{{namespace}}}TextLine/{{{namespace}}}String"
    for element in tree.iterfind(string_path):
        content = _string_content(element)
        hpos = _safe_int(element.get("HPOS"), "HPOS")
        vpos = _safe_int(element.get("VPOS"), "VPOS")
        width = _safe_int(element.get("WIDTH"), "WIDTH")
        height = _safe_int(element.get("HEIGHT"), "HEIGHT")

        if None in (content, hpos, vpos, width, height):
            # Skip malformed entries while logging enough context to debug.
            LOGGER.debug(
                "Skipping malformed String element: content=%r, hpos=%r, vpos=%r, width=%r, height=%r",
                content,
                hpos,
                vpos,
                width,
                height,
            )
            continue

        yield AltoString(content=content, hpos=hpos, vpos=vpos, width=width, height=height)


def _string_content(element: ET.Element) -> Optional[str]:
    if element.get("SUBS_CONTENT") and element.get("SUBS_TYPE") == "HypPart1":
        return element.get("SUBS_CONTENT")
    return element.get("CONTENT")


def _safe_int(value: Optional[str], field: str) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(float(value))
    except ValueError:  # pragma: no cover - guard against malformed XML
        LOGGER.debug("Unable to convert %s=%r to an integer", field, value)
        return None


def format_records(
    records: Iterable[AltoString],
    mode: str,
    include_text: bool = True,
    separator: str = "\t",
) -> Iterator[str]:
    """Format *records* according to *mode*.

    Parameters
    ----------
    records:
        Iterable of :class:`AltoString` entries.
    mode:
        Either ``"top_left"`` or ``"bounding_box"``.
    include_text:
        When ``True`` the content is prefixed to each line.
    separator:
        Separator used when joining the values.
    """

    mode = mode.lower()
    if mode not in {"top_left", "bounding_box"}:
        raise ValueError("mode must be either 'top_left' or 'bounding_box'")

    for record in records:
        values: list[str]
        if mode == "top_left":
            values = [str(record.hpos), str(record.vpos)]
        else:
            x_max, y_max = record.bottom_right
            values = [str(record.hpos), str(record.vpos), str(x_max), str(y_max)]

        if include_text:
            values.insert(0, record.content or "")

        yield separator.join(values)


def write_records(
    records: Sequence[str],
    output_path: Path,
    encoding: str = "utf-8",
) -> None:
    """Write the formatted strings to *output_path* with a trailing newline."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding=encoding, newline="\n") as handle:
        handle.write("\n".join(records))
        handle.write("\n")

