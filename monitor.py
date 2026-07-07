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

        # Tabla de puertos para cada piso
        self.TABLA_PISOS = {
            "1": 6001,
            "2": 6002,
            "3": 6003
        }

        # Alertas que verá el conserje
        self.alertas_pendientes = {}

    def procesar_datos(self, datos):
        campos = ["id", "gas", "humo", "temperatura", "voltaje"]
        for campo in campos:
            if campo not in datos:
                return {"estado": "ERROR", "mensaje": f"Falta el campo '{campo}'", "activar": False}

        id_nodo = datos["id"]
        self.nodos[id_nodo] = datos

        print(f"\nNodo {id_nodo}")
        print(f"Gas          : {datos['gas']}")
        print(f"Humo         : {datos['humo']}")
        print(f"Temperatura  : {datos['temperatura']}")
        print(f"Voltaje      : {datos['voltaje']}")

        resultado = self.detector.analizar(datos)
        self.logger.registrar(datos, resultado)

        # Si recibe peligro, primero lo guarda en pendiente y espera confirmacion
        if resultado and resultado.get("activar"):
            piso_sensor = str(datos.get("piso", "1"))
            
            # guarda la alerta para que la vea el conserje
            self.alertas_pendientes[piso_sensor] = {
                "nodo": id_nodo,
                "datos": datos
            }
            print(f"\n Peligro en Piso {piso_sensor}. Conserje confirme")

        print("Estado:", resultado["estado"])
        return resultado

    def mostrar_alertas_pendientes(self):
        #Muestra las alertas pendientes al conserje en la terminal
        return list(self.alertas_pendientes.keys())

    def resolver_alerta(self, piso, autorizado=True):
        #El conserje decide si activar o no los sistemas de emergencia
        piso = str(piso)
        if piso not in self.alertas_pendientes:
            print(f"No hay alertas pendientes para el Piso {piso}.")
            return False

        if autorizado:
            print(f"\nAlerta confirmada por conserje para el Piso {piso}.")
            puerto_destino = self.TABLA_PISOS.get(piso)
            if puerto_destino:
                # Se autoriza la activación.
                Trigger.trigger_actuator(actuator_port=puerto_destino)
            else:
                print(f"No hay puerto para el piso {piso}")
        else:
            print(f"\n Falsa alarma decretada por conserje para el Piso {piso}.")

        # Quitar de la lista de pendientes una vez resuelta
        del self.alertas_pendientes[piso]
        return True

    def obtener_estado_nodo(self, id_nodo):
        return self.nodos.get(id_nodo)

    def obtener_todos_los_nodos(self):
        return self.nodos