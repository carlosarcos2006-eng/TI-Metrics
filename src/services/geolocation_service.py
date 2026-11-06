import requests
from coverage import results


class GeolocationService:
    def __init__(self,
                 url_base: str = "http://ip-api.com/json",
                 timeout: int = 5
    ):
        if not isinstance(url_base, str):
            raise TypeError("La URL base debe ser una cadena de texto.")

        if not url_base.strip():
            raise ValueError("La URL base no puede estar vacía.")

        if not isinstance(timeout, (int, float)) or isinstance(timeout, bool):
            raise TypeError("El timeout debe ser un número.")

        if timeout <= 0:
            raise ValueError("El timeout debe ser mayor que cero.")

        self._url_base = url_base.rstrip("/")
        self._timeout = timeout

    @property
    def url_base(self) -> str:
        return self._url_base

    @property
    def timeout(self) -> int | float:
        return self._timeout

    def obtener_geolocalizacion(self, ip):
        url = f"{self._url_base}/{ip}"

        try:
            respuesta = requests.get(url, timeout=self._timeout)

            if respuesta.status_code != 200:
                return None

            datos = respuesta.json()

            if datos["status"] != "success":
                return None

            return datos

        except requests.exceptions.Timeout:
            return None

        except requests.exceptions.RequestException:
            return None

    def enriquecer_ips_con_geolocalizacion(self, ips):
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