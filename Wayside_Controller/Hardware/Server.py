import socket
import json

from GreenYardPLC import PLC


def main():
    plc = PLC()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server is listening")


    try:
        client_socket, addr = server_socket.accept()
        print(f"connection from {addr} has been established")
        while True:
            length_prefix = client_socket.recv(10).decode('utf-8').strip()
            if not length_prefix:
                break
            
            message_length = int(length_prefix)
            
            message_data = client_socket.recv(message_length).decode('utf-8')
            decoded_json = ""
            try:
              decoded_json = json.loads(message_data)
            except json.JSONDecodeError:
                print("failed to decode Json", message_data)
                
            try:
                occupancy, authority, sw_success, switch_58, switch_62, maintenance = plc.update(decoded_json["occupancy"], decoded_json["switch_bool"], decoded_json["proposed_maintenance"], decoded_json["current_maintenance"])
                response = {
                    "authority": authority,
                    "occupancy": occupancy,
                    "switch_58": switch_58,
                    "switch_62": switch_62,
                    "maintenance": maintenance,
                }
                client_socket.sendall(json.dumps(response).encode('utf-8'))
            except UnboundLocalError:
                print("Failed to decode JSON:")

    finally:
         client_socket.close()
         server_socket.close()
         print("Connection closed")


if __name__ == "__main__":
    main()
