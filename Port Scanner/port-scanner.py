import sys
import socket
import pyfiglet
import os # For os.system('cls') for screen clearing
import time # For optional sleep to visualize progress

# --- ASCII Banner ---
def print_banner():
    ascii_banner = pyfiglet.figlet_format("Mini - PySec \nPort Scanner v1")
    print(ascii_banner)
    print("By - @mello-io")
    print("-" * 30 + "\n")


# --- Port Probing Function ---
def probe_port(target_ip, port, timeout=0.5):
    """
    Attempts to connect to a given port on a target IP.
    Returns 0 if the port is open, or a non-zero error code otherwise.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout) # Set the connection timeout
        result = sock.connect_ex((target_ip, port))
        sock.close()
        return result
    except socket.error as e:
        # Catch specific socket errors (e.g., network unreachable)
        # from connect_ex's return, but this handles broader network issues.
        return -1 # Indicate a general error
    except Exception as e:
        # Catch any other unexpected errors during socket creation/setup
        return -2 # Indicate an unexpected error

# --- Get Target IP from User ---
def get_target_ip():
    while True:
        target_input = input("[?] Enter the target IP address or hostname (e.g., 192.168.1.1, example.com): ").strip()
        if not target_input:
            print("[-] Target cannot be empty. Please try again.")
            continue
        
        try:
            # Attempt to resolve hostname to IP address
            resolved_ip = socket.gethostbyname(target_input)
            print(f"[+] Scanning target: {target_input} ({resolved_ip})")
            return resolved_ip
        except socket.gaierror:
            print(f"[-] Error: Could not resolve hostname '{target_input}'. Please check the spelling or network connection.")
        except Exception as e:
            print(f"[-] An unexpected error occurred while resolving target: {e}")


# --- Get Scan Type and Port Range from User ---
def get_scan_type_and_ports():
    while True:
        print("\n[?] Select scan type:")
        print("    1. Top 1024 TCP Ports (Common Services)")
        print("    2. Full TCP Port Scan (1-65535)")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == '1':
            return "Top 1024 Ports", range(1, 1025)
        elif choice == '2':
            print("[!] Warning: A full port scan (1-65535) can take a very long time and be noisy.")
            confirm = input("Are you sure you want to proceed with a full scan? (yes/no): ").strip().lower()
            if confirm == 'yes':
                return "Full Scan", range(1, 65536)
            else:
                print("[-] Full scan cancelled. Please choose again.")
                continue
        else:
            print("[-] Invalid choice. Please enter '1' or '2'.")

# --- Main Port Scanning Logic ---
def run_port_scan():
    """
    Orchestrates the port scanning process.
    """
    print_banner()

    target_ip = get_target_ip()
    scan_type_name, ports_to_scan = get_scan_type_and_ports()

    print(f"\n[+] Starting {scan_type_name} on {target_ip}...")
    print("[+] This may take a while, please be patient.")

    open_ports = []
    total_ports = len(ports_to_scan)
    processed_count = 0
    bar_length = 50 # Length of the progress bar

    for port in ports_to_scan:
        processed_count += 1
        
        response = probe_port(target_ip, port)
        
        if response == 0:
            open_ports.append(port)
            # Clear the current progress line before printing the open port
            sys.stdout.write("\r" + " " * (bar_length + 40) + "\r")
            sys.stdout.flush()
            print(f"[+] Port {port} is OPEN")

        # --- Progress Bar Logic ---
        percentage = (processed_count / total_ports) * 100
        filled_chars = int(bar_length * (processed_count / total_ports))
        
        bar = '#' * filled_chars + '-' * (bar_length - filled_chars)
        
        # Print the progress bar on the same line
        sys.stdout.write(f"\r[{bar}] {percentage:.2f}% ({processed_count}/{total_ports})")
        sys.stdout.flush()

        # Optional: Add a small delay to visualize the progress bar filling
        # time.sleep(0.001) # Very small delay for faster scans

    # --- Scan Completion ---
    # Print a final newline to ensure subsequent output appears on a new line
    print("\n" + "=" * 30)
    if open_ports:
        print("Open Ports Found:")
        print(sorted(open_ports))
    else:
        print("Looks like no ports are open in the scanned range :(")
    print("=" * 30)
    print("[+] Port Scan complete.")

# --- Entry Point ---
if __name__ == "__main__":
    run_port_scan()

