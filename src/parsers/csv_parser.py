import csv

def leer_logs_csv(ruta_archivo):
    registros = []

    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            fila ["status"] = int(fila["status"])
            fila ["response_time"] = int(fila["response_time"])

            registros.append(fila)

    return registros