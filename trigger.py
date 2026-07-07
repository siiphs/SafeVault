import socket
import time

from cryptography.fernet import InvalidToken

from security import decrypt_json, encrypt_json


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

            # Enviar comando cifrado por TCP. Así Wireshark tampoco muestra el JSON del actuador.
            encrypted_command = encrypt_json(command_payload)
            client_socket.sendall(encrypted_command)
            print(f"Comando TCP cifrado enviado al actuador en puerto {actuator_port}.")

            # Esperar la confirmación (ACK) cifrada del actuador
            raw_response = client_socket.recv(4096)
            if raw_response:
                try:
                    response = decrypt_json(raw_response)
                except InvalidToken:
                    print("ACK rechazado: no se pudo descifrar o fue manipulado.")
                    return False

                print(f"El actuador confirmó la acción de red:")
                print(f"ID Actuador: {response.get('actuator_id')}")
                print(f"Estado: {response.get('status')}")
                print(f"Mensaje: {response.get('message')}")
                return True
            else:
                print("El actuador cerró la conexión sin responder.")
                return False

        except ConnectionRefusedError:
            print(f"No se pudo conectar al actuador en {actuator_host}:{actuator_port}. ¿Está encendido el nodo?")
            return False
        except Exception as e:
            print(f"Error en la comunicación con el actuador: {e}")
            return False
        finally:
            client_socket.close()
