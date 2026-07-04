import csv
import os
from datetime import datetime


class EventLogger:

    def __init__(self):

        self.archivo = "data/eventos.csv"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.archivo):

            with open(self.archivo, "w", newline="", encoding="utf-8") as f:

                writer = csv.writer(f)

                writer.writerow([
                    "Fecha",
                    "Nodo",
                    "Gas",
                    "Humo",
                    "Temperatura",
                    "Voltaje",
                    "Estado",
                    "Mensaje"
                ])

    def registrar(self, datos, resultado):

        with open(self.archivo, "a", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([

                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                datos["id"],

                datos["gas"],

                datos["humo"],

                datos["temperatura"],

                datos["voltaje"],

                resultado["estado"],

                resultado["mensaje"]

            ])