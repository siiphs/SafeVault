import json

import aiocoap
import aiocoap.resource as resource
from cryptography.fernet import InvalidToken

from security import decrypt_json, encrypt_json


class SensorResource(resource.Resource):

    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

    async def render_post(self, request):

        try:
            # El payload recibido por CoAP viene cifrado. Wireshark solo verá bytes/token,
            # no el JSON original del sensor.
            datos = decrypt_json(request.payload)

            print("\n===== Mensaje CoAP recibido y descifrado =====")
            print(datos)

            # Procesar la información
            respuesta = self.monitor.procesar_datos(datos)

            # La respuesta al sensor también viaja cifrada.
            return aiocoap.Message(
                code=aiocoap.CONTENT,
                payload=encrypt_json(respuesta)
            )

        except InvalidToken:
            print("[SEGURIDAD] Mensaje rechazado: payload inválido, manipulado o con clave incorrecta.")

            return aiocoap.Message(
                code=aiocoap.UNAUTHORIZED,
                payload=b"Mensaje no autorizado"
            )

        except json.JSONDecodeError:

            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=b"JSON invalido"
            )

        except Exception as e:

            print("Error:", e)

            return aiocoap.Message(
                code=aiocoap.INTERNAL_SERVER_ERROR,
                payload=b"Error interno"
            )
