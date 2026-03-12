import requests
import sys
import os # For path manipulation and checking file existence
import time # For progress bar
import pyfiglet

# --- ASCII Banner ---
def print_banner():
    ascii_banner = pyfiglet.figlet_format("Mini - PySec \nFile Fetcher v1")
    print(ascii_banner)
    print("By - @mello-io")
    print("-" * 30 + "\n")


# --- File Downloader Function ---
def download_file(url, output_filename=None, timeout=10):
    """
    Downloads a file from a given URL with a progress bar and error handling.

    Args: 
        url (str): The URL of the file to download.
        output_filename (str, optional): The name to save the file as. | If None, tries to derive from URL.
        timeout (int): Timeout for the request in seconds.
    """
    print(f"[+] Attempting to download from: {url}")

    try:
        # 1. Add timeout and stream=True for chunked download
        response = requests.get(url, allow_redirects=True, stream=True, timeout=timeout)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx) (URL Error Handling)

        # 2. Determine output filename
        if output_filename is None:
            # Basic attempt to get filename from URL, needs more robust sanitization ⚠️
            # For security, a user-provided filename is safer. ❗
            output_filename = url.split('/')[-1]
            if not output_filename or '.' not in output_filename:
                # Fallback if URL doesn't provide a clear filename
                output_filename = "downloaded_file" + str(int(time.time())) 
                print(f"[*] Could not determine filename from URL. Saving as: {output_filename}")
            else:
                print(f"[+] Derived filename from URL: {output_filename}")

        # 3. Handle existing files
        if os.path.exists(output_filename):
            confirm = input(f"[?] File '{output_filename}' already exists. Overwrite? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("[-] Download cancelled by user. File not overwritten.")
                return

        # 4. Get total file size for progress bar
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192 # 8 KB chunks
        downloaded_size = 0
        
        bar_length = 50 # Length of the progress bar
        
        print(f"[+] Saving to: {output_filename}")
        print("[+] Starting download...")

        # 5. Download in chunks with progress bar
        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # Progress Bar Logic
                    if total_size > 0: # Only show percentage if total size is known
                        percentage = (downloaded_size / total_size) * 100
                        filled_chars = int(bar_length * (downloaded_size / total_size))
                        bar = '#' * filled_chars + '-' * (bar_length - filled_chars)
                        sys.stdout.write(f"\r[{bar}] {percentage:.2f}% ({downloaded_size}/{total_size} bytes)")
                    else:
                        # If content-length is not available, just show downloaded bytes
                        sys.stdout.write(f"\r[+] Downloaded: {downloaded_size} bytes")
                    sys.stdout.flush()
        
        print("\n[+] Download complete!")

    except requests.exceptions.HTTPError as errh:
        print(f"[-] HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"[-] Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"[-] Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"[-] An unexpected error occurred: {err}")
    except IOError as e:
        print(f"[-] Error writing file to disk: {e}")
    except Exception as e:
        print(f"[-] An unhandled error occurred: {e}")

# --- Main Logic ---
def main():
    print_banner()

    # Get URL from user
    url = input("[?] Enter the URL of the file to download: ").strip()
    if not url:
        print("[-] URL cannot be empty. Exiting.")
        sys.exit(1)

    # Get output filename from user
    output_name_input = input("[?] Enter desired output filename (press Enter to auto-derive): ").strip()
    output_filename = output_name_input if output_name_input else None

    download_file(url, output_filename)

# --- Entry Point ---
if __name__ == "__main__":
    main()
