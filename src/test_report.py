import json

from src.services.report_service import (
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

    assert resumen == {
        "porcentaje_http_500": 30.0,
        "ips_criticas": [
            "192.168.1.10",
            "203.0.113.25",
        ],
        "geolocalizaciones": {
            "192.168.1.10": None,
            "203.0.113.25": {
                "status": "success",
                "country": "United States",
            },
        },
    }

    assert ips_criticas == {
        "192.168.1.10",
        "203.0.113.25",
    }


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

    assert ruta_reporte.is_file()

    contenido_texto = ruta_reporte.read_text(
        encoding="utf-8"
    )

    contenido = json.loads(contenido_texto)

    assert contenido == resumen
    assert '\n    "porcentaje_http_500"' in contenido_texto
    assert '\n        "192.168.1.10": null' in contenido_texto


def test_guardar_reporte_json_con_texto_unicode(tmp_path):
    ruta_reporte = tmp_path / "report_unicode.json"

    resumen = {
        "mensaje": "Geolocalización de Quito",
    }

    guardar_reporte_json(resumen, ruta_reporte)

    assert ruta_reporte.is_file()

    contenido_texto = ruta_reporte.read_text(
        encoding="utf-8"
    )

    contenido = json.loads(contenido_texto)

    assert contenido == resumen
    assert "Geolocalización de Quito" in contenido_texto
    assert "\\u00f3" not in contenido_texto
