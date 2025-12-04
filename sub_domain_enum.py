import requests
import threading
import os

if not os.path.exists("subdomains.txt"):
    with open("subdomains.txt", "w") as f:
        f.write("www\nmail\nftp\nadmin\ntest\n")
    print("subdomains.txt created with default subdomains.")

domain = input("Enter an domain name: ")


with open('subdomains.txt') as f:
    subdomains = f.read().splitlines()

discovered_subdomains = []


lock = threading.Lock()


def check_subdomains(subdomain):

    url = f'http://{subdomain}.{domain}'
    try:
        requests.get(url, timeout=3)
    except requests.ConnectionError:
        pass
    else:
        print("[+] Discovered subdomain:", url)

        with lock:
            discovered_subdomains.append(url)


threads = []


for subdomain in subdomains:
    thread = threading.Thread(target=check_subdomains, args=(subdomain,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

with open("discovered_subdomains.txt", 'w') as f:
    for sub in discovered_subdomains:
        print(sub, file=f)

print("\nScan Completed!")
print(f"Total Found: {len(discovered_subdomains)}")
