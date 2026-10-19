
import json

from services.report_service import (
    construir_resumen,
    guardar_reporte_json,
)


def test_construir_resumen():
    porcentaje_500 = 30.0
    ips_criticas = {"192.168.1.10", "203.0.113.25"}
    geolocalizaciones = {
        "192.168.1.10": None,
        "203.0.113.25": {
            "status": "success",
            "country": "United States",
        },
    }

    resumen = construir_resumen(
        porcentaje_500,
        ips_criticas,
        geolocalizaciones,
    )

    assert resumen["porcentaje_http_500"] == 30.0
    assert set(resumen["ips_criticas"]) == ips_criticas
    assert resumen["geolocalizaciones"] == geolocalizaciones


def test_guardar_reporte_json(tmp_path):
    ruta_reporte = tmp_path / "report.json"

    resumen = {
        "porcentaje_http_500": 30.0,
        "ips_criticas": ["192.168.1.10"],
        "geolocalizaciones": {
            "192.168.1.10": None,
        },
    }

    guardar_reporte_json(resumen, ruta_reporte)

    assert ruta_reporte.exists()

    with open(ruta_reporte, "r", encoding="utf-8") as archivo:
        contenido = json.load(archivo)

    assert contenido == resumen


def test_guardar_reporte_json_con_texto_unicode(tmp_path):
    ruta_reporte = tmp_path / "report_unicode.json"

    resumen = {
        "mensaje": "Geolocalización de Quito",
    }

    guardar_reporte_json(resumen, ruta_reporte)

    with open(ruta_reporte, "r", encoding="utf-8") as archivo:
        contenido = json.load(archivo)

    assert contenido == resumen
