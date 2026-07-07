import asyncio
import sys

from aiocoap import Context
from aiocoap.resource import Site

from resources import SensorResource
from monitor import Monitor
import time


def menu_conserje(monitor_instancia):
    #Bucle en la terminal para que el conserje vea las alertas, y decida si activar los actuadores
    while True:
        try:
            time.sleep(1)
            
            pendientes = monitor_instancia.mostrar_alertas_pendientes()
            if pendientes:
                print(f"¡ALERTA! Pisos esperando confirmación: {pendientes}")
                piso_a_resolver = input("Ingrese el número del piso para responder (o Enter para omitir): ").strip()
                if piso_a_resolver in pendientes:
                    decision = input(f"¿Confirmar y activar actuadores en Piso {piso_a_resolver}? (s/n): ").strip().lower()
                    if decision == 's':
                        monitor_instancia.resolver_alerta(piso_a_resolver, autorizado=True)
                    else:
                        monitor_instancia.resolver_alerta(piso_a_resolver, autorizado=False)
        except Exception as e:
            print(f"ERROR CONSERJE {e}")


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

    # Para ejecutar el menu del conserje
    asyncio.create_task(asyncio.to_thread(menu_conserje, monitor))

    # Mantiene el servidor vivo
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())