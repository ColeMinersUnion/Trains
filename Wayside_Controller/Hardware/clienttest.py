import socket
import json
from time import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.137.222'
server_port = 12345

start = time()
client_socket.connect((server_ip, server_port))
end = time()    
print(f"Connected to server {end - start} seconds") 

# Create some data to send as JSON
data_to_send = {'name': 'Alice', 'age': 30, 'city': 'New York'}

# Send JSON data
json_data = json.dumps(data_to_send)  # Convert dictionary to JSON string
client_socket.send(json_data.encode('utf-8'))  # Send as bytes
client_socket.sendall('Hello from the client!'.encode())


print(client_socket.recv(1024).decode())

# Close the connection
client_socket.close()