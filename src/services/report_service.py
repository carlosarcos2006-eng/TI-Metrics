import json
from os import PathLike, fspath
from src.utils.data_utils import validar_ip


class ReportService:
    def __init__(self, indentacion: int = 4):
        if (
            not isinstance(indentacion, int)
            or isinstance(indentacion, bool)
        ):
            raise TypeError(
                "La indentación debe ser un número entero."
            )

        if indentacion < 0:
            raise ValueError(
                "La indentación no puede ser negativa."
            )

        self._indentacion = indentacion

    @property
    def indentacion(self) -> int:
        return self._indentacion

    @staticmethod
    def _validar_ip(ip: str) -> None:
        validar_ip(ip)

    def construir_resumen(
        self,
        porcentaje_500,
        ips_criticas,
        geolocalizaciones
    ) -> dict:

        if (
            not isinstance(porcentaje_500, (int, float))
            or isinstance(porcentaje_500, bool)
        ):
            raise TypeError(
                "El porcentaje HTTP 500 debe ser un número."
            )

        if not 0 <= porcentaje_500 <= 100:
            raise ValueError(
                "El porcentaje HTTP 500 debe ser finito "
                "y estar entre 0 y 100."
            )

        if not isinstance(
            ips_criticas, (list, tuple, set, frozenset)
        ):
            raise TypeError(
                "Las IP críticas deben proporcionarse "
                "como una lista, tupla o conjunto."
            )

        for ip in ips_criticas:
            self._validar_ip(ip)

        if not isinstance(geolocalizaciones, dict):
            raise TypeError(
                "Las geolocalizaciones deben proporcionarse "
                "como un diccionario."
            )

        for ip, datos in geolocalizaciones.items():
            self._validar_ip(ip)

            if datos is not None and not isinstance(datos, dict):
                raise TypeError(
                    f"La geolocalización de {ip} debe ser "
                    "un diccionario o None."
                )

        if isinstance(ips_criticas, (set, frozenset)):
            ips_ordenadas = sorted(ips_criticas)
        else:
            ips_ordenadas = list(ips_criticas)

        resumen = {
            "porcentaje_http_500": porcentaje_500,
            "ips_criticas": ips_ordenadas,
            "geolocalizaciones": geolocalizaciones
        }

        return resumen

    def guardar_reporte_json(
        self,
        resumen,
        ruta_archivo
    ) -> None:

        if not isinstance(resumen, dict):
            raise TypeError(
                "El resumen debe ser un diccionario."
            )

        if isinstance(ruta_archivo, PathLike):
            ruta_archivo = fspath(ruta_archivo)

        if not isinstance(ruta_archivo, str):
            raise TypeError(
                "La ruta del reporte debe ser una cadena "
                "de texto o un objeto PathLike "
                "que represente una ruta de texto."
            )

        if not ruta_archivo.strip():
            raise ValueError(
                "La ruta del reporte no puede estar vacía."
            )

        try:
            contenido_json = json.dumps(
                resumen,
                indent=self._indentacion,
                ensure_ascii=False,
                allow_nan=False
            )

        except TypeError as error:
            raise TypeError(
                f"El resumen contiene datos no serializables "
                f"a JSON: {error}"
            ) from error

        except ValueError as error:
            raise ValueError(
                f"El resumen contiene valores inválidos "
                f"para JSON: {error}"
            ) from error

        try:
            with open(
                ruta_archivo,
                mode="w",
                encoding="utf-8"
            ) as archivo:
                archivo.write(contenido_json)

        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"No se encontró la ruta del reporte: "
                f"{ruta_archivo}"
            ) from error

        except PermissionError as error:
            raise PermissionError(
                f"No tienes permisos para guardar el reporte: "
                f"{ruta_archivo}"
            ) from error


def construir_resumen(
    porcentaje_500,
    ips_criticas,
    geolocalizaciones
):
    servicio = ReportService()

    return servicio.construir_resumen(
        porcentaje_500,
        ips_criticas,
        geolocalizaciones
    )


def guardar_reporte_json(resumen, ruta_archivo):
    servicio = ReportService()
    servicio.guardar_reporte_json(resumen, ruta_archivo)