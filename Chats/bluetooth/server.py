import socket

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) 
server.bind(("58:6C:25:08:5F:A6", 4)) 
server.listen(1)

print("Waiting for connection...")

client, addr = server.accept()
print(f"Connected to {addr}")

try:
    while True:
        data = client.recv(1024)
        if not data:
            break
        print(f"Recieved message: {data.decode('utf-8')}")
        message = input("Enter message: ")
        client.send(message.encode('utf-8'))
except OSError:
    pass

print("Disconnected")

client.close()
server.close()

# A simple server for a bluetooth chat
