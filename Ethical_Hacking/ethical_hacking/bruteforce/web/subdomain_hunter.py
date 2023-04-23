from requests import *

turl = input("Enter Target URL: ")
file = open("Directories_Common.wordlist", 'r')

def reque(url):
    try:
        return get("https://" + url)
        
    except exceptions.ConnectionError:
        pass

for l in file:
    w = l.strip()
    furl = w + "." + turl
    resp = reque(furl)
    if resp:
        print(f"Discovered a Subdomain: {furl}")
