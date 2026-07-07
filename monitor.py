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

        # TABLA DE RED: Asocia el piso con el puerto TCP del actuador
        self.TABLA_PISOS = {
            "1": 6001,
            "2": 6002,
            "3": 6003
        }

        # NUEVO: Almacena las alertas que esperan aprobación del conserje
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

        # NUEVA LÓGICA INTERMEDIA:
        if resultado and resultado.get("activar"):
            piso_sensor = str(datos.get("piso", "1"))
            
            # En lugar de disparar el Trigger, lo guardamos en pendientes
            self.alertas_pendientes[piso_sensor] = {
                "nodo": id_nodo,
                "datos": datos
            }
            print(f"\n[ALERTA INTERCEPTADA] Peligro en Piso {piso_sensor}. Esperando confirmación del Conserje...")

        print("Estado:", resultado["estado"])
        return resultado

    # =========================================================================
    # NUEVOS MÉTODOS PARA EL CONSERJE
    # =========================================================================
    def mostrar_alertas_pendientes(self):
        """Muestra al conserje qué pisos requieren atención inmediata."""
        return list(self.alertas_pendientes.keys())

    def resolver_alerta(self, piso, autorizado=True):
        """El conserje decide si activa la red de actuadores o cancela la alerta."""
        piso = str(piso)
        if piso not in self.alertas_pendientes:
            print(f"[CONSERJERÍA] No hay alertas pendientes para el Piso {piso}.")
            return False

        if autorizado:
            print(f"\n[CONSERJERÍA] Alerta CONFIRMADA por conserje para el Piso {piso}.")
            puerto_destino = self.TABLA_PISOS.get(piso)
            if puerto_destino:
                # La señal de red viaja RECIÉN ahora hacia el actuador
                Trigger.trigger_actuator(actuator_port=puerto_destino)
            else:
                print(f"[ERROR RED] No hay puerto para el piso {piso}")
        else:
            print(f"\n[CONSERJERÍA] Alerta RECHAZADA (Falsa Alarma) por conserje para el Piso {piso}.")

        # Quitar de la lista de pendientes una vez resuelta
        del self.alertas_pendientes[piso]
        return True

    def obtener_estado_nodo(self, id_nodo):
        return self.nodos.get(id_nodo)

    def obtener_todos_los_nodos(self):
        return self.nodos