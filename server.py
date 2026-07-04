import asyncio

from aiocoap import Context
from aiocoap.resource import Site

from resources import SensorResource
from monitor import Monitor


async def main():

    # Objeto que mantiene el estado de todos los nodos
    monitor = Monitor()

    # Sitio CoAP
    root = Site()

    # Registrar recursos
    root.add_resource(["sensor"], SensorResource(monitor))

    # Crear servidor CoAP
    await Context.create_server_context(root, bind=("127.0.0.1", 5683))

    print("=" * 50)
    print("SafeVault - Servidor CoAP iniciado")
    print("Escuchando en el puerto 5683...")
    print("=" * 50)

    # Mantiene el servidor vivo
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())