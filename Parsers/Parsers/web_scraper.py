import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

url = input("Enter url: ")
try:
    html = urllib.request.urlopen(url).read()
except:
    print("Invalid URL")
    quit()
soup = BeautifulSoup(html, 'html.parser')

anchors = soup('a')
for anchor in anchors:
    names = anchor.contents[0]
    names = str(names)
    fl = anchor.get('href')
    path = r"C:\Users\shrey\OneDrive\Desktop\Code\Python\parse.txt"
    print(names)
    print(fl)
