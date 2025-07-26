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
⚒️ Development & Testing - 
⚒️ Initial Deployment - 
⚠️ Feature Development - 
⚠️ Code Maintainance

---

Projects in python to;
- Enumerate the target's subdomain & subdirectories
- Build a simple keylogger
- Scan the network to find target systems
- Scan any target to find the open ports
- Download files from the internet
- Crack hashes

---

🖥️ Dependencies
```
#python3 -m pip install --upgrade pip
#pip3 install requests pyfiglet scapy requests sys

```

---

## 🔍 Subdomain Scanner

Subdom Scanner : v1

Is a standard subdomain scanner made in python, to find different types of subdomains for a domain.
- Download both subdom-scanner.py and subdomains.txt for usuage.
- Usuage;
  ```
  #wget https://github.com/mello-io/Mini-PySec-Projects/blob/main/Sub%20Domain%20Scanner/subdom-scanner.py
  #wget https://github.com/mello-io/Mini-PySec-Projects/blob/main/Sub%20Domain%20Scanner/subdomains.txt
  #chmod +x subdom-scanner.py
  #python3 subdom-scanner.py google.com
  ```

---

## 🔍 Directory Scanner

Directory Scanner : v1

Is a standard directory scanner made in python, to use on valid domains and subdomains to find internal directories and interesting endpoints.
- Download both subdir-scanner.py and wordlist.txt for usuage.
- Usuage;
  ```
  #wget https://github.com/mello-io/Mini-PySec-Projects/blob/main/Directory%20Scanner/subdir-scanner.py
  #wget https://github.com/mello-io/Mini-PySec-Projects/blob/main/Directory%20Scanner/wordlists.txt
  #chmod +x subdir-scanner.py
  #python3 subdir-scanner.py google.com
    > Enter extension of choice.
  ```

---

## 🔍 Network Scanner

ARP Scanner : v1

Is a intermediate network scanner made in python, to use find and validate IP addresses to MAC addresses in a user provided network.  
- Usuage;
  ```
  #wget https://github.com/mello-io/Mini-PySec-Projects/blob/main/Network%20Scanner/arp-scanner.py
  #chmod +x arp-scanner.py
  #python3 arp-scanner.py
    > Enter network interface.
    > Enter IP address range.
  ```

---

<!--
## 📄 License

This work is licensed under the  
**Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**

📌 *You may view and share this project with proper credit, but you may not modify it or use it commercially.*

🔗 [View License Terms](https://creativecommons.org/licenses/by-nc-nd/4.0/)
-->
