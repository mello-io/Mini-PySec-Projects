import sys
import pyfiglet
from scapy.all import *

# --- ASCII Banner ---
def print_banner():
    ascii_banner = pyfiglet.figlet_format("Mini - PySec \nARP Scanner v1")
    print(ascii_banner)
    print("By - @mello-io")
    print("-" * 30) # Separator for readability


# --- Main Scanner Function ---
def run_arp_scan():

    print_banner()

    # --- 1. Get Network Interface from User ---
    # List available interfaces to assist the user
    print("[+] Available network interfaces (may vary by OS/setup):")
    # scapy.conf.ifaces provides a dictionary of interfaces
    # printing the names for ease and simplicity
    for iface_name in conf.ifaces:
        print(f"    - {iface_name}")
    print("\n")

    interface = input("[?] Enter the network interface to scan on (e.g., eth0, wlan0, en0): ").strip()
    if not interface:
        print("[-] Interface cannot be empty. Exiting.")
        sys.exit(1)

    # --- 2. Get IP Range from User ---
    ip_range = input("[?] Enter the IP address range to scan (e.g., 192.168.1.0/24, 10.0.0.1-254): ").strip()
    if not ip_range:
        print("[-] IP range cannot be empty. Exiting.")
        sys.exit(1)

    # Basic validation for IP range format (⚠️ can be expanded)
    if "/" not in ip_range and "-" not in ip_range:
        print("[-] Warning: IP range format might be incorrect. Please use CIDR (e.g., 192.168.1.0/24) or range (e.g., 192.168.1.1-254).")
        # Further validation can be added!

    print(f"\n[+] Starting ARP scan on interface: '{interface}' for IP range: '{ip_range}'")
    print("[+] Please ensure you have sufficient permissions (e.g., run using sudo or as root/administrator).")

    broadcastMac = "ff:ff:ff:ff:ff:ff" # Standard broadcast MAC address

    # --- Packet Construction ---
    packet = Ether(dst=broadcastMac)/ARP(pdst = ip_range)

    # --- Perform the Scan ---
    try:
        # srp() sends packets at Layer 2 and returns answered and unanswered packets
        ans, unans = srp(packet, timeout=2, iface=interface, inter=0.1, verbose=False)
        # verbose=False suppresses scapy's default output for cleaner console.

        print("\n[+] Scan Results:")
        print("------------------------------------")
        if ans:
            for send, receive in ans:
                # sprintf allows powerful formatting of packet fields
                print(receive.sprintf(r"%Ether.src% - %ARP.psrc%"))
        else:
            print("No active hosts found in the specified range or interface issues.")
        print("------------------------------------")

    except PermissionError:
        print("\n[-] Error: Permission denied. You likely need to run this script with root/administrator privileges.")
        print("    Try: sudo python3 arp-scanner.py")
    except OSError as e:
        # Catches errors like "No such device" if the interface is wrong
        print(f"\n[-] Error during scan: {e}")
        print(f"    Please check if interface '{interface}' exists and is active.")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"\n[-] An unexpected error occurred: {e}")

    print("\n[+] ARP Scan complete.")

# --- Entry Point ---
if __name__ == "__main__":
    run_arp_scan()
