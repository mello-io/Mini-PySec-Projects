<h1>PySec Suite — v2.0</h1>

A unified Python CLI security toolkit. Six tools, one entry point, consistent output, optional TXT export on every operation.

<p align="center">
<a href="https://www.linkedin.com/in/dmelloderick/">
  <img height="50" src="https://user-images.githubusercontent.com/46517096/166973395-19676cd8-f8ec-4abf-83ff-da8243505b82.png"/>
</a>

---

❗Overall Project Phase :

✅ Planning -
✅ Design -
✅ Development & Testing -
✅ v1 Deployment -
✅ v2 Feature Development -
✅ v2 Integration & Polish

---

## What's New in v2.0

v1 was six standalone scripts in separate folders — each with its own banner, its own argument style, no shared output format. v2 unifies everything:

| | v1 | v2 |
| --- | --- | --- |
| Entry point | Navigate to folder, run individual script | `python main.py` — single menu |
| Output | Plain `print()` statements | Rich tables, panels, colour, progress bars |
| Export | None | Optional TXT export on every tool |
| Subdomain Scanner | HTTP probing (slow, inaccurate) | DNS resolution via `dnspython` + 50 threads |
| Directory Scanner | Sequential, binary found/not-found | 30 threads, HTTP status code + size per result |
| Port Scanner | Sequential, no service names | 100 threads, service names, optional banner grab |
| Hash Cracker | Manual algorithm selection | Auto-detects algorithm from hash length |
| File Fetcher | Download + size only | SHA256 checksum computed during download |
| Network Scanner | IP + MAC only | IP + MAC + vendor hint (61-entry OUI map) |

---

## Prerequisites

- Python 3.8+
- pip

> Network Scanner requires elevated privileges (`sudo` on Linux/macOS, run as Administrator on Windows) for raw socket access via scapy.

---

## Install

```bash
git clone https://github.com/mello-io/Mini-PySec-Projects.git
cd Mini-PySec-Projects

python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
.\venv\Scripts\activate

pip install -r requirements.txt
```

---

## Launch

```bash
python main.py
```

```text
    ____        _____              _____       _ __
   / __ \__  __/ ___/___  _____   / ___/__  __(_) /____
  / /_/ / / / /\__ \/ _ \/ ___/   \__ \/ / / / / __/ _ \
 / ____/ /_/ /___/ /  __/ /__    ___/ / /_/ / / /_/  __/
/_/    \__, //____/\___/\___/   /____/\__,_/_/\__/\___/
      /____/
  v2.0 | Security Toolkit | Educational Use Only

  Select a tool:

  [1]  Subdomain Scanner
  [2]  Directory Scanner
  [3]  Network Scanner
  [4]  Port Scanner
  [5]  File Fetcher
  [6]  Hash Cracker
  [0]  Exit
```

---

## Tools

### 🔍 Subdomain Scanner

Enumerates live subdomains via DNS resolution against a wordlist.

**v2:** Uses `dnspython` for proper DNS lookups (v1 used HTTP — unreliable). Threaded with 50 concurrent workers. Displays resolved IP alongside each found subdomain.

```text
Target domain: example.com
Wordlist: wordlists/subdomains.txt (50,000 entries)
```

---

### 🔍 Directory Scanner

Discovers accessible paths on a web target by probing a wordlist over HTTP.

**v2:** 30 concurrent threads replace the sequential loop. Each result shows HTTP status code and response size. 403 responses included — a forbidden resource is still useful recon intel. Optional extension filter (`.php`, `.html`, `.txt`, `.bak`, custom).

```text
Target URL: http://example.com
Extension: .php  (or none for bare paths)
Wordlist: wordlists/wordlist.txt (81,629 entries)
```

---

### 🌐 Network Scanner

ARP sweep to discover active hosts on a local network segment.

**v2:** MAC OUI lookup against a 61-entry static vendor map adds manufacturer hints (Cisco, Raspberry Pi, VMware, Apple, etc.) with no external API calls. Results displayed in IP | MAC | Vendor table.

> Requires elevated privileges (sudo / Administrator).

```text
Interface: eth0
IP range: 192.168.1.0/24
```

---

### 🖥️ Port Scanner

TCP port scanner with service identification and optional banner grab.

**v2:** 100 concurrent threads vs. v1's sequential loop — top-1024 scan completes in seconds. `socket.getservbyport()` maps open ports to well-known service names. Optional banner grab surfaces service version strings on open ports.

```text
Target: 192.168.1.1
Scan type: [1] Top 1024  [2] Full 65535
Banner grab: [y/n]
```

---

### 🗄️ File Fetcher

Downloads a file from a URL with progress display and integrity verification.

**v2:** SHA256 checksum computed incrementally per chunk during download — no second pass over the file. Displayed on completion so you can verify against a known-good hash.

```text
URL: https://example.com/file.zip
Output filename: file.zip  (or Enter to auto-derive)
```

---

### 🔐 Hash Cracker

Wordlist-based hash cracker supporting MD5, SHA1, SHA256, and SHA512.

**v2:** Hash algorithm auto-detected from length — no manual selection needed. Live crack speed (hashes/sec) and elapsed time displayed in progress bar and summary.

| Hash Length | Algorithm |
| --- | --- |
| 32 | MD5 |
| 40 | SHA1 |
| 64 | SHA256 |
| 128 | SHA512 |

```text
Hash: 5f4dcc3b5aa765d61d8327deb882cf99
  → Algorithm detected: MD5 (length 32)
Wordlist: wordlists/wordlist.txt
```

---

## Export

After every operation, the tool prompts:

```text
Save results to TXT? [y/n]:
```

Files are saved to `./output/` (auto-created) with the naming convention:

```text
{tool}_{target}_{YYYY-MM-DD_HH-MM}.txt
```

Examples:

- `Port_Scanner_192.168.1.1_2026-03-11_14-30.txt`
- `Hash_Cracker_5f4dcc3b5aa7_2026-03-11_15-22.txt`
- `Subdomain_Scanner_example.com_2026-03-11_15-01.txt`

Each file includes a metadata header (tool, target, settings, timestamp) followed by the result data and a summary line.

---

## Wordlists

Bundled defaults in `wordlists/`:

| File | Entries | Used by |
| --- | --- | --- |
| `subdomains.txt` | 50,000 | Subdomain Scanner |
| `wordlist.txt` | 81,629 | Directory Scanner, Hash Cracker |

Any user-supplied wordlist path is accepted at each prompt.

---

## ⚠️ Ethical & Legal Notice

These tools are provided strictly for **educational purposes** and **authorised security testing** in isolated or lab environments (VMs, CTF platforms, systems you own or have explicit written permission to test).

- Do not use these tools against systems you do not own or have written authorisation to test.
- Scanning or probing networks, hosts, or web applications without permission may be illegal under computer misuse laws in your jurisdiction.
- The author accepts no responsibility for misuse of these tools.

---

## ⌨️ Keylogger — Deferred

The keylogger (`Key Logger/transcriptor.py`) from v1 is not included in the PySec Suite v2.0 menu. It is under separate development consideration and will be revisited for v3.

---

## 📝 Contributions

Feel free to fork, open issues, or submit pull requests.

---

<!--
## 📄 License

This work is licensed under the
**Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**

📌 *You may view and share this project with proper credit, but you may not modify it or use it commercially.*

🔗 [View License Terms](https://creativecommons.org/licenses/by-nc-nd/4.0/)
-->
