import csv
from pathlib import Path
from src.models.base_log_parser import BaseLogParser

class CSVLogParser(BaseLogParser):
    def leer(self):
        registros = []
        try:
            with open(
                self.ruta_archivo,
                mode="r",
                encoding="utf-8"
            ) as archivo:
                lector = csv.DictReader(archivo)

                campos_obligatorios = {
                    "ip",
                    "status",
                    "response_time"
                }

                encabezados = set(lector.fieldnames or [])
                campos_faltantes = campos_obligatorios - encabezados

                if campos_faltantes:
                    raise ValueError(
                        "El archivo CSV no contiene todos los "
                        "encabezados obligatorios: "
                        f"{', '.join(sorted(campos_faltantes))}"
                    )

                for numero_fila, fila in enumerate(lector, start=2):
                    try:
                        if not fila["ip"] or not fila["ip"].strip():
                            raise ValueError(
                                "La dirección IP no puede estar vacía."
                            )

                        fila["status"] = int(fila["status"])
                        fila["response_time"] = int(
                            fila["response_time"]
                        )

                        if not 100 <= fila["status"] <= 599:
                            raise ValueError(
                                "El estado HTTP debe estar "
                                "entre 100 y 599."
                            )

                        if fila["response_time"] < 0:
                            raise ValueError(
                                "El tiempo de respuesta "
                                "no puede ser negativo."
                            )

                    except (ValueError, TypeError, KeyError) as error:
                        raise ValueError(
                            f"Datos inválidos en la fila {numero_fila} "
                            f"del archivo CSV: {error}"
                        ) from error

                    registros.append(fila)

        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"No se encontró el archivo CSV: {self.ruta_archivo}"
            ) from error

        except PermissionError as error:
            raise PermissionError(
                f"No tienes permisos para leer el archivo CSV: "
                f"{self.ruta_archivo}"
            ) from error

        return registros

def leer_logs_csv(ruta_archivo):
    if isinstance(ruta_archivo, Path):
        ruta_archivo = str(ruta_archivo)

    parser = CSVLogParser(ruta_archivo)
    return parser.leer()