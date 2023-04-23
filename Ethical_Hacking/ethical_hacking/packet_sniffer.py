from socket import *
from os import *
from sys import *
import struct as st
import binascii as b

sockc = False
sniff_sock = 0

def analyse_udp(data):
    udp_hd = st.unpack('!4H', data[:8])
    src_prt = udp_hd[0]
    dst_prt = udp_hd[1]
    ulen = udp_hd[2]
    chksum = udp_hd[3]
    
    rdata = data[8:]

    print("UDP Header")
    print(f"Source: {src_prt}")
    print(f"Destination: {dst_prt}")
    print(f"Length: {ulen}")
    print(f"Checksum: {chksum}")
    
    return rdata

def analyse_tcp(data):
    tcp_hd = st.unpack('2H2I4H', data[:20])
    src_prt = tcp_hd[0]
    dst_prt = tcp_hd[1]
    seq_num = tcp_hd[2]
    ack_num = tcp_hd[3]
    data_off = tcp_hd[4] >> 12
    reser = (tcp_hd[5] >> 6) & 0x03ff
    flgs = tcp_hd[4] & 0x003f
    win = tcp_hd[5]
    chksum = tcp_hd[6]
    rdata = data[20:]
    
    urg = bool(flgs & 0x0020)
    ack = bool(flgs & 0x0010)
    psh = bool(flgs & 0x0008)
    rst = bool(flgs & 0x0004)
    syn = bool(flgs & 0x0002)
    fin = bool(flgs & 0x0001)

    print("TCP Header")
    print(f"Source: {src_prt}")
    print(f"Destination: {dst_prt}")
    print(f"Seq: {seq_num}")
    print(f"Ack: {ack_num}")
    print(f"Flags: {flgs}")
    print(f"URG: {urg}")
    print(f"ACK: {ack}")
    print(f"PSH: {psh}")
    print(f"RST: {rst}")
    print(f"SYN: {syn}")
    print(f"FIN: {fin}")
    print(f"Window Size: {win}")
    print(f"Checksum: {chksum}")
    
    return rdata

def analyse_ip(data):
    ip_head = st.unpack('!6H4s4s', data[:20])
    v = ip_head[0] >> 12
    ihl = (ip_head[0] >> 8) & 0x0f
    tos = ip_head[0] & 0x00ff
    tlen = ip_head[1]
    ipid = ip_head[2] 
    flgs = ip_head[3] >> 13
    frg = ip_head[3] & 0x1fff
    ip_ttl = ip_head[4] >> 8
    ip_pro = ip_head[4] & 0x00ff
    chksum = ip_head[5]
    src_addr = inet_ntoa(ip_head[6])
    dst_addr = inet_ntoa(ip_head[7])
    rdata = data[20:]

    print("IP Header")
    print(f"Version: {v}")
    print(f"IHL: {ihl}")
    print(f"ID: {ipid}")
    print(f"Length: {tlen}")
    print(f"TTL: {ip_ttl}")
    print(f"TOS: {tos}")
    print(f"Offset: {frg}")
    print(f"Protocol: {ip_pro}")
    print(f"Checksum: {chksum}")
    print(f"Source IP: {src_addr}")
    print(f"Destination IP: {dst_addr}")

    if ip_pro == 6:
        tcp_udp = "TCP"
        
    elif ip_pro == 17:
        tcp_udp = "UDP"
        
    else: 
        tcp_udp = "OTHER"
        
    return rdata, tcp_udp

def analyze_ether(data):
    ip_bool = False
    eth_head = st.unpack('!6s6sH', data[:14])
    des_mac = b.hexlify(eth_head[0])
    src_mac = b.hexlify(eth_head[1])
    pro = eth_head[2] >> 8
    rdata = data[14:]

    print("ETHER Header")
    print("Destination MAC: {}{}{}{}{}{}".format(des_mac[0:2], des_mac[2:4], des_mac[4:6], des_mac[6:8], des_mac[8:10], des_mac[10:12]))
    print("Source MAC: {}{}{}{}{}{}".format(src_mac[0:2], src_mac[2:4], src_mac[4:6], src_mac[6:8], src_mac[8:10], src_mac[10:12]))
    print("Protocol: {}".format(pro))
    if pro == 0x08:
        ip_bool = True
    return rdata, ip_bool

def func():
    global sockc
    global sniff_sock
    if sockc == False:
        sniff_sock = socket(PF_PACKET, SOCK_RAW, htons(0x0003))
        sockc = True

    data = sniff_sock.recv(3072)
    system('clear')

    data, ip_bool = analyze_ether(data)
    if ip_bool:
        data, tcp_udp = analyse_ip(data)
    else:
        return

    if tcp_udp == "TCP":
        data = analyse_tcp(data)
    if tcp_udp == "UDP":
        data = analyse_udp(data)
    else:
        return

while True:
    func()
