from copy import deepcopy

class MetricsService:
    def __init__(self, registros: list):
        if not isinstance(registros, list):
            raise TypeError(
                "Los registros deben proporcionarse como una lista."
            )

        for numero_registro, registro in enumerate(
            registros, start=1
        ):
            if not isinstance(registro, dict):
                raise ValueError(
                    f"Datos inválidos en el registro {numero_registro}: "
                    "el registro debe ser un diccionario."
                )

            if "status" not in registro:
                raise ValueError(
                    f"Datos inválidos en el registro {numero_registro}: "
                    "falta el campo obligatorio 'status'."
                )

            status = registro["status"]

            if not isinstance(status, int) or isinstance(status, bool):
                raise ValueError(
                    f"Datos inválidos en el registro {numero_registro}: "
                    "el estado HTTP debe ser un número entero."
                )

            if not 100 <= status <= 599:
                raise ValueError(
                    f"Datos inválidos en el registro {numero_registro}: "
                    "el estado HTTP debe estar entre 100 y 599."
                )

        self._registros = deepcopy(registros)

    @property
    def registros(self) -> list:
        return deepcopy(self._registros)

    def calcular_porcentaje_http_500(self) -> float:
        total_registros = len(self._registros)

        if total_registros == 0:
            return 0.0

        errores_500 = 0

        for registro in self._registros:
            if registro["status"] == 500:
                errores_500 += 1

        porcentaje = (errores_500 / total_registros) * 100

        return porcentaje

def calcular_porcentaje_http_500(registros):
    servicio = MetricsService(registros)
    return servicio.calcular_porcentaje_http_500()