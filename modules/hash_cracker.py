"""
modules/hash_cracker.py — PySec Suite v2.0
Wordlist-based hash cracking with auto-detection and speed display.

v2 enhancements over v1:
  - Auto-detects algorithm from hash length (no manual selection needed)
  - Fallback to manual selection for ambiguous lengths
  - Rich progress bar with live crack speed (hashes/sec)
  - Elapsed time and candidate count in final summary
  - Full integration with display.py and exporter.py
"""

import hashlib
import os
import time
from typing import Optional

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

# v2: Map hash length → algorithm name for auto-detection.
#     v1 required the user to manually select from a list every time.
LENGTH_TO_ALGO = {
    32: "md5",
    40: "sha1",
    64: "sha256",
    128: "sha512",
}

ALGO_FUNCS = {
    "md5":    hashlib.md5,
    "sha1":   hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


def _detect_algorithm(hash_str: str) -> Optional[str]:
    """Return algorithm name inferred from hash length, or None if ambiguous."""
    return LENGTH_TO_ALGO.get(len(hash_str))


def _validate_hash(hash_str: str) -> bool:
    """Return True if hash_str is a valid hex string."""
    return all(c in "0123456789abcdefABCDEF" for c in hash_str)


def _count_lines(path: str) -> int:
    """Count lines in a file efficiently (needed for progress bar total)."""
    count = 0
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for _ in f:
            count += 1
    return count


def run():
    print_tool_header("Hash Cracker")

    # --- 1. Get hash input ---
    while True:
        hash_input = console.input("  [bold white]Hash to crack:[/bold white] ").strip().lower()
        if not hash_input:
            print_error("Hash cannot be empty.")
            continue
        if not _validate_hash(hash_input):
            print_error("Hash contains invalid characters — expected hex only.")
            continue
        break

    # --- 2. v2: Auto-detect algorithm from hash length ---
    algo = _detect_algorithm(hash_input)
    if algo:
        console.print(f"  [dim]Algorithm detected: [bold cyan]{algo.upper()}[/bold cyan] (length {len(hash_input)})[/dim]")
    else:
        # Fallback: manual selection for unrecognised lengths
        print_warning(f"Cannot auto-detect algorithm from length {len(hash_input)}. Select manually:")
        console.print("  [1] MD5  [2] SHA1  [3] SHA256  [4] SHA512")
        choices = {"1": "md5", "2": "sha1", "3": "sha256", "4": "sha512"}
        while True:
            pick = console.input("  [bold white]>[/bold white] ").strip()
            if pick in choices:
                algo = choices[pick]
                break
            print_error("Invalid choice — enter 1, 2, 3, or 4.")

    hash_func = ALGO_FUNCS[algo]

    # --- 3. Get wordlist path ---
    default_wordlist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "wordlists", "wordlist.txt")
    while True:
        path_input = console.input(
            f"  [bold white]Wordlist path[/bold white] [dim](Enter for default: wordlists/wordlist.txt)[/dim]: "
        ).strip()
        wordlist_path = path_input if path_input else default_wordlist
        if not os.path.exists(wordlist_path):
            print_error(f"File not found: {wordlist_path}")
            continue
        break

    # --- 4. Count lines for progress bar ---
    console.print(f"  [dim]Counting wordlist entries...[/dim]")
    total_lines = _count_lines(wordlist_path)
    console.print(f"  [dim]{total_lines:,} candidates loaded[/dim]\n")

    # --- 5. Crack ---
    found_word = None
    candidates_tested = 0
    start_time = time.time()

    # v2: Rich progress bar replaces the raw sys.stdout.write loop from v1.
    #     Speed (hashes/sec) is computed live from elapsed time.
    with get_progress_bar() as progress:
        task = progress.add_task("Cracking...", total=total_lines)
        try:
            with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    word = line.strip()
                    candidates_tested += 1

                    hashed = hash_func(word.encode("utf-8")).hexdigest()
                    if hashed == hash_input:
                        found_word = word
                        progress.update(task, completed=total_lines)
                        break

                    progress.advance(task)

        except IOError as e:
            print_error(f"Could not read wordlist: {e}")
            return

    elapsed = time.time() - start_time
    speed = int(candidates_tested / elapsed) if elapsed > 0 else 0

    # --- 6. Display results ---
    console.print()
    console.print(f"  [dim]Hash      :[/dim]  {hash_input}")
    console.print(f"  [dim]Algorithm :[/dim]  [bold cyan]{algo.upper()}[/bold cyan]")
    console.print(f"  [dim]Wordlist  :[/dim]  {wordlist_path}")
    console.print()

    if found_word:
        print_success(f"Password found: [bold white]{found_word}[/bold white]")
    else:
        print_error("No match found in wordlist.")

    # v2: Show crack speed and elapsed time — not present in v1.
    print_summary(
        f"Tested: {candidates_tested:,} candidates  |  "
        f"Speed: {speed:,} h/s  |  "
        f"Time: {elapsed:.3f}s"
    )

    # --- 7. Export ---
    if prompt_export():
        target_label = hash_input[:12]
        rows = [(found_word or "NOT FOUND", algo.upper(), f"{candidates_tested:,}", f"{speed:,} h/s", f"{elapsed:.3f}s")]
        path = save_report(
            tool="Hash Cracker",
            target=target_label,
            settings={"Algorithm": algo.upper(), "Wordlist": wordlist_path},
            rows=rows,
            summary=f"{'Cracked' if found_word else 'Not found'} | {candidates_tested:,} tested | {elapsed:.3f}s",
        )
        print_success(f"Saved: {path}")
    else:
        console.print("  [dim]Results not saved.[/dim]")
