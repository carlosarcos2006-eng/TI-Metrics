
import json

import pytest

from services.report_service import ReportService


def test_constructor_valores_predeterminados():
    servicio = ReportService()

    assert servicio.indentacion == 4


def test_constructor_indentacion_personalizada():
    servicio = ReportService(indentacion=2)

    assert servicio.indentacion == 2


def test_propiedad_indentacion_solo_lectura():
    servicio = ReportService()

    with pytest.raises(AttributeError):
        servicio.indentacion = 8


@pytest.mark.parametrize("indentacion", [-1, -4])
def test_indentacion_negativa(indentacion):
    with pytest.raises(ValueError):
        ReportService(indentacion=indentacion)


@pytest.mark.parametrize("indentacion", ["cuatro", None, 2.5, True])
def test_indentacion_tipo_incorrecto(indentacion):
    with pytest.raises(TypeError):
        ReportService(indentacion=indentacion)


def test_metodo_construir_resumen():
    servicio = ReportService()

    resumen = servicio.construir_resumen(
        30.0,
        {"192.168.1.10"},
        {"192.168.1.10": None}
    )

    assert resumen["porcentaje_http_500"] == 30.0
    assert resumen["ips_criticas"] == ["192.168.1.10"]
    assert resumen["geolocalizaciones"] == {
        "192.168.1.10": None
    }


def test_metodo_guardar_reporte_json(tmp_path):
    servicio = ReportService(indentacion=2)
    ruta = tmp_path / "reporte_poo.json"

    resumen = {
        "mensaje": "Geolocalización de Quito",
        "porcentaje_http_500": 30.0
    }

    servicio.guardar_reporte_json(resumen, ruta)

    assert ruta.exists()

    contenido_texto = ruta.read_text(encoding="utf-8")
    contenido_json = json.loads(contenido_texto)

    assert contenido_json == resumen
    assert '\n  "mensaje"' in contenido_texto
    assert "Geolocalización de Quito" in contenido_texto
