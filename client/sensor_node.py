import asyncio
import json
import os
import random
import sys 

from aiocoap import *
from cryptography.fernet import InvalidToken

# Permite importar security.py desde la carpeta raíz aunque este script esté en client/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from security import decrypt_json, encrypt_json

# Configuración del nodo
NODE_ID = 1
PISO = "1"  # Por defecto asignado al piso 1

SERVER_URL = "coap://127.0.0.1:5683/sensor"
INTERVALO = 5    


# Generación de sensores
def generar_datos():
    return {
        "id": NODE_ID,
        "piso": PISO,  
        "gas": random.randint(100, 2000),
        "humo": random.random() < 0.15,
        "temperatura": random.randint(15, 90),
        "voltaje": random.randint(195, 245)
    }


# Actuadores simulados
def ejecutar_acciones(respuesta):
    if not respuesta.get("activar"):
        return

    print("\n===== ACTUADORES =====")
    for accion in respuesta.get("acciones", []):
        print(f"-> {accion}")
    print("======================\n")


# Cliente CoAP
async def enviar_datos():
    protocolo = await Context.create_client_context()
    await asyncio.sleep(1)

    while True:
        datos = generar_datos()

        print("\n==========================")
        print("Datos generados por el sensor")
        print(json.dumps(datos, indent=4))
        print("==========================")

        # Antes se enviaba el JSON en bruto. Ahora el payload viaja cifrado.
        payload = encrypt_json(datos)
        print(f"Payload CoAP cifrado enviado ({len(payload)} bytes).")

        request = Message(
            code=POST,
            uri=SERVER_URL,
            payload=payload
        )

        try:
            response = await protocolo.request(request).response

            try:
                respuesta = decrypt_json(response.payload)
            except InvalidToken:
                print("\nLa respuesta del servidor no pudo descifrarse.")
                print("Respuesta recibida:", response.payload.decode("utf-8", errors="replace"))
                await asyncio.sleep(INTERVALO)
                continue

            print("\nRespuesta del servidor descifrada")
            print(json.dumps(respuesta, indent=4))

            ejecutar_acciones(respuesta)

        except Exception as e:
            print("\nNo fue posible conectar con el servidor.")
            print("Reintentando en 5 segundos")
            print(e)

        await asyncio.sleep(INTERVALO)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        NODE_ID = int(sys.argv[1])
        PISO = sys.argv[2]
    else:
        print("Usando valores por defecto. Puedes personalizarlos usando:")
        print("       python sensor_node.py <ID_NODO> <PISO>")
        print("Ejemplo: python sensor_node.py 2 2\n")

    asyncio.run(enviar_datos())
