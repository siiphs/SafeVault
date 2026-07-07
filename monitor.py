from detector import Detector
from logger import EventLogger
from trigger import Trigger

class Monitor:

    def __init__(self):

        # Estado actual de todos los nodos
        self.nodos = {}

        # Componentes del sistema
        self.detector = Detector()
        self.logger = EventLogger()

        # TABLA DE RED: Asocia el piso con el puerto TCP del actuador correspondiente
        self.TABLA_PISOS = {
            "1": 6001,
            "2": 6002,
            "3": 6003
        }

    def procesar_datos(self, datos):
        # Verificar que existan los campos mínimos
        campos = ["id", "gas", "humo", "temperatura", "voltaje"]

        for campo in campos:
            if campo not in datos:
                return {
                    "estado": "ERROR",
                    "mensaje": f"Falta el campo '{campo}'",
                    "activar": False
                }

        id_nodo = datos["id"]

        # Guarda el estado más reciente del nodo
        self.nodos[id_nodo] = datos

        # Mostrar información en consola
        print(f"\nNodo {id_nodo}")
        print(f"Gas          : {datos['gas']}")
        print(f"Humo         : {datos['humo']}")
        print(f"Temperatura  : {datos['temperatura']}")
        print(f"Voltaje      : {datos['voltaje']}")

        # Detectar posibles peligros
        resultado = self.detector.analizar(datos)

        # Registrar el evento
        self.logger.registrar(datos, resultado)

        # Enviar señal de activación si es necesario
        if resultado and resultado.get("activar"):
            # Obtenemos el piso del sensor (por defecto el "1" si no se envía)
            piso_sensor = str(datos.get("piso", "1"))
            puerto_destino = self.TABLA_PISOS.get(piso_sensor)
            
            if puerto_destino:
                Trigger.trigger_actuator(actuator_port=puerto_destino)
            else:
                print(f"[ERROR RED] No existe un puerto asignado para el piso {piso_sensor}")

        # Mostrar estado
        print("Estado:", resultado["estado"])

        # Responder al nodo
        return resultado

    def obtener_estado_nodo(self, id_nodo):
        return self.nodos.get(id_nodo)

    def obtener_todos_los_nodos(self):
        return self.nodos