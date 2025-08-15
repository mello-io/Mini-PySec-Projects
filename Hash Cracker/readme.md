## Purpose

The code's intent is to take an MD5 hash and a wordlist file, then attempt to find the plaintext password by hashing each word in the list with MD5 and comparing it to the target hash.

---

## Core Logic Strengths:

- ` import hashlib `: Correctly imports Python's standard hashing library.
- ` hashlib.md5(line.strip().encode()) `: This is the way to hash a string in Python:
  - ` line.strip() `: Removes leading/trailing whitespace (like newlines), which is crucial for accurate hashing.
  - ` .encode() `: Hashing functions operate on bytes, so it is necessary to convert the string to bytes.
- ` .hexdigest() `: Correctly converts the hash object into a hexadecimal string for comparison.
- ` with open(wordlist_location, 'r') as file: ` : Used for safe file handling, ensuring the file is closed automatically.
- ` for line in file.readlines(): `: This iterates through each line of the wordlist.

---

## Current version feature layout

1. Dynamic Hash Algorithm:
   - `HASH_ALGORITHMS` Dictionary: A dictionary maps user-friendly names (`'md5'`, `'sha256'`) to the actual `hashlib` functions and their expected hexadecimal hash lengths.
   - User Selection Loop: Prompts the user to choose an algorithm and validates the input against the `HASH_ALGORITHMS` keys.
   - Dynamic Hashing: The `hash_func` variable (e.g., `hashlib.md5` or `hashlib.sha256`) is used dynamically within the loop.


2. Robust Error Handling and Validation:
   - Wordlist File Not Found: Uses `os.path.exists()` and a `while True` loop with `try-except IOError` to ensure the user provides a valid, existing wordlist path.
   - Hash Input Validation:
      - Checks if the input hash is empty.
      - Validates the length of the input hash against the `expected_hash_length` for the chosen algorithm.
      - Performs a basic check to ensure the hash consists of valid hexadecimal characters.
   - File Encoding: Added `encoding='utf-8', errors='ignore'` to `open()` calls. This helps handle wordlists that might contain non-ASCII characters without crashing, by ignoring characters that can't be decoded.


3. Progress Indicator:
   - Line Counting: Performs a first pass over the wordlist (`for _ in file: total_lines += 1`) to accurately count the total number of lines. This is memory-efficient as it doesn't load the whole file.
   - Progress Bar Logic: Integrated the progress bar (using `\r` and `sys.stdout.flush()`) to show percentage and count of processed words.
   - Clean Output on Match: When a password is found, the current progress bar line is cleared (`sys.stdout.write("\r" + " " * (bar_length + 40) + "\r")`) before printing the "Found cleartext password!" message on a new line.

4. Efficiency for Large Wordlists:
   - `for line in file:`: The core cracking loop now iterates directly over the file object, reading one line at a time. This is highly memory-efficient and crucial for handling very large wordlists (gigabytes) without running out of RAM.

5. No Match Scenario:
   - A `found_password` boolean flag tracks whether a match was found.
   - After the loop completes, it checks this flag and prints "Password not found in the provided wordlist." if no match was made.

6. Clean Exit:
   - Removed `exit(0)` from inside the loop, based on the initial code. The function now simply breaks the loop if a match is found, and the script naturally finishes after printing the final summary.
