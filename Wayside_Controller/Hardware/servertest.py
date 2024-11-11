import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)
print("Server is listening")

while True:
   client, addr =  server_socket.accept()
   print(client.recv(1024).decode())
   client.send('Hello from the server!'.encode())