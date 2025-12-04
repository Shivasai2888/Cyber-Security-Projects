Requirements



To run this tool, you need:



Python Version



Python 3.8 or higher



Required Python Libraries



Install all required packages with:



Built‑in Libraries Used (No installation needed)



These are included with Python:



os



socket



threading



concurrent.futures



urllib3 (installed via pip but used as main module)



You give it a domain

For example: example.com.



It checks a list of possible subdomains



Online scanner: Downloads a big list of common subdomains (like mail.example.com, admin.example.com) from the internet.



Local scanner: Uses your small local list (subdomains.txt) for faster scanning.



It checks if each subdomain exists



The tool tries to resolve the subdomain using DNS.



If it exists, it moves to the next step.



It checks if the subdomain is alive



Sends a quick request via HTTP or HTTPS.



If the server responds, it’s considered “live”.



It saves results



Online scanner: discovered\_wordlist.txt



Local scanner: discovered\_subdomains.txt



It runs fast



Uses multithreading, so multiple subdomains are checked at the same time.

