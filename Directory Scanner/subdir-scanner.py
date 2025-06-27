import requests 
import pyfiglet
import sys

ascii_banner = pyfiglet.figlet_format("Mini - PySec \nDirectory \nScanner v.1")
print(ascii_banner)

print("By - @mello-io")

print("\n")

sub_list = open("wordlist.txt").read() 
directories = sub_list.splitlines()

print("Please enter the type of sub directory extention type to enumerate.")
print( """
Types of extentions available;
1. html
2. txt
3. php
""") # More extensions to come !

sub_ext = input("Enter your correspoing extention : ")

for dir in directories:
    dir_enum = f"http://{sys.argv[1]}/{dir}.{sub_ext}" #change to https if using for global web enumeration.
    r = requests.get(dir_enum)
    
    if r.status_code==404: 
        pass
   
    else:
        print("Valid directory:" ,dir_enum)