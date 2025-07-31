import hashlib
import pyfiglet
import sys
import os # For file existence check and counting lines
import time # For optional sleep to visualize progress

# --- ASCII Banner ---
def print_banner():
    """Prints a cool ASCII banner for the Hash Cracker."""
    ascii_banner = pyfiglet.figlet_format("Mini - PySec  \nHash Cracker v1")
    print(ascii_banner)
    print("By - @mello-io")
    print("-" * 30 + "\n")

# --- Hash Algorithm Mapping ---
# Dictionary to map user input to hashlib functions and expected hash lengths
HASH_ALGORITHMS = {
    'md5': {'func': hashlib.md5, 'length': 32},
    'sha1': {'func': hashlib.sha1, 'length': 40},
    'sha256': {'func': hashlib.sha256, 'length': 64},
    'sha512': {'func': hashlib.sha512, 'length': 128}
}

# --- Main Hash Cracking Function ---
def crack_hash():

    print_banner()

    # --- 1. Get Wordlist File Location ---
    while True:
        wordlist_location = input('[?] Enter wordlist file location: ').strip()
        if not wordlist_location:
            print("[-] Wordlist location cannot be empty. Please try again.")
            continue
        if not os.path.exists(wordlist_location):
            print(f"[-] Error: Wordlist file not found at '{wordlist_location}'. Please check the path.")
            continue
        break # Exit loop if path is valid

    # --- 2. Get Hash Algorithm Choice ---
    selected_algo_info = None
    while selected_algo_info is None:
        print("\n[?] Select hash algorithm:")
        for algo_name in HASH_ALGORITHMS.keys():
            print(f"    - {algo_name.upper()}")
        
        algo_choice = input("Enter your choice (e.g., md5, sha256): ").strip().lower()
        selected_algo_info = HASH_ALGORITHMS.get(algo_choice)
        
        if selected_algo_info is None:
            print("[-] Invalid hash algorithm choice. Please select from the list.")

    hash_algorithm_name = algo_choice
    hash_func = selected_algo_info['func']
    expected_hash_length = selected_algo_info['length']

    # --- 3. Get Hash to be Cracked ---
    while True:
        hash_input = input(f'[?] Enter the {hash_algorithm_name.upper()} hash to be cracked: ').strip()
        if not hash_input:
            print("[-] Hash cannot be empty. Please try again.")
            continue
        if len(hash_input) != expected_hash_length:
            print(f"[-] Error: Expected a {expected_hash_length}-character {hash_algorithm_name.upper()} hash, but got {len(hash_input)} characters.")
            continue
        # Basic check for hex characters (can be expanded)
        if not all(c in '0123456789abcdefABCDEF' for c in hash_input):
            print("[-] Error: Hash contains invalid hexadecimal characters.")
            continue
        break # Exit loop if hash is valid

    print(f"\n[+] Cracking {hash_algorithm_name.upper()} hash: {hash_input}")
    print(f"[+] Using wordlist: {wordlist_location}")

    found_password = False
    total_lines = 0

    # First pass: count lines for progress bar (memory-efficient way)
    try:
        with open(wordlist_location, 'r', encoding='utf-8', errors='ignore') as file:
            for _ in file:
                total_lines += 1
    except IOError as e:
        print(f"[-] Error reading wordlist file for line count: {e}")
        return # Exit function if file can't be read

    print(f"[+] Total words in wordlist: {total_lines}")
    
    processed_count = 0
    bar_length = 50 # Length of the progress bar

    # Second pass: actual cracking
    try:
        with open(wordlist_location, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file: # Read line by line for memory efficiency
                processed_count += 1
                word = line.strip() # Remove newline and other whitespace

                # Hash the word using the selected algorithm
                hash_obj = hash_func(word.encode('utf-8'))
                hashed_pass = hash_obj.hexdigest()

                # --- Progress Bar Logic ---
                percentage = (processed_count / total_lines) * 100
                filled_chars = int(bar_length * (processed_count / total_lines))
                bar = '#' * filled_chars + '-' * (bar_length - filled_chars)
                
                # Print progress bar on the same line
                sys.stdout.write(f"\r[{bar}] {percentage:.2f}% ({processed_count}/{total_lines})")
                sys.stdout.flush()
                # Optional: Add a small delay to visualize the progress bar filling
                time.sleep(0.0001)

                if hashed_pass == hash_input:
                    found_password = True
                    # Clear the progress bar line before printing the result
                    sys.stdout.write("\r" + " " * (bar_length + 40) + "\r")
                    sys.stdout.flush()
                    print(f"\n[+] Found cleartext password! : {word}")
                    break # Exit the loop once found
        
    except IOError as e:
        print(f"\n[-] Error reading wordlist file during cracking: {e}")
    except Exception as e:
        print(f"\n[-] An unexpected error occurred during cracking: {e}")

    # --- Final Output ---
    print("\n" + "=" * 30)
    if not found_password:
        print("[-] Password not found in the provided wordlist.")
    print("=" * 30)
    print("[+] Hash cracking attempt complete.")

# --- Entry Point ---
if __name__ == "__main__":
    crack_hash()

