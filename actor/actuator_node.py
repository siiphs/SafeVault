import json
import os
import socket
import sys
import threading

from cryptography.fernet import InvalidToken

# Permite importar security.py desde la carpeta raíz aunque este script esté en actor/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from security import decrypt_json, encrypt_json

# Variables globales configurables dinámicamente
ACTUATOR_HOST = '127.0.0.1'
ACTUATOR_PORT = 6000
ACTUATOR_ID = "ACT_VALVULA_GENERICA"


def handle_server_command(conn, addr):
    print(f"[CONEXIÓN] Servidor conectado desde {addr}")
    try:
        # Recibir la señal de activación cifrada
        data = conn.recv(4096)
        if not data:
            return

        try:
            payload = decrypt_json(data)
        except InvalidToken:
            print("[SEGURIDAD] Comando rechazado: payload inválido, manipulado o con clave incorrecta.")
            return

        print(f"[COMANDO RECIBIDO Y DESCIFRADO] Procesando señal: {payload}")

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

            # Enviar la confirmación cifrada de vuelta al servidor
            conn.sendall(encrypt_json(response))
            print(f"[CONFIRMACIÓN ENVIADA] ACK cifrado enviado al servidor.")

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON inválido después de descifrar: {e}")
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
