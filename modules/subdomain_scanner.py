"""
modules/subdomain_scanner.py — PySec Suite v2.0
Threaded DNS subdomain enumeration using dnspython.

v2 enhancements over v1:
  - v1 used HTTP requests to probe subdomains — unreliable and slow.
    v2 uses proper DNS resolution via dnspython for accurate results.
  - ThreadPoolExecutor (50 workers) for concurrent DNS lookups —
    reduces scan time on large wordlists from minutes to seconds
  - Returns (subdomain, resolved_ip) tuples with tabular display
  - Result count summary (X found / Y tested)
  - Rich progress bar and TXT export integration
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Tuple

import dns.resolver
import dns.exception

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

MAX_WORKERS = 50
DNS_TIMEOUT = 2.0


def _resolve_subdomain(subdomain: str) -> Optional[Tuple[str, str]]:
    """Attempt DNS A-record resolution for a subdomain.

    Returns (fqdn, ip_address) if resolved, else None.
    """
    resolver = dns.resolver.Resolver()
    resolver.lifetime = DNS_TIMEOUT
    try:
        answers = resolver.resolve(subdomain, "A")
        ip = answers[0].address
        return (subdomain, ip)
    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.NoNameservers,
        dns.exception.Timeout,
        dns.exception.DNSException,
    ):
        return None
    except Exception:
        return None


def run():
    print_tool_header("Subdomain Scanner")

    # --- 1. Get target domain ---
    while True:
        domain = console.input("  [bold white]Target domain (e.g. example.com):[/bold white] ").strip().lower()
        if not domain:
            print_error("Domain cannot be empty.")
            continue
        if "." not in domain:
            print_warning("Domain looks incomplete — expected format: example.com")
        break

    # --- 2. Wordlist path ---
    default_wordlist = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "wordlists", "subdomains.txt"
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

    # --- 3. Load prefixes ---
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        prefixes = [line.strip() for line in f if line.strip()]

    subdomains = [f"{prefix}.{domain}" for prefix in prefixes]
    total = len(subdomains)
    console.print(f"\n  [dim]Testing {total:,} subdomains on {domain}...[/dim]\n")

    # --- 4. Threaded DNS resolution ---
    # v2: Concurrent DNS lookups replace v1's sequential HTTP probing.
    #     50 workers reduce scan time dramatically on large wordlists.
    results = []
    with get_progress_bar() as progress:
        task = progress.add_task("Resolving...", total=total)
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(_resolve_subdomain, sub): sub for sub in subdomains
            }
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                progress.advance(task)

    results.sort(key=lambda x: x[0])

    # --- 5. Display results ---
    console.print()
    if results:
        print_table(
            ["Subdomain", "Resolved IP"],
            results,
            title=f"Subdomain Scan — {domain}",
        )
        print_success(f"{len(results)} subdomain(s) resolved")
    else:
        print_error("No live subdomains found.")

    print_summary(f"{len(results)} found / {total:,} tested")

    # --- 6. Export ---
    if prompt_export():
        path = save_report(
            tool="Subdomain Scanner",
            target=domain,
            settings={"Wordlist": wordlist_path, "Total Tested": str(total)},
            rows=results,
            summary=f"{len(results)} subdomains found / {total:,} tested",
        )
        print_success(f"Saved: {path}")
    else:
        console.print("  [dim]Results not saved.[/dim]")
