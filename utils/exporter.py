"""
utils/exporter.py — PySec Suite v2.0
All TXT export logic lives here.
"""

import os
import re
from datetime import datetime


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")


def ensure_output_dir():
    """Create ./output/ directory if it does not already exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _sanitise(value: str) -> str:
    """Replace characters that are unsafe in filenames with underscores."""
    return re.sub(r"[^\w\-.]", "_", value)


def build_filename(tool: str, target: str) -> str:
    """Generate a standardised export filename.

    Format: {tool}_{target}_{YYYY-MM-DD_HH-MM}.txt
    Special characters in tool/target are sanitised to safe equivalents.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    safe_tool = _sanitise(tool)
    safe_target = _sanitise(target)
    return f"{safe_tool}_{safe_target}_{timestamp}.txt"


def prompt_export() -> bool:
    """Ask the user whether to save the output to a TXT file.

    Returns:
        True if user confirms, False otherwise.
    """
    try:
        answer = input("\n  Save results to TXT? [y/n]: ").strip().lower()
        return answer == "y"
    except (EOFError, KeyboardInterrupt):
        return False


def save_report(
    tool: str,
    target: str,
    settings: dict,
    rows: list,
    summary: str,
) -> str:
    """Write a formatted TXT report to ./output/.

    Args:
        tool:     Human-readable tool name (e.g. "Port Scanner")
        target:   Target string (e.g. "192.168.1.1")
        settings: Dict of key→value pairs for the metadata header
                  (e.g. {"Scan Type": "Top 1024 ports"})
        rows:     List of tuples/lists for the data body
                  (e.g. [("22", "OPEN", "SSH"), ("80", "OPEN", "HTTP")])
        summary:  One-line summary footer (e.g. "4 open ports found / 1024 tested")

    Returns:
        Full path to the saved file.
    """
    ensure_output_dir()
    filename = build_filename(tool, target)
    filepath = os.path.join(OUTPUT_DIR, filename)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    divider = "=" * 44
    thin = "-" * 44

    lines = [
        divider,
        "PySec Suite v2.0 — Operation Report",
        divider,
        f"Tool       : {tool}",
        f"Target     : {target}",
    ]

    for key, value in settings.items():
        label = f"{key:<10} : {value}"
        lines.append(label)

    lines += [
        f"Timestamp  : {timestamp}",
        divider,
        "",
    ]

    # Data rows — auto-format columns based on the widest value per column
    if rows:
        col_count = max(len(row) for row in rows)
        col_widths = [0] * col_count
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        for row in rows:
            row_line = "  ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
            lines.append(row_line)

    lines += [
        "",
        thin,
        f"Summary: {summary}",
        divider,
    ]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return filepath
