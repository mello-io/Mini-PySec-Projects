"""
modules/directory_scanner.py — PySec Suite v2.0
Threaded HTTP directory/file enumeration with status code and size display.

v2 enhancements over v1:
  - v1 was a bare script with no input validation, no error handling,
    and required the target as sys.argv[1] with a fixed wordlist path.
  - ThreadPoolExecutor (30 workers) replaces the sequential per-path loop
  - HTTP status code AND Content-Length displayed per result — not just found/not-found
  - 403 responses included (still useful recon intel — resource exists but is restricted)
  - Rich progress bar and tabular results
  - Extension filter is optional; 'none' scans bare paths
  - Full integration with display.py and exporter.py
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import requests

from utils.display import (
    console,
    print_tool_header,
    print_success,
    print_error,
    print_warning,
    print_table,
    print_summary,
    get_progress_bar,
)
from utils.exporter import prompt_export, save_report

MAX_WORKERS = 30
REQUEST_TIMEOUT = 5
# Status codes considered "found" — 200 success + 403 forbidden (resource exists)
VALID_STATUSES = {200, 204, 301, 302, 307, 308, 401, 403, 405}


def _normalise_url(url: str) -> str:
    """Ensure URL has a scheme; strip trailing slash."""
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url.rstrip("/")


def _human_size(content_length) -> str:
    """Format Content-Length header value as human-readable size."""
    try:
        size = int(content_length)
    except (TypeError, ValueError):
        return "—"
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.0f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def _probe_path(base_url: str, path: str, ext: str) -> tuple:
    """Probe a single path. Returns (full_url, status_code, size) or None."""
    target = f"{base_url}/{path}{ext}"
    try:
        resp = requests.get(target, timeout=REQUEST_TIMEOUT, allow_redirects=False)
        if resp.status_code in VALID_STATUSES:
            size = _human_size(resp.headers.get("Content-Length"))
            return (f"/{path}{ext}", str(resp.status_code), size)
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException:
        return None


def run():
    print_tool_header("Directory Scanner")

    # --- 1. Get target URL ---
    while True:
        url_input = console.input("  [bold white]Target URL (e.g. http://example.com):[/bold white] ").strip()
        if not url_input:
            print_error("URL cannot be empty.")
            continue
        base_url = _normalise_url(url_input)
        parsed = urlparse(base_url)
        if not parsed.netloc:
            print_error("Invalid URL — could not parse host.")
            continue
        break

    # --- 2. Extension filter ---
    console.print("\n  [bold cyan]Extension filter:[/bold cyan]")
    console.print("  [1]  None [dim](bare paths)[/dim]")
    console.print("  [2]  .php")
    console.print("  [3]  .html")
    console.print("  [4]  .txt")
    console.print("  [5]  .bak")
    console.print("  [6]  Custom")
    ext_map = {"1": "", "2": ".php", "3": ".html", "4": ".txt", "5": ".bak"}
    while True:
        ext_choice = console.input("  [bold white]>[/bold white] ").strip()
        if ext_choice in ext_map:
            extension = ext_map[ext_choice]
            break
        elif ext_choice == "6":
            extension = console.input("  [bold white]Enter extension (e.g. .asp):[/bold white] ").strip()
            if not extension.startswith("."):
                extension = "." + extension
            break
        else:
            print_error("Enter 1–6.")

    # --- 3. Wordlist path ---
    default_wordlist = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "wordlists", "wordlist.txt"
    )
    while True:
        path_input = console.input(
            f"  [bold white]Wordlist path[/bold white] [dim](Enter for default)[/dim]: "
        ).strip()
        wordlist_path = path_input if path_input else default_wordlist
        if not os.path.exists(wordlist_path):
            print_error(f"File not found: {wordlist_path}")
            continue
        break

    # --- 4. Load wordlist ---
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        paths = [line.strip() for line in f if line.strip()]

    ext_label = extension if extension else "none"
    console.print(f"\n  [dim]Scanning {base_url} | {len(paths):,} paths | ext: {ext_label}[/dim]\n")

    # --- 5. Threaded scan ---
    # v2: Concurrent HTTP requests replace the sequential loop from v1.
    #     30 workers keep the scan fast without hammering the server.
    results = []
    with get_progress_bar() as progress:
        task = progress.add_task("Scanning...", total=len(paths))
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(_probe_path, base_url, path, extension): path
                for path in paths
            }
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                progress.advance(task)

    results.sort(key=lambda x: x[0])

    # --- 6. Display results ---
    console.print()
    if results:
        # Colour-code status column
        coloured_rows = []
        for path, status, size in results:
            if status.startswith("2"):
                status_display = f"[green]{status}[/green]"
            elif status.startswith("3"):
                status_display = f"[cyan]{status}[/cyan]"
            else:
                status_display = f"[yellow]{status}[/yellow]"
            coloured_rows.append((path, status_display, size))
        print_table(["Path", "Status", "Size"], coloured_rows, title=f"Results — {parsed.netloc}")
        print_success(f"{len(results)} path(s) found")
    else:
        print_error("No valid paths found.")

    print_summary(f"{len(results)} valid paths found / {len(paths):,} tested")

    # --- 7. Export ---
    if prompt_export():
        path = save_report(
            tool="Directory Scanner",
            target=parsed.netloc,
            settings={"URL": base_url, "Extension": ext_label, "Wordlist": wordlist_path},
            rows=[(p, s, sz) for p, s, sz in results],
            summary=f"{len(results)} valid paths found / {len(paths):,} tested",
        )
        print_success(f"Saved: {path}")
    else:
        console.print("  [dim]Results not saved.[/dim]")
