"""
modules/network_scanner.py — PySec Suite v2.0
ARP-based network host discovery with MAC vendor identification.

v2 enhancements over v1:
  - Static OUI dictionary maps the first 3 MAC octets to manufacturer names —
    adds immediate recon value with no extra network calls (v1 showed IP+MAC only)
  - Tabular results display (IP | MAC | Vendor Hint)
  - Clear permission error message with corrective hint
  - Full integration with display.py and exporter.py

Note: Requires elevated privileges (run as Administrator on Windows,
      or sudo on Linux/macOS) for raw socket access via scapy.
"""

from utils.display import (
    console,
    print_tool_header,
    print_success,
    print_error,
    print_warning,
    print_table,
    print_summary,
)
from utils.exporter import prompt_export, save_report

# v2: Static OUI map for MAC vendor prefix lookup.
#     First 3 octets of MAC (uppercase, colon-delimited) → vendor name.
#     No external API calls needed — fully offline.
OUI_VENDORS = {
    "00:00:0C": "Cisco Systems",
    "00:1A:A0": "Dell",
    "00:50:56": "VMware",
    "00:0C:29": "VMware",
    "00:05:69": "VMware",
    "B8:27:EB": "Raspberry Pi Foundation",
    "DC:A6:32": "Raspberry Pi Foundation",
    "E4:5F:01": "Raspberry Pi Foundation",
    "28:CD:C1": "Raspberry Pi Foundation",
    "00:1B:21": "Intel",
    "00:21:6A": "Intel",
    "8C:EC:4B": "Intel",
    "F4:4D:30": "Intel",
    "00:0D:3A": "Microsoft",
    "00:15:5D": "Microsoft",
    "00:50:F2": "Microsoft",
    "00:17:FA": "Microsoft",
    "F8:FF:C2": "Apple",
    "AC:BC:32": "Apple",
    "F4:F1:5A": "Apple",
    "00:1C:B3": "Apple",
    "3C:D0:F8": "Apple",
    "A4:C3:F0": "Apple",
    "00:1C:42": "Parallels",
    "08:00:27": "VirtualBox",
    "0A:00:27": "VirtualBox",
    "00:03:FF": "Microsoft",
    "00:0F:4B": "Oracle",
    "00:16:3E": "Xen / Citrix",
    "00:1A:4B": "Netgear",
    "20:E5:2A": "Netgear",
    "84:1B:5E": "Netgear",
    "00:14:6C": "Netgear",
    "C0:FF:D4": "TP-Link",
    "EC:08:6B": "TP-Link",
    "14:CC:20": "TP-Link",
    "F4:EC:38": "TP-Link",
    "50:C7:BF": "TP-Link",
    "00:1D:0F": "ASUS",
    "AC:22:0B": "ASUS",
    "04:D4:C4": "ASUS",
    "2C:FD:A1": "ASUS",
    "00:50:BA": "D-Link",
    "1C:BD:B9": "D-Link",
    "B0:C5:54": "D-Link",
    "00:26:18": "D-Link",
    "00:19:5B": "D-Link",
    "00:25:9C": "Cisco-Linksys",
    "00:14:BF": "Cisco-Linksys",
    "C0:C1:C0": "Cisco-Linksys",
    "00:1E:58": "D-Link",
    "F0:7D:68": "Amazon",
    "74:75:48": "Amazon",
    "FC:65:DE": "Amazon",
    "18:74:2E": "Amazon",
    "00:17:88": "Philips Hue",
    "EC:B5:FA": "Philips Hue",
    "00:1A:11": "Google",
    "F4:F5:D8": "Google",
    "3C:5A:B4": "Google",
    "54:60:09": "Google",
}


def _lookup_vendor(mac: str) -> str:
    """Look up the vendor name from the first 3 octets of a MAC address."""
    prefix = mac.upper()[:8]  # e.g. "AA:BB:CC"
    return OUI_VENDORS.get(prefix, "Unknown")


def run():
    print_tool_header("Network Scanner")

    # Late import — scapy is slow to load and requires elevated privileges.
    try:
        from scapy.all import ARP, Ether, conf, srp
    except ImportError:
        print_error("scapy is not installed. Run: pip install scapy")
        return

    # --- 1. List available interfaces ---
    console.print("  [bold cyan]Available network interfaces:[/bold cyan]\n")
    try:
        for iface_name in conf.ifaces:
            console.print(f"    [dim]{iface_name}[/dim]")
    except Exception:
        console.print("  [dim](Could not list interfaces)[/dim]")
    console.print()

    # --- 2. Get interface ---
    interface = console.input("  [bold white]Network interface (e.g. eth0, Wi-Fi):[/bold white] ").strip()
    if not interface:
        print_error("Interface cannot be empty.")
        return

    # --- 3. Get IP range ---
    ip_range = console.input("  [bold white]IP range (CIDR, e.g. 192.168.1.0/24):[/bold white] ").strip()
    if not ip_range:
        print_error("IP range cannot be empty.")
        return
    if "/" not in ip_range:
        print_warning("IP range should be in CIDR notation (e.g. 192.168.1.0/24).")

    # --- 4. Run ARP sweep ---
    console.print(f"\n  [dim]Running ARP sweep on {ip_range} via {interface}...[/dim]\n")

    try:
        broadcast_mac = "ff:ff:ff:ff:ff:ff"
        packet = Ether(dst=broadcast_mac) / ARP(pdst=ip_range)
        answered, _ = srp(packet, timeout=2, iface=interface, inter=0.1, verbose=False)

    except PermissionError:
        print_error("Permission denied — run as Administrator (Windows) or with sudo (Linux/macOS).")
        return
    except OSError as e:
        print_error(f"Interface error: {e}")
        print_warning(f"Check that '{interface}' exists and is active.")
        return
    except Exception as e:
        print_error(f"Unexpected error during scan: {e}")
        return

    # --- 5. Build results with vendor lookup ---
    # v2: OUI lookup adds manufacturer hint — v1 showed raw IP+MAC only.
    results = []
    for _, received in answered:
        ip = received[ARP].psrc
        mac = received[Ether].src
        vendor = _lookup_vendor(mac)
        results.append((ip, mac, vendor))

    results.sort(key=lambda x: [int(o) for o in x[0].split(".")])

    # --- 6. Display results ---
    console.print()
    if results:
        print_table(
            ["IP Address", "MAC Address", "Vendor Hint"],
            results,
            title=f"Network Scan — {ip_range}",
        )
        print_success(f"{len(results)} host(s) discovered")
    else:
        print_error("No active hosts found in the specified range.")

    print_summary(f"{len(results)} hosts discovered on {ip_range}")

    # --- 7. Export ---
    if prompt_export():
        path = save_report(
            tool="Network Scanner",
            target=ip_range.replace("/", "-"),
            settings={"Interface": interface, "Range": ip_range},
            rows=results,
            summary=f"{len(results)} hosts discovered",
        )
        print_success(f"Saved: {path}")
    else:
        console.print("  [dim]Results not saved.[/dim]")
