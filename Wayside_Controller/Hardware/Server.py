import socket
import json
from GreenYardPLC import PLC


def main():
    plc = PLC()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server is listening")

    client_socket, addr = server_socket.accept()
    print(f"connection from {addr} has been established")
    try:
        while True:
            data = client_socket.recv(4096)
            received_data = json.loads(data.decode('utf-8'))
            print(received_data)

            if not data:
                    print("Client disconnected")
                    break

            occupancy, authority, sw_success, switch_58, switch_62, maintenance = plc.update(received_data["occupancy"], received_data["switch_bool"], received_data["proposed_maintenance"], received_data["current_maintenance"])
            response = {
                "authority": authority,
                "occupancy": occupancy,
                "switch_58": switch_58,
                "switch_62": switch_62,
                "maintenance": maintenance,
            }
            client_socket.sendall(json.dumps(response).encode('utf-8'))

    finally:
         client_socket.close()
         server_socket.close()
         print("Connection closed")


if __name__ == "__main__":
    main()