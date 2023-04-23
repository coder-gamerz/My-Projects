from queue import Queue
import socket
import threading
from termcolor import cprint
from colorama import init
from os import system

system("color")
init()

target = input("Enter target to scan: ")
target = socket.gethostbyname(target)
queue = Queue()
open_ports = []


def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

def get_ports(mode):
    if mode == 1:
        for port in range(1, 1024):
            queue.put(port)
    elif mode == 2:
        for port in range(1, 49152):
            queue.put(port)
    elif mode == 3:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            queue.put(port)
    elif mode == 4:
        ports = input("Enter your ports (seperate by blank):")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            cprint("Port {} is open!".format(port), 'green')
            open_ports.append(port)
        
        if KeyboardInterrupt:
            exit()

        else:
            print("Port {} is closed!".format(port), 'red')

        

def run_scanner(threads, mode):

    get_ports(mode)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    cprint(f"Open ports are: {open_ports}", 'cyan')

run_scanner(1000, 1)

