import socket
import json

# Set up server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))  # Bind to localhost and port 12345
server_socket.listen(1)  # Listen for one connection

print("Server listening on port 12345...")

# Accept a connection
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

# Receive JSON data
data = client_socket.recv(1024).decode('utf-8')
json_data = json.loads(data)  # Decode JSON data

print("Received JSON data:", json_data)

response = {"Occupancy": [True, False, True], "Authority": [True, False, True]}
response_json = json.dumps(response)  # Convert dictionary to JSON string
client_socket.send(response_json.encode('utf-8'))  # Send JSON data


# Close the connection
client_socket.close()
server_socket.close()
