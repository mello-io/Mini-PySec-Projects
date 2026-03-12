"""
modules/file_fetcher.py — PySec Suite v2.0
File download with progress display, integrity check, and export.

v2 enhancements over v1:
  - SHA256 checksum computed incrementally during download (no second file pass)
  - Rich progress bar replaces raw sys.stdout.write loop
  - Prompt before overwriting existing files (carried over from v1)
  - Informative error messages for all failure modes
  - Full integration with display.py and exporter.py
"""

import hashlib
import os
import time
from urllib.parse import urlparse

import requests

from utils.display import (
    console,
    print_tool_header,
    print_success,
    print_error,
    print_warning,
    print_summary,
    get_progress_bar,
)
from utils.exporter import prompt_export, save_report


def _derive_filename(url: str) -> str:
    """Derive a safe output filename from a URL."""
    path = urlparse(url).path
    name = path.split("/")[-1]
    if not name or "." not in name:
        return f"downloaded_{int(time.time())}"
    return name


def _human_size(size_bytes: int) -> str:
    """Format a byte count as a human-readable string."""
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def run():
    print_tool_header("File Fetcher")

    # --- 1. Get URL ---
    while True:
        url = console.input("  [bold white]URL to download:[/bold white] ").strip()
        if not url:
            print_error("URL cannot be empty.")
            continue
        if not url.startswith(("http://", "https://")):
            print_error("URL must start with http:// or https://")
            continue
        break

    # --- 2. Get output filename ---
    derived = _derive_filename(url)
    name_input = console.input(
        f"  [bold white]Output filename[/bold white] [dim](Enter for: {derived})[/dim]: "
    ).strip()
    output_filename = name_input if name_input else derived

    # --- 3. Overwrite check ---
    if os.path.exists(output_filename):
        print_warning(f"'{output_filename}' already exists.")
        confirm = console.input("  [yellow]Overwrite? [y/n]:[/yellow] ").strip().lower()
        if confirm != "y":
            console.print("  [dim]Download cancelled.[/dim]")
            return

    # --- 4. Download with progress bar and SHA256 ---
    console.print(f"\n  [dim]Connecting to {url}...[/dim]")

    try:
        response = requests.get(url, allow_redirects=True, stream=True, timeout=15)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print_error(f"HTTP error: {e}")
        return
    except requests.exceptions.ConnectionError:
        print_error("Connection failed — check the URL and your network.")
        return
    except requests.exceptions.Timeout:
        print_error("Request timed out after 15 seconds.")
        return
    except requests.exceptions.RequestException as e:
        print_error(f"Request error: {e}")
        return

    total_size = int(response.headers.get("content-length", 0))
    chunk_size = 8192

    # v2: SHA256 digest is updated incrementally per chunk — no second file pass needed.
    sha256 = hashlib.sha256()
    downloaded = 0

    try:
        with get_progress_bar() as progress:
            task = progress.add_task(
                "Downloading...",
                total=total_size if total_size > 0 else None,
            )
            with open(output_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        sha256.update(chunk)
                        downloaded += len(chunk)
                        progress.advance(task, len(chunk))

    except IOError as e:
        print_error(f"Could not write file: {e}")
        return

    digest = sha256.hexdigest()
    size_str = _human_size(downloaded)

    # --- 5. Display results ---
    console.print()
    print_success(f"Downloaded: [bold white]{output_filename}[/bold white]  ({size_str})")
    console.print(f"  [dim]SHA256:[/dim]  {digest}")
    print_summary(f"File saved to: {os.path.abspath(output_filename)}")

    # --- 6. Export ---
    if prompt_export():
        rows = [
            ("File", output_filename),
            ("Size", size_str),
            ("SHA256", digest),
            ("URL", url),
        ]
        path = save_report(
            tool="File Fetcher",
            target=output_filename,
            settings={"URL": url},
            rows=rows,
            summary=f"Downloaded {size_str} | SHA256: {digest}",
        )
        print_success(f"Saved: {path}")
    else:
        console.print("  [dim]Results not saved.[/dim]")
