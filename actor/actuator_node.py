import socket
import json
import threading
import sys

# Variables globales configurables dinámicamente
ACTUATOR_HOST = '127.0.0.1'
ACTUATOR_PORT = 6000
ACTUATOR_ID = "ACT_VALVULA_GENERICA"

def handle_server_command(conn, addr):
    print(f"[CONEXIÓN] Servidor conectado desde {addr}")
    try:
        # Recibir la señal de activación
        data = conn.recv(1024).decode('utf-8')
        if not data:
            return
        
        payload = json.loads(data)
        print(f"[COMANDO RECIBIDO] Procesando señal: {payload}")

        # Validar si el comando es para activarse
        if payload.get("command") == "ACTIVATE":
            print(f"[{ACTUATOR_ID}] SIMULACIÓN: Ejecutando acción física en la red...")
            
            # Generar mensaje de confirmación (ACK)
            response = {
                "status": "SUCCESS",
                "actuator_id": ACTUATOR_ID,
                "message": f"Actuador {ACTUATOR_ID} activado correctamente en la red.",
                "timestamp": payload.get("timestamp") 
            }
            
            # Enviar la confirmación de vuelta al servidor
            conn.sendall(json.dumps(response).encode('utf-8'))
            print(f"[CONFIRMACIÓN ENVIADA] ACK enviado al servidor.")
            
    except Exception as e:
        print(f"[ERROR] Error procesando comando: {e}")
    finally:
        conn.close()

def start_actuator():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ACTUATOR_HOST, ACTUATOR_PORT))
    server_socket.listen()
    
    print(f"[*] Actuador {ACTUATOR_ID} escuchando en {ACTUATOR_HOST}:{ACTUATOR_PORT}...")
    
    try:
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_server_command, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print(f"\n[*] Apagando nodo actuador {ACTUATOR_ID}.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    # Si pasas parámetros por consola, reescribe la configuración por defecto
    if len(sys.argv) == 3:
        ACTUATOR_ID = sys.argv[1]
        ACTUATOR_PORT = int(sys.argv[2])
    else:
        print("[INFO] Iniciando con valores por defecto. Puedes pasar parámetros:")
        print("       python actuator_node.py <ID_ACTUADOR> <PUERTO>")
        print("Ejemplo: python actuator_node.py ACT_PISO_1 6001\n")
        
    start_actuator()