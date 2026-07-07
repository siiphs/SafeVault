import asyncio
import json
import random
import sys  # Importamos sys para poder pasar parámetros por consola opcionalmente

from aiocoap import *

# Configuración del nodo
NODE_ID = 1
PISO = "1"  # <--- NUEVO: Por defecto asignado al piso 1

SERVER_URL = "coap://127.0.0.1:5683/sensor"
INTERVALO = 5      # en segundos


# Generación de sensores
def generar_datos():
    return {
        "id": NODE_ID,
        "piso": PISO,  # <--- NUEVO: Enviamos el piso a la red para que el Monitor sepa qué actuador activar
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
        print("Datos enviados")
        print(json.dumps(datos, indent=4))
        print("==========================")

        payload = json.dumps(datos).encode("utf-8")
        request = Message(
            code=POST,
            uri=SERVER_URL,
            payload=payload
        )

        try:
            response = await protocolo.request(request).response
            respuesta = json.loads(response.payload.decode())

            print("\nRespuesta del servidor")
            print(json.dumps(respuesta, indent=4))

            ejecutar_acciones(respuesta)

        except Exception as e:
            print("\nNo fue posible conectar con el servidor.")
            print("Reintentando en 5 segundos...")
            print(e)

        await asyncio.sleep(INTERVALO)


if __name__ == "__main__":
    # Opcional: Permite pasar el ID del nodo y el Piso por consola para levantar los 3 sensores fácil
    if len(sys.argv) == 3:
        NODE_ID = int(sys.argv[1])
        PISO = sys.argv[2]
    else:
        print("[INFO] Usando valores por defecto. Puedes personalizarlos usando:")
        print("       python sensor_node.py <ID_NODO> <PISO>")
        print("Ejemplo: python sensor_node.py 2 2\n")

    asyncio.run(enviar_datos())