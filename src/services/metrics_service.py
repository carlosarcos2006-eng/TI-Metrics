class MetricsService:
    def __init__(self, registros: list):
        if not isinstance(registros, list):
            raise TypeError("Los registros deben proporcionarse como una lista.")
        self._registros = registros.copy()

    @property
    def registros(self) -> list:
        return self._registros.copy()

    def calcular_porcentaje_http_500(self) -> float:
        total_registros = len(self._registros)

        if total_registros == 0:
            return 0.0

        errores_500 = 0

        for registro in self.registros:
            if registro["status"] == 500:
                errores_500 += 1

        porcentaje = (errores_500 / total_registros) * 100
        return porcentaje

def calcular_porcentaje_http_500(registros):
    servicio = MetricsService(registros)
    return servicio.calcular_porcentaje_http_500()