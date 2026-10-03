import requests


def obtener_geolocalizacion(ip):
    url = f"http://ip-api.com/json/{ip}"

    try:
        respuesta = requests.get(url, timeout=5)

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


def enriquecer_ips_con_geolocalizacion(ips):
    resultados = {}

    for ip in ips:
        resultados[ip] = obtener_geolocalizacion(ip)

    return resultados