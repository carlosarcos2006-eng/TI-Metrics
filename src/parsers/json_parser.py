
import json


def leer_eventos_json(ruta_archivo):
    try:
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            eventos = json.load(archivo)

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"No se encontró el archivo JSON: {ruta_archivo}"
        ) from error

    except PermissionError as error:
        raise PermissionError(
            f"No tienes permisos para leer el archivo JSON: {ruta_archivo}"
        ) from error

    except json.JSONDecodeError as error:
        raise ValueError(
            f"El archivo JSON contiene datos inválidos: {ruta_archivo}"
        ) from error

    return eventos
