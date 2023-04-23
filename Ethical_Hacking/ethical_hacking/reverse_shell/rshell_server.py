import socket
import threading
import os
import sys

def send_commands(conn):
    while True:
        cmd = input("Shell~# ")
        if cmd == 'quit':
            conn.close()
            server.close()
            sys.exit(0)
            
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(102400), "utf-8")
            print(client_response, end="")

bind_ip = "0.0.0.0"
bind_port = 99
serv_add = (bind_ip, bind_port)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((serv_add))
server.listen(5)
print ("Listening on {}:{}".format(bind_ip,bind_port))

conn,addr = server.accept()
print('Accepted connection from {} and port {}'.format(addr[0],addr[1]))

send_commands(conn)
conn.close()
