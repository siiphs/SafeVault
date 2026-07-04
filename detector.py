class Detector:

    def __init__(self):

        # Umbrales del sistema
        self.GAS_MAX = 1000
        self.TEMP_MAX = 60
        self.VOLTAJE_MAX = 240
        self.VOLTAJE_MIN = 200

    def analizar(self, datos):
        gas = datos["gas"]
        humo = datos["humo"]
        temperatura = datos["temperatura"]
        voltaje = datos["voltaje"]

        acciones = []

        # Incendio
        if humo:
            acciones.append("Activar aspersores")

        # Fuga de gas
        if gas >= self.GAS_MAX:
            acciones.append("Cerrar válvula de gas")
            acciones.append("Cortar electricidad")

        # Temperatura elevada
        if temperatura >= self.TEMP_MAX:
            acciones.append("Activar aspersores")

        # Voltaje anormal
        if voltaje < self.VOLTAJE_MIN or voltaje > self.VOLTAJE_MAX:
            acciones.append("Revisar sistema eléctrico")

        # Eliminar acciones repetidas
        acciones = list(set(acciones))

        if len(acciones) == 0:

            return {
                "estado": "OK",
                "mensaje": "Sistema funcionando normalmente.",
                "activar": False,
                "acciones": []
            }

        return {
            "estado": "PELIGRO",
            "mensaje": "Se detectó una condición de riesgo.",
            "activar": True,
            "acciones": acciones
        }