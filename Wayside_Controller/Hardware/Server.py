import socket
import json

from GreenYardPLC import PLC
#import RPi.GPIO as GPIO

# 62 yard: GPIO 12
# 62-63 : GPIO 6
# 62 red: GPIO 25
# 62 green: GPIO 24

# 58 green: GPIO 23
# 58 red: GPIO 22
# 58-57: GPIO 27
# 58 yard: GPIO 17


def main():
    plc = PLC()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.2.2', 9000))
    server_socket.listen(5)
    print("Server is listening")

    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(23, GPIO.OUT) # Switch58 true
    # GPIO.setup(24, GPIO.OUT) # Switch58 false
    # GPIO.setup(22, GPIO.OUT) # Switch62 true
    # GPIO.setup(27, GPIO.OUT) # Switch62 false
    # GPIO.setup(5, GPIO.OUT) #Sig58False
    # GPIO.setup(12, GPIO.OUT) #Sig58True
    # GPIO.setup(6, GPIO.OUT) #Sig62False
    # GPIO.setup(13, GPIO.OUT) #Sig62True
    try:
        client_socket, addr = server_socket.accept()
        print(f"connection from {addr} has been established")
        while True:
            # GPIO.output(23, plc.sw58)
            # GPIO.output(24, not plc.sw58)
            # GPIO.output(22, plc.sw62)
            # GPIO.output(27, not plc.sw62)
            # GPIO.output(5, not plc.sig58)
            # GPIO.output(12, plc.sig58)
            # GPIO.output(6, not plc.sig62)
            # GPIO.output(13, plc.sig62)
            
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
                            "auth": new_auth,
                            "sig58": plc.sig58,
                            "sig62": plc.sig62

                        }
                    
                    case "ctc_suggested_switch":
                        result = plc.ctc_suggested_switch(decoded_json["switch"])
                        response = {
                            "response": "ctc_suggested_switch",
                            "result": result,
                            "sw58": plc.sw58,
                            "sw62": plc.sw62,
                            "sig58": plc.sig58,
                            "sig62": plc.sig62,
                            "auth": plc.authority

                        }
                    
                    case "ctc_maintenance":
                        result = plc.ctc_update_maintenance(decoded_json["maint"])
                        response = {
                            "response": "ctc_maintenance",
                            "maint": plc.maintenance,
                        }

                    case "ws_sw58":
                        plc.toggle_sw58()
                        response = {
                            "response": "ws_sw58",
                            "sw58": plc.sw58,
                            "auth" : plc.authority
                        }
                    
                    case "ws_sw62":
                        plc.toggle_sw62()
                        response = {
                            "response": "ws_sw62",
                            "sw62": plc.sw62,
                            "auth" : plc.authority
                        }

                    case "ws_sig58":
                        plc.toggle_sig58()
                        response = {
                            "response": "ws_sig58",
                            "sig58": plc.sig58
                        }

                    case "ws_sig62":
                        plc.toggle_sig62()
                        response = {
                            "response": "ws_sig62",
                            "sig62": plc.sig62
                        }

                    case "ctc_sw58":
                        plc.maint_sw58()
                        response = {
                            "response": "ctc_sw58",
                            "sw58": plc.sw58,
                            "sw62": plc.sw62,
                            "sig58": plc.sig58,
                            "sig62": plc.sig62,
                            "auth": plc.authority

                        }

                    case "ctc_sw62":
                        plc.maint_sw62()
                        response = {
                            "response": "ctc_sw62",
                            "sw58": plc.sw58,
                            "sw62": plc.sw62,
                            "sig58": plc.sig58,
                            "sig62": plc.sig62,
                            "auth": plc.authority
                        }

                    case "say_hi":
                        plc.update_authority(decoded_json["occ"])
                        response = {"response": "server connect",
                                    "auth": plc.authority
                                    }
                
                print(response)
                json_data = json.dumps(response)
                length_prefix = f"{len(json_data):<10}" # Fixed 10-byte length prefix
                print(int(length_prefix))
                client_socket.sendall(length_prefix.encode('utf-8') + json_data.encode('utf-8'))

            except json.JSONDecodeError:
                print("failed to decode Json", message_data)
                
            

    finally:
        # GPIO.output(23, False)
        # GPIO.output(24, False)
        # GPIO.output(22, False)
        # GPIO.output(27, False)
        # GPIO.output(5, False)
        # GPIO.output(12, False)
        # GPIO.output(6, False)
        # GPIO.output(13, False)

        client_socket.close()
        server_socket.close()
        print("Connection closed")


if __name__ == "__main__":
    main()
