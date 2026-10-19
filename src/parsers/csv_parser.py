
import csv


def leer_logs_csv(ruta_archivo):
    registros = []

    try:
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    fila["status"] = int(fila["status"])
                    fila["response_time"] = int(fila["response_time"])
                except (ValueError, TypeError, KeyError) as error:
                    raise ValueError(
                        f"Datos inválidos en la fila {numero_fila} "
                        f"del archivo CSV: {error}"
                    ) from error

                registros.append(fila)

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"No se encontró el archivo CSV: {ruta_archivo}"
        ) from error

    except PermissionError as error:
        raise PermissionError(
            f"No tienes permisos para leer el archivo CSV: {ruta_archivo}"
        ) from error

    return registros
