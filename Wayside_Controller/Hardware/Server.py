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

    while True:
        data = client_socket.recv(4096)
        received_data = json.loads(data.decode('utf-8'))
        print(received_data)

        if received_data.get("exit"):
                client_socket.close()
                server_socket.close()

        plc.update(received_data.get("occupancy"), received_data.get("switch_bool"), received_data.get("maintenance"))
        response = {
            "authority": plc.authority,
            "occupancy": plc.occupancy,
            "switch_57": plc.switch_57,
            "switch_63": plc.switch_63,
            "maintenance": plc.maintenance,
            "signal_57": plc.signal_57,
            "signal_63": plc.signal_63,
        }
        client_socket.sendall(json.dumps(response).encode('utf-8'))


if __name__ == "__main__":
    main()