<h1> Mini-PySec-Projects </h1>

These are small scale locally Linux/UNIX deployable python projects for offensive and defensive security testing.

These projects are made with guidance from Tryhackme. And if you are a beginner and would like to make something like this too, check in <a href="https://tryhackme.com/module/scripting-for-pentesters"> here </a> for some great steps and methods. Feel free to test these projects locally and share me your thoughts, suggestions and code improvement via my Linkedin.

<p align="center">
<a href="https://www.linkedin.com/in/dmelloderick/">
  <img height="50" src="https://user-images.githubusercontent.com/46517096/166973395-19676cd8-f8ec-4abf-83ff-da8243505b82.png"/>
</a>
  
---
❗Overall Project Phase : 

✅ Planning - 
✅ Design - 
✅ Development & Testing - 
✅ Initial Deployment - 
🛠️ Feature Development - 
⚠️ Code Maintainance

---

Projects in python to;
- Enumerate the target's subdomain & subdirectory files.
- Scan the network to find target systems IP & MAC addresses
- Scan a target to find the open ports
- Download files from the internet
- Cracking hashes
- Key Logging

---

## 🖥️ Prerequisites & Dependency

Before running any of these scripts, ensure you have the latest Python3 and pip installed. It's highly recommended to use a virtual environment to manage dependencies.


1. Create a Virtual Environment (Optional but Recommended):
```
python3 -m venv venv
```

2. Activate the Virtual Environment:
    - Linux/macOS:
      ```
      source venv/bin/activate
      ```
    - Windows:
      ```
      .\venv\Scripts\activate
      ```

3. Install Dependencies:\
   Each project may require specific Python libraries. You can install all common ones used across these projects with:
   ```
   pip install pyfiglet requests scapy keyboard
   ```

   <i>(Note: ` scapy ` and ` keyboard ` might require elevated privileges for installation or execution on some systems.)</i>

---

## 🔍 Subdomain Scanner

This tool reads a list of potential second level domains (SLD) from a file and attempts to resolve them against a specified target domain to identify live subdomains.

> Current version : v1

- Features:
  - Dynamic target domain input via command-line argument.
  - Reads subdomains from a ` subdomains.txt ` file.
  - Identifies and prints valid subdomains.

- How to Use:
  - Save the script as ` subdom-scanner.py `.
  - Create a ` subdomains.txt ` file in the same directory with one subdomain per line (e.g., www, mail, dev).\
    OR\
    Use the preset ` subdomains.txt ` file within the folder.
  - Run the script from your terminal:\
    ```
    python3 subdom-scanner.py example.com
    ```

    <i> (Replace ` example.com ` with your target domain.) </i>

---

## 🔍 Directory Scanner

This tool attempts to find common or hidden subdirectory files on a target website by making HTTP requests based on entries from a wordlist.

> Current Version : v1

- Features:
  - Dynamic target URL input.
  - Dynamic extension scan based from varied choices. 
  - Reads directory/file names from ` wordlist.txt `.
  - Identifies and prints valid subdirectories.

- How to Use:
  - Save the script as ` subdir-scanner.py `.
  - Create a wordlist.txt file in the same directory with common directory/file names (e.g., admin, backup, robots.txt).\
    OR\
    Use the preset ` wordlist.txt ` file within the folder.
  - Run the script from your terminal:
    ```
    python3 subdir-scanner.py example.com
    ```

    <i> (Replace ` example.com ` with your target domain. && Follow the prompts to enter the target URL and wordlist path.) </i>

---

## 🔍 Network Scanner

This script sends ARP requests to a specified IP range on a chosen network interface to identify devices that respond, revealing their IP and MAC addresses.

> Current Version : v1

- Features:
  - Dynamic user input for network interface (e.g., ` eth0 `, ` wlan0 `).
  - Dynamic user input for IP address range (e.g., ` 192.168.1.0/24 `).
  - Lists available interfaces to assist the user.
  - Robust error handling for permissions and invalid interfaces.

- How to Use:
  - Save the script as ` arp-scanner.py `.
  - Run the script with elevated privileges (required for ` scapy `):
    - Linux/macOS:
      ```
      sudo python3 arp_scanner.py
      ```
    - Windows: Run Command Prompt/PowerShell as Administrator, then run;
      ```
      python arp_scanner.py
      ```
  - Follow the prompts to enter your desired interface and IP range.

