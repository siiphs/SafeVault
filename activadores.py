import time

class Activadores:
    
    ventilacion_activada = False
    iluminacion_activada = False
    aspersores_activados = False

    def __init__(self, calor_threshold, gas_threshold, luz_threshold):
        self.calor_threshold = calor_threshold
        self.gas_threshold = gas_threshold 
        self.luz_threshold = luz_threshold

    def activar_aspersor(self, sensor_calor):
        if (sensor_calor > self.calor_threshold) & (self.aspersores_activados == False):
            calor = input("Ingrese 1 para encender aspersores: ")
            if calor == '1':
                for i in range(3):
                    print("Encendiendo aspersores.")
                    time.sleep(0.1)
                    print("Encendiendo aspersores..")
                    time.sleep(0.1)
                    print("Encendiendo aspersores...")
                    time.sleep(0.1)
                self.aspersores_activados = True
            else:  
                print("Aspersores no encendidos")

    def activar_ventilacion(self, sensor_gas):
        if (sensor_gas > self.gas_threshold)  & (self.ventilacion_activada == False):
            gas = input("Ingrese 1 para activar ventilación: ")
            if gas == '1':
                for i in range(3):
                    print("Activando ventilación.")
                    time.sleep(0.1)
                    print("Activando ventilación..")
                    time.sleep(0.1)
                    print("Activando ventilación...")
                    time.sleep(0.1)
                self.ventilacion_activada = True
            else:
                print("Ventilación no activada")
                
    def activar_iluminacion(self, sensor_luz):
        if (sensor_luz < self.luz_threshold) & (self.iluminacion_activada == False):
            luz = input("Ingrese 1 para iluminar pasillos: ")
            if luz == '1' :
                for i in range(3):
                    print("Iluminando pasillos.")
                    time.sleep(0.1)
                    print("Iluminando pasillos..")
                    time.sleep(0.1)
                    print("Iluminando pasillos...")
                    time.sleep(0.1)
                self.iluminacion_activada = True
            else:
                print("Pasillos no iluminados")


class Sensores:
    def __init__(self):
        # Calor: normal, luego incendio progresivo
        self.calor = (
            [10]*20 +
            [12]*20 +
            [15]*20 +
            [20]*20 +
            [25]*20 +
            [30]*20 +
            [35]*20 +
            [40]*20 +
            [45]*20 +
            [50]*20
        )

        # Gas: normal, luego fuga progresiva
        self.gas = (
            [5]*30 +
            [10]*20 +
            [15]*20 +
            [20]*20 +
            [25]*20 +
            [30]*20 +
            [35]*20 +
            [40]*20 +
            [45]*20 +
            [50]*20
        )

        # Luz: normal, luego apagón progresivo
        self.luz = (
            [100]*40 +
            [90]*20 +
            [80]*20 +
            [70]*20 +
            [60]*20 +
            [50]*20 +
            [40]*20 +
            [30]*20 +
            [20]*20 +
            [10]*20
        )
    
    def obtener_calor(self):
        for i in range(len(self.calor)):
            print(f"Sensor de calor: {self.calor[i]}°C")
            yield self.calor[i]
            
    
    def obtener_gas(self):
        for i in range(len(self.gas)):
            print(f"Sensor de gas: {self.gas[i]} ppm")
            yield self.gas[i]
            

    def obtener_luz(self):
        for i in range(len(self.luz)):
            print(f"Sensor de luz: {self.luz[i]} lux")
            yield self.luz[i]
            
activador = Activadores(calor_threshold=29, gas_threshold=29, luz_threshold=25)
sensor = Sensores()

gen_calor = sensor.obtener_calor()
gen_gas = sensor.obtener_gas()
gen_luz = sensor.obtener_luz()

while True:
    try:
        activador.activar_aspersor(next(gen_calor))
        activador.activar_ventilacion(next(gen_gas))
        activador.activar_iluminacion(next(gen_luz))
        time.sleep(1)
    except StopIteration:
        print("Fin de la simulación")
        break
    