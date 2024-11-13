import socket
import json

from GreenYardPLC import PLC
import RPi.GPIO as GPIO

def main():
    plc = PLC()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9000))
    server_socket.listen(5)
    print("Server is listening")

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.OUT) # Switch58 true
    GPIO.setup(24, GPIO.OUT) # Switch58 false

    try:
        client_socket, addr = server_socket.accept()
        print(f"connection from {addr} has been established")
        while True:
            GPIO.output(23, plc.sw58)
            GPIO.output(24, not plc.sw58)
            length_prefix = client_socket.recv(10).decode('utf-8').strip()
            print(length_prefix)
            if not length_prefix:
                break
            
            message_length = int(length_prefix)
            
            message_data = client_socket.recv(message_length).decode('utf-8')
            decoded_json = ""
            try:
                decoded_json = json.loads(message_data)
                print(decoded_json)


                match decoded_json["input"]:
                  
                    case "tm_occupancy":
                        new_auth = plc.update_authority(decoded_json["occupancy"])
                        response = {
                            "response": "tm_occupancy",
                            "auth": new_auth
                        }
                    
                    case "ctc_suggested_switch":
                        result = plc.ctc_suggested_switch(decoded_json["switch"])
                        response = {
                            "response": "ctc_suggested_switch",
                            "result": result,
                            "sw58": plc.sw58,
                            "sw62": plc.sw62
                        }
                    case "say_hi":
                        response = {"response": "server connect"}
                        
                json_data = json.dumps(response)
                length_prefix = f"{len(json_data):<10}" # Fixed 10-byte length prefix
                print(length_prefix)
                client_socket.sendall(length_prefix.encode('utf-8') + json_data.encode('utf-8'))

            except json.JSONDecodeError:
                print("failed to decode Json", message_data)
                
            

    finally:
         client_socket.close()
         server_socket.close()
         print("Connection closed")


if __name__ == "__main__":
    main()
