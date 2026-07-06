import socket
import json
import threading

# Configuración base del actuador
ACTUATOR_HOST = '127.0.0.1'
ACTUATOR_PORT = 6000  # Puedes usar diferentes puertos si tienes múltiples actuadores
ACTUATOR_ID = "ACT_VALVULA_01"

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
                "message": "Actuador activado correctamente y funcionando.",
                "timestamp": payload.get("timestamp") # Opcional: para medir latencia
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
    # allow reuse of address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ACTUATOR_HOST, ACTUATOR_PORT))
    server_socket.listen()
    
    print(f"[*] Actuador {ACTUATOR_ID} escuchando en {ACTUATOR_HOST}:{ACTUATOR_PORT}...")
    
    try:
        while True:
            conn, addr = server_socket.accept()
            # Manejar en un hilo para no bloquear el flujo de red si llegan más peticiones
            thread = threading.Thread(target=handle_server_command, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\n[*] Apagando nodo actuador.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_actuator()