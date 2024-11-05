import socket
import json
from GreenYardPLC import PLC

plc = PLC()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)
print("Server is listening")

client_socket, addr = server_socket.accept()
print(f"connection from {addr} has been established")

try: 
    data = client_socket.recv(4096)
    received_data = json.loads(data.decode('utf-8'))
    print(received_data)

    response = {
        "authority": [False for i in range(4)],
        "signal_57": True,
    }
    client_socket.sendall(json.dumps(response).encode('utf-8'))
finally:
    client_socket.close()
    server_socket.close()