---

## 🖥️ Port Scanner

A versatile TCP port scanner that allows scanning common or all ports on a target IP address or hostname to determine if they are open, indicating a running service.

> Current Version : v1

- Features:
  - Dynamic target input (IP address or hostname, with resolution).
  - Two scan types:
    - Top 1024 TCP Ports: Scans common, well-known ports.
    - Full TCP Port Scan: Scans all 65535 ports (with a warning confirmation due to time and noise).
  - Progress bar to show scan status.
  - Comprehensive error handling for network issues and invalid inputs.
  - Displays all found open ports.

- How to Use:
  - Save the script as ` port-scanner.py `.
  - Run the script:
    ```
    python3 port_scanner.py
    ```
  - Follow the prompts to enter the target and select the scan type.

---

## 🌐🗄️ File Downloader


A utility to download files from a given URL and saves it to your local machine, showing download progress.

> Current Version : v1

- Features:
  - Dynamic URL input.
  - User defined output filename, with auto-derivation fallback.
  - Handles HTTP redirects.
  - Progress bar for large file downloads.
  - Prompts before overwriting existing files.
  - Robust error handling for network issues and HTTP errors.

- How to Use:
  - Save the script as ` file-fetcher.py `.
  - Run the script:
    ```
    python3 file-fetcher.py
    ```
  - Follow the prompts to enter the URL and a desired filename.

---

## 🔐 Hash Cracker

A versatile hash cracker that takes a cryptographic hash and a wordlist, then tries to match the hash by hashing each word in the list with various algorithms until a match is found.

> Current Version : v1

- Features:
  - Dynamic user input for wordlist file location.
  - Supports multiple hash algorithms (MD5, SHA1, SHA256, SHA512).
  - Validates input hash format and length.
  - Memory-efficient processing for large wordlists.
  - Progress bar to show cracking status.
  - Provides clear output if the password is found or not.

- How to Use:
  - Save the script as ` hash-cracker.py `.
  - Create a ` wordlist.txt ` file (or any name) with one password candidate per line.\
    OR\
    Use ` rockyou.txt ` found within the standard Kali deployment.
  - Run the script:
    ```
    python3 hash-cracker.py
    ```
  - Follow the prompts to enter the wordlist path, select the hash algorithm, and provide the hash to crack.

---

## ⌨️ Keylogger

A basic keylogger, demonstrating keyboard event capture and local logging. It saves the captured event information to a local file, providing a clear, readable output.

## ⚠️⚠️ ETHICAL AND LEGAL WARNING ⚠️⚠️
This tool is developed and shared strictly for educational and isolated (VM environment) testing purposes. Deploying a keylogger on any system without explicit, informed consent of the user and the system owner is illegal and unethical. Ensure you comply with all applicable laws and regulations in your jurisdiction. Use this tool responsibly.

> Current Version : v1

- Features:
  - Logs all pressed keys to ` keylog.txt `.
  - Runs in the background.
  - Converts special keys (e.g., ` space `, ` enter `, ` shift `) into readable strings.
  - Configurable stop hotkey ( ` ctrl+alt+x ` by default).
  - Basic error handling for file writing.

- How to Use:
  - Save the script as ` transcriptor.py `.
  - Crucial: Understand and accept the ethical implications.
  - Run the script with elevated privileges (required for keyboard hooking):
    - Linux/macOS:
      ```
      sudo python3 transcriptor.py
      ```
    - Windows: Run Command Prompt/PowerShell as Administrator:
      ```
      python transcriptor.py
      ```
  - The keylogger will start logging. Press ` Ctrl + Alt + X ` to stop it.
  - Check keylog.txt in the same directory for the logged keystrokes.

---

## 📝 Contributions

Feel free to fork this repository, open issues, or submit pull requests to improve these tools or add new ones.

---

<!--
## 📄 License

This work is licensed under the  
**Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**

📌 *You may view and share this project with proper credit, but you may not modify it or use it commercially.*

🔗 [View License Terms](https://creativecommons.org/licenses/by-nc-nd/4.0/)
-->
