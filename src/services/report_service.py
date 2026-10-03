import json


def construir_resumen(porcentaje_500, ips_criticas, geolocalizaciones):
    resumen = {
        "porcentaje_http_500": porcentaje_500,
        "ips_criticas": list(ips_criticas),
        "geolocalizaciones": geolocalizaciones
    }

    return resumen


def guardar_reporte_json(resumen, ruta_archivo):
    with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, indent=4, ensure_ascii=False)