import socket
from time import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.137.222'
server_port = 12345

start = time()
client_socket.connect((server_ip, server_port))
end = time()    
print(f"Connected to server {end - start} seconds") 