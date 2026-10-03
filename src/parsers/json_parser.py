import json


def leer_eventos_json(ruta_archivo):
    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        eventos = json.load(archivo)

    return eventos