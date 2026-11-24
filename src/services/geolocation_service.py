import math
import requests
from urllib.parse import urlsplit
from src.utils.data_utils import validar_ip

class GeolocationService:
    def __init__(
        self,
        url_base: str = "http://ip-api.com/json",
        timeout: int | float = 5
    ) -> None:

        if not isinstance(url_base, str):
            raise TypeError(
                "La URL base debe ser una cadena de texto."
            )

        if not url_base.strip():
            raise ValueError(
                "La URL base no puede estar vacía."
            )

        url_base = url_base.strip()
        componentes_url = urlsplit(url_base)

        if (
            componentes_url.scheme not in ("http", "https")
            or not componentes_url.hostname
        ):
            raise ValueError(
                "La URL base debe utilizar HTTP o HTTPS "
                "y contener un servidor válido."
            )

        if (
            not isinstance(timeout, (int, float))
            or isinstance(timeout, bool)
        ):
            raise TypeError(
                "El timeout debe ser un número."
            )

        if (
            timeout <= 0
            or (
                isinstance(timeout, float)
                and not math.isfinite(timeout)
            )
        ):
            raise ValueError(
                "El timeout debe ser positivo y finito."
            )

        self._url_base = url_base.rstrip("/")
        self._timeout = timeout

    @property
    def url_base(self) -> str:
        return self._url_base

    @property
    def timeout(self) -> int | float:
        return self._timeout

    @staticmethod
    def _validar_ip(ip: str) -> None:
        validar_ip(ip)

    def obtener_geolocalizacion(self, ip):
        self._validar_ip(ip)

        url = f"{self._url_base}/{ip}"

        try:
            respuesta = requests.get(
                url,
                timeout=self._timeout
            )

            if respuesta.status_code != 200:
                return None

            datos = respuesta.json()

            if not isinstance(datos, dict):
                return None

            if datos.get("status") != "success":
                return None

            return datos

        except requests.exceptions.Timeout:
            return None

        except requests.exceptions.RequestException:
            return None

    def enriquecer_ips_con_geolocalizacion(self, ips):
        if not isinstance(
            ips, (list, tuple, set, frozenset)
        ):
            raise TypeError(
                "Las direcciones IP deben proporcionarse "
                "como una lista, tupla o conjunto."
            )

        for ip in ips:
            self._validar_ip(ip)

        resultados = {}

        for ip in ips:
            resultados[ip] = self.obtener_geolocalizacion(ip)

        return resultados


def obtener_geolocalizacion(ip):
    servicio = GeolocationService()
    return servicio.obtener_geolocalizacion(ip)


def enriquecer_ips_con_geolocalizacion(ips):
    servicio = GeolocationService()
    return servicio.enriquecer_ips_con_geolocalizacion(ips)