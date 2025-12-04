import requests
import threading
import os
import urllib3
import socket
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WORDLIST_URL = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt"

if not os.path.exists("wordlist.txt"):
    data = requests.get(WORDLIST_URL).text
    with open("wordlist.txt", "w", encoding="utf-8") as f:
        f.write(data)

domain = input("Enter the target domain (e.g., example.com): ")

with open("wordlist.txt") as f:
    subdomains = f.read().splitlines()

limit = input(
    f"How many subdomains you want to scan? (max {len(subdomains)}): ")

try:
    limit = int(limit)
    if limit <= 0 or limit > len(subdomains):
        limit = len(subdomains)
except:
    limit = len(subdomains)

subdomains = subdomains[:limit]

discovered_subdomains = []
lock = threading.Lock()


def check_subdomains(subdomain):
    full_domain = f"{subdomain}.{domain}"
    try:
        socket.gethostbyname(full_domain)
    except socket.gaierror:
        return

    for proto in ["http", "https"]:
        url = f"{proto}://{full_domain}"
        try:
            response = requests.get(url, timeout=3, verify=False)
            if response.status_code < 400:
                print(f"[+] Alive: {url} (Status: {response.status_code})")
                with lock:
                    discovered_subdomains.append(
                        f"{url}  Status:{response.status_code}")
        except:
            pass


with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(check_subdomains, subdomains)

with open("discovered_wordlist.txt", "w") as f:
    for s in discovered_subdomains:
        f.write(s + "\n")

print("\nScan Completed!")
print(f"Total Found: {len(discovered_subdomains)}")
