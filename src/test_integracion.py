import json
import runpy
import shutil
import warnings
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.main import main


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]


@pytest.fixture
def entorno_integracion(tmp_path, monkeypatch):
    """Prepara copias temporales de los datos originales."""

    directorio_datos = tmp_path / "data"
    directorio_datos.mkdir()

    for nombre in ("logs.csv", "events.json"):
        shutil.copy2(
            RAIZ_PROYECTO / "data" / nombre,
            directorio_datos / nombre,
        )

    monkeypatch.chdir(tmp_path)

    return directorio_datos


@pytest.fixture
def api_geolocalizacion():
    """Simula exclusivamente las respuestas HTTP externas."""

    respuestas = {
        "192.168.1.10": {
            "status": "fail",
            "message": "private range",
            "query": "192.168.1.10",
        },
        "203.0.113.25": {
            "status": "success",
            "country": "United States",
            "city": "New York",
            "query": "203.0.113.25",
        },
    }

    def responder(url, timeout):
        ip = url.rsplit("/", 1)[-1]

        respuesta = Mock()
        respuesta.status_code = 200
        respuesta.json.return_value = respuestas[ip]

        return respuesta

    with patch(
        "src.services.geolocation_service.requests.get",
        autospec=True,
        side_effect=responder,
    ) as peticion:
        yield peticion


def leer_reporte(directorio_datos):
    """Lee el reporte generado durante una prueba."""

    ruta = directorio_datos / "report.json"

    assert ruta.is_file()

    return json.loads(
        ruta.read_text(encoding="utf-8")
    )


def reporte_esperado():
    """Define el resultado esperado de los datos originales."""

    return {
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
                "city": "New York",
                "query": "203.0.113.25",
            },
        },
    }


def test_integracion_datos_originales(
    entorno_integracion,
    api_geolocalizacion,
    capsys,
):
    """Comprueba el procesamiento completo de datos reales."""

    resultado = main()
    captura = capsys.readouterr()

    assert resultado == 0
    assert captura.err == ""

    assert captura.out.splitlines() == [
        "TI-Metrics iniciado correctamente",
        "Porcentaje HTTP 500: 30.0 %",
        "Cantidad de IP críticas: 2",
        "Reporte generado en: data/report.json",
    ]

    assert (
        leer_reporte(entorno_integracion)
        == reporte_esperado()
    )

    assert api_geolocalizacion.call_count == 2

    ips_consultadas = {
        llamada.args[0].rsplit("/", 1)[-1]
        for llamada in api_geolocalizacion.call_args_list
    }

    assert ips_consultadas == {
        "192.168.1.10",
        "203.0.113.25",
    }


def test_integracion_eventos_duplicados(
    entorno_integracion,
    api_geolocalizacion,
):
    """Comprueba la integración con eventos repetidos."""

    ruta = entorno_integracion / "events.json"

    eventos = json.loads(
        ruta.read_text(encoding="utf-8")
    )

    eventos.extend([
        eventos[2].copy(),
        eventos[3].copy(),
    ])

    assert len(eventos) == 8

    ruta.write_text(
        json.dumps(eventos, ensure_ascii=False),
        encoding="utf-8",
    )

    resultado = main()

    assert resultado == 0

    assert (
        leer_reporte(entorno_integracion)
        == reporte_esperado()
    )

    assert api_geolocalizacion.call_count == 2


def test_integracion_archivos_vacios(
    entorno_integracion,
    api_geolocalizacion,
    capsys,
):
    """Comprueba archivos sin registros, pero válidos."""

    ruta_csv = entorno_integracion / "logs.csv"
    ruta_json = entorno_integracion / "events.json"

    encabezado = (
        ruta_csv.read_text(encoding="utf-8")
        .splitlines()[0]
    )

    ruta_csv.write_text(
        encabezado + "\n",
        encoding="utf-8",
    )

    ruta_json.write_text(
        "[]",
        encoding="utf-8",
    )

    resultado = main()
    captura = capsys.readouterr()

    assert resultado == 0
    assert captura.err == ""

    assert captura.out.splitlines() == [
        "TI-Metrics iniciado correctamente",
        "Porcentaje HTTP 500: 0.0 %",
        "Cantidad de IP críticas: 0",
        "Reporte generado en: data/report.json",
    ]

    assert leer_reporte(entorno_integracion) == {
        "porcentaje_http_500": 0.0,
        "ips_criticas": [],
        "geolocalizaciones": {},
    }

    api_geolocalizacion.assert_not_called()


def ejecutar_punto_entrada():
    """Ejecuta src.main como módulo principal."""

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=(
                r"'src\.main' found in sys\.modules "
                r"after import of package 'src'.*"
            ),
            category=RuntimeWarning,
        )

        runpy.run_module(
            "src.main",
            run_name="__main__",
        )


def test_cli_ejecucion_satisfactoria(
    entorno_integracion,
    api_geolocalizacion,
    capsys,
):
    """Comprueba el código de salida CLI satisfactorio."""

    with pytest.raises(SystemExit) as salida:
        ejecutar_punto_entrada()

    captura = capsys.readouterr()

    assert salida.value.code == 0
    assert captura.err == ""

    assert captura.out.splitlines() == [
        "TI-Metrics iniciado correctamente",
        "Porcentaje HTTP 500: 30.0 %",
        "Cantidad de IP críticas: 2",
        "Reporte generado en: data/report.json",
    ]

    assert (
        leer_reporte(entorno_integracion)
        == reporte_esperado()
    )

    assert api_geolocalizacion.call_count == 2


def test_cli_ejecucion_fallida(
    entorno_integracion,
    api_geolocalizacion,
    capsys,
):
    """Comprueba el código de salida CLI ante un error."""

    ruta_csv = entorno_integracion / "logs.csv"
    ruta_csv.unlink()

    with pytest.raises(SystemExit) as salida:
        ejecutar_punto_entrada()

    captura = capsys.readouterr()

    assert salida.value.code == 1

    assert captura.out == (
        "TI-Metrics iniciado correctamente\n"
    )

    assert captura.err.startswith(
        "Error en TI-Metrics:"
    )

    assert "data/logs.csv" in captura.err

    assert not (
        entorno_integracion / "report.json"
    ).exists()

    api_geolocalizacion.assert_not_called()
