import json

from src.models.base_log_parser import BaseLogParser

class JSONLogParser(BaseLogParser):

    def leer(self):
        try:
            with open(
                self.ruta_archivo,
                mode="r",
                encoding="utf-8",
            ) as archivo:
                eventos = json.load(archivo)

        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"No se encontró el archivo JSON: {self.ruta_archivo}"
            ) from error

        except json.JSONDecodeError as error:
            raise ValueError(
                f"El archivo JSON contiene datos inválidos:"
                f"{self.ruta_archivo}"
            ) from error

        return eventos

def leer_eventos_json(ruta_archivo):
    parser = JSONLogParser(str(ruta_archivo))
    return parser.leer()