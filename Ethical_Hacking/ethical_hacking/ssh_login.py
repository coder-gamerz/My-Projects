from paramiko import *
from sys import *

results = []

def ssh():
    client = SSHClient()
    client.load_system_host_keys()
    client.connect('172.29.33.94', username='coder_gamerz', password='naruto1559')

    stdin, stdout, stderr = client.exec_command('ss -ltn')

    for line in stdout:
        results.append(line.strip('\n'))

def func():
    host = input('Enter ip address')
