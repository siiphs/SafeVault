import socket
import json
import time

class Trigger:
 
 @staticmethod
 def trigger_actuator(actuator_host='127.0.0.1', actuator_port=6000):
    
    # Crear el socket para conectar con el actuador
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((actuator_host, actuator_port))
        
        # Estructura del comando de red
        command_payload = {
            "command": "ACTIVATE",
            "timestamp": time.time(),
            "reason": "Umbral de sensor excedido"
        }
        
        # Enviar comando
        client_socket.sendall(json.dumps(command_payload).encode('utf-8'))
        
        # Esperar la confirmación (ACK) del actuador
        raw_response = client_socket.recv(1024).decode('utf-8')
        if raw_response:
            response = json.loads(raw_response)
            print(f"[ACK RECIBIDO] El actuador confirmó la acción de red:")
            print(f"    ID Actuador: {response.get('actuator_id')}")
            print(f"    Estado: {response.get('status')}")
            print(f"    Mensaje: {response.get('message')}")
            return True
        else:
            print("[ERROR DE RED] El actuador cerró la conexión sin responder.")
            return False
            
    except ConnectionRefusedError:
        print(f"[ERROR DE RED] No se pudo conectar al actuador en {actuator_host}:{actuator_port}. ¿Está encendido el nodo?")
        return False
    except Exception as e:
        print(f"[ERROR] Error en la comunicación con el actuador: {e}")
        return False
    finally:
        client_socket.close()