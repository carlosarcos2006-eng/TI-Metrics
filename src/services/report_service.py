import json
from encodings import utf_8


class ReportService:
    def __init__(self, indentacion: int = 4):
        if not isinstance(indentacion, int) or isinstance(indentacion, bool):
            raise TypeError("La indentación debe ser un numero entero.")

        if indentacion < 0:
            raise ValueError("La indentación no puede ser negativa.")

        self._indentacion = indentacion

    @property
    def indentacion(self) -> int:
        return self._indentacion

    def construir_resumen(
            self,
            porcentaje_500,
            ips_criticas,
            geolocalizaciones
    ) -> dict:
        resumen = {
            "porcentaje_http_500": porcentaje_500,
            "ips_criticas": list(ips_criticas),
            "geolocalizaciones": geolocalizaciones
        }

        return resumen

    def guardar_reporte_json(self, resumen, ruta_archivo) -> None:
        with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
            json.dump(resumen,
                      archivo,
                      indent=self._indentacion,
                      ensure_ascii=False
            )


def construir_resumen(porcentaje_500, ips_criticas, geolocalizaciones):
    servicio = ReportService()

    return servicio.construir_resumen(
        porcentaje_500,
        ips_criticas,
        geolocalizaciones
    )

def guardar_reporte_json(resumen, ruta_archivo):
    servicio = ReportService()
    servicio.guardar_reporte_json(resumen, ruta_archivo)