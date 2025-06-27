import requests
import pyfiglet
import sys

ascii_banner = pyfiglet.figlet_format("Mini - PySec \nSub Domain \nScanner v.1")
print(ascii_banner)

print("By - @mello-io")

print("\n")

sub_list = open("subdomains.txt").read() 
subdoms = sub_list.splitlines()

for sub in subdoms:
    sub_domains = f"https://{sub}.{sys.argv[1]}" 

    try:
        requests.get(sub_domains)
    
    except requests.ConnectionError: 
        pass
    
    else:
        print("Valid domain: ",sub_domains) 

'''
Usuage : #python3 subdom-scanner.py [domain].com
'''

