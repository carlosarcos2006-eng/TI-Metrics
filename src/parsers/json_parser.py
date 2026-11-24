import json
from os import PathLike, fspath
from src.models.base_log_parser import BaseLogParser

class JSONLogParser(BaseLogParser):
    def leer(self):
        campos_obligatorios = ("ip", "event", "severity")
        try:
            with open(
                self.ruta_archivo,
                mode="r",
                encoding="utf-8",
            ) as archivo:
                eventos = json.load(archivo)
        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"No se encontró el archivo JSON: "
                f"{self.ruta_archivo}"
            ) from error
        except PermissionError as error:
            raise PermissionError(
                f"No tienes permisos para leer el archivo JSON: "
                f"{self.ruta_archivo}"
            ) from error
        except json.JSONDecodeError as error:
            raise ValueError(
                f"El archivo JSON contiene datos inválidos: "
                f"{self.ruta_archivo}"
            ) from error
        if not isinstance(eventos, list):
            raise ValueError(
                "El archivo JSON debe contener una lista de eventos."
            )

        for numero_evento, evento in enumerate(eventos, start=1):

            if not isinstance(evento, dict):
                raise ValueError(
                    f"Datos inválidos en el evento {numero_evento}: "
                    "el evento debe ser un diccionario."
                )

            for campo in campos_obligatorios:

                if campo not in evento:
                    raise ValueError(
                        f"Datos inválidos en el evento {numero_evento}: "
                        f"falta el campo obligatorio '{campo}'."
                    )

                valor = evento[campo]

                if not isinstance(valor, str) or not valor.strip():
                    raise ValueError(
                        f"Datos inválidos en el evento {numero_evento}: "
                        f"el campo '{campo}' debe ser una cadena no vacía."
                    )

        return eventos

def leer_eventos_json(ruta_archivo):
    if isinstance(ruta_archivo, PathLike):
        ruta_archivo = fspath(ruta_archivo)

    parser = JSONLogParser(ruta_archivo)
    return parser.leer()