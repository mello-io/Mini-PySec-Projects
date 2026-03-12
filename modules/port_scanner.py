"""
modules/port_scanner.py — PySec Suite v2.0
Threaded TCP port scanner with service identification and banner grab.

v2 enhancements over v1:
  - ThreadPoolExecutor (100 workers) replaces sequential per-port loop —
    massively reduces scan time on large port ranges
  - socket.getservbyport() maps open ports to well-known service names
    (e.g. 22 → ssh, 80 → http) — v1 reported open/closed only
  - Optional banner grab on open ports to surface service version strings
  - Rich progress bar replaces raw sys.stdout.write loop
  - Scan duration tracked and displayed
  - Full integration with display.py and exporter.py
"""

import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Tuple

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

SOCKET_TIMEOUT = 0.5
BANNER_TIMEOUT = 2.0
MAX_WORKERS = 100


def _resolve_target(target: str) -> Optional[str]:
    """Resolve hostname to IP. Returns IP string or None on failure."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None


def _get_service(port: int) -> str:
    """Return well-known service name for a port, or 'Unknown'."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "Unknown"


def _grab_banner(ip: str, port: int) -> str:
    """Attempt a short recv on an open port to capture service banner."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(BANNER_TIMEOUT)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()
        # Truncate to 50 chars and collapse whitespace for clean table display
        return " ".join(banner[:50].split()) if banner else ""
    except Exception:
        return ""


def _scan_port(ip: str, port: int, do_banner: bool) -> Optional[Tuple[int, str, str]]:
    """Probe a single TCP port. Returns (port, service, banner) if open, else None."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(SOCKET_TIMEOUT)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            service = _get_service(port)
            banner = _grab_banner(ip, port) if do_banner else ""
            return (port, service, banner)
        return None
    except Exception:
        return None


def run():
    print_tool_header("Port Scanner")

    # --- 1. Get target ---
    while True:
        target = console.input("  [bold white]Target IP or hostname:[/bold white] ").strip()
        if not target:
            print_error("Target cannot be empty.")
            continue
        ip = _resolve_target(target)
        if not ip:
            print_error(f"Could not resolve '{target}'. Check spelling or connectivity.")
            continue
        if ip != target:
            console.print(f"  [dim]Resolved: {target} → {ip}[/dim]")
        break

    # --- 2. Scan type ---
    console.print("\n  [bold cyan]Scan type:[/bold cyan]")
    console.print("  [1]  Top 1024 ports [dim](fast)[/dim]")
    console.print("  [2]  Full scan — 65535 ports [dim](slow, noisy)[/dim]")
    while True:
        choice = console.input("  [bold white]>[/bold white] ").strip()
        if choice == "1":
            scan_label = "Top 1024 ports"
            ports = range(1, 1025)
            break
        elif choice == "2":
            print_warning("Full scan may take several minutes and generate significant traffic.")
            confirm = console.input("  [yellow]Confirm? [y/n]:[/yellow] ").strip().lower()
            if confirm == "y":
                scan_label = "Full 65535 ports"
                ports = range(1, 65536)
                break
            console.print("  [dim]Cancelled — choose again.[/dim]")
        else:
            print_error("Enter 1 or 2.")

    # --- 3. Banner grab option ---
    do_banner = console.input("\n  [bold white]Attempt banner grab on open ports? [y/n]:[/bold white] ").strip().lower() == "y"

    # --- 4. Threaded scan ---
    console.print(f"\n  [dim]Scanning {len(list(ports))} ports on {ip}...[/dim]\n")
    open_ports = []
    total = len(list(ports))
    start_time = time.time()

    # v2: Concurrent scanning with ThreadPoolExecutor replaces v1's sequential loop.
    #     100 workers reduce scan time from minutes to seconds on top-1024.
    with get_progress_bar() as progress:
        task = progress.add_task(f"Scanning {ip}...", total=total)
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(_scan_port, ip, port, do_banner): port for port in ports}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
                progress.advance(task)

    elapsed = time.time() - start_time
    open_ports.sort(key=lambda x: x[0])

    # --- 5. Display results ---
    console.print()
    if open_ports:
        headers = ["Port", "State", "Service"] + (["Banner"] if do_banner else [])
        rows = []
        for port, service, banner in open_ports:
            row = [str(port), "[green]OPEN[/green]", service]
            if do_banner:
                row.append(banner)
            rows.append(row)
        print_table(headers, rows, title=f"Scan Results — {ip}")
        print_success(f"{len(open_ports)} open port(s) found on {ip}")
    else:
        print_error(f"No open ports found on {ip} in the scanned range.")

    print_summary(f"{len(open_ports)} open ports found | {total} scanned | {elapsed:.1f}s")

    # --- 6. Export ---
    if prompt_export():
        export_rows = [(str(p), "OPEN", svc, ban) for p, svc, ban in open_ports]
        path = save_report(
            tool="Port Scanner",
            target=ip,
            settings={"Scan Type": scan_label, "Duration": f"{elapsed:.1f}s", "Banner Grab": "Yes" if do_banner else "No"},
            rows=export_rows,
            summary=f"{len(open_ports)} open ports found / {total} tested",
        )
        print_success(f"Saved: {path}")
    else:
        console.print("  [dim]Results not saved.[/dim]")
