import json

import aiocoap
import aiocoap.resource as resource


class SensorResource(resource.Resource):

    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

    async def render_post(self, request):

        try:
            # Convertir la entrada a un diccionario
            payload = request.payload.decode("utf-8")
            datos = json.loads(payload)

            print("\n===== Mensaje recibido =====")
            print(datos)

            # Procesar la información
            respuesta = self.monitor.procesar_datos(datos)

            return aiocoap.Message(
                code=aiocoap.CONTENT,
                payload=json.dumps(respuesta).encode("utf-8")
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