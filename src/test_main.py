
import pytest

from unittest.mock import patch
from main import main


@patch("main.ReportService")
@patch("main.GeolocationService")
@patch("main.obtener_ips_criticas")
@patch("main.MetricsService")
@patch("main.deduplicar_eventos")
@patch("main.JSONLogParser")
@patch("main.CSVLogParser")
def test_main_coordina_modulos(
    mock_csv_parser,
    mock_json_parser,
    mock_deduplicar,
    mock_metrics_service,
    mock_ips_criticas,
    mock_geolocation_service,
    mock_report_service,
    capsys,
):
    # Datos simulados para los analizadores
    registros = [{"status": 500}]
    eventos = [
        {
            "ip": "192.168.1.10",
            "event": "login",
            "severity": "CRITICAL",
        }
    ]

    # Configurar lectura CSV y JSON
    mock_csv_parser.return_value.leer.return_value = registros
    mock_json_parser.return_value.leer.return_value = eventos

    # Configurar deduplicación
    mock_deduplicar.return_value = eventos

    # Configurar métricas
    mock_metrics_service.return_value.calcular_porcentaje_http_500.return_value = 30.0

    # Configurar IP críticas
    ips_criticas = {"192.168.1.10"}
    mock_ips_criticas.return_value = ips_criticas

    # Configurar geolocalización
    geolocalizaciones = {"192.168.1.10": None}

    mock_geolocation_service.return_value.enriquecer_ips_con_geolocalizacion.return_value = (
        geolocalizaciones
    )

    # Configurar reporte
    resumen = {
        "porcentaje_http_500": 30.0,
        "ips_criticas": ["192.168.1.10"],
        "geolocalizaciones": geolocalizaciones,
    }

    mock_report_service.return_value.construir_resumen.return_value = resumen

    # Ejecutar el programa principal
    resultado = main()

    # Verificar creación de analizadores
    mock_csv_parser.assert_called_once_with("data/logs.csv")
    mock_json_parser.assert_called_once_with("data/events.json")

    # Verificar lectura de archivos
    mock_csv_parser.return_value.leer.assert_called_once_with()
    mock_json_parser.return_value.leer.assert_called_once_with()

    # Verificar deduplicación
    mock_deduplicar.assert_called_once_with(eventos)

    # Verificar servicio de métricas
    mock_metrics_service.assert_called_once_with(registros)

    mock_metrics_service.return_value.calcular_porcentaje_http_500.assert_called_once_with()

    # Verificar IP críticas
    mock_ips_criticas.assert_called_once_with(eventos)

    # Verificar geolocalización
    mock_geolocation_service.assert_called_once_with()

    mock_geolocation_service.return_value.enriquecer_ips_con_geolocalizacion.assert_called_once_with(
        ips_criticas
    )

    # Verificar construcción y persistencia del reporte
    mock_report_service.assert_called_once_with()

    mock_report_service.return_value.construir_resumen.assert_called_once_with(
        30.0,
        ips_criticas,
        geolocalizaciones,
    )

    mock_report_service.return_value.guardar_reporte_json.assert_called_once_with(
        resumen,
        "data/report.json",
    )

    # Verificar mensajes de la terminal
    captura = capsys.readouterr()

    assert "TI-Metrics iniciado correctamente" in captura.out
    assert "Porcentaje HTTP 500: 30.0 %" in captura.out
    assert "Cantidad de IP críticas: 1" in captura.out
    assert "Reporte generado en: data/report.json" in captura.out

    # Verificar ejecución satisfactoria
    assert resultado == 0
    assert captura.err == ""


# Pruebas de manejo de excepciones


@pytest.fixture
def componentes_main():
    """Simula los componentes utilizados por main()."""

    with (
        patch("main.CSVLogParser") as csv_parser,
        patch("main.JSONLogParser") as json_parser,
        patch("main.deduplicar_eventos") as deduplicar,
        patch("main.MetricsService") as metricas,
        patch("main.obtener_ips_criticas") as ips_criticas,
        patch("main.GeolocationService") as geolocalizacion,
        patch("main.ReportService") as reporte,
    ):
        registros = [{"status": 500}]

        eventos = [
            {
                "ip": "192.168.1.10",
                "event": "login",
                "severity": "CRITICAL",
            }
        ]

        csv_parser.return_value.leer.return_value = registros
        json_parser.return_value.leer.return_value = eventos
        deduplicar.return_value = eventos

        metricas.return_value.calcular_porcentaje_http_500.return_value = 100.0

        ips_criticas.return_value = {"192.168.1.10"}

        geolocalizacion.return_value.enriquecer_ips_con_geolocalizacion.return_value = {
            "192.168.1.10": None
        }

        reporte.return_value.construir_resumen.return_value = {
            "porcentaje_http_500": 100.0,
            "ips_criticas": ["192.168.1.10"],
            "geolocalizaciones": {"192.168.1.10": None},
        }

        yield {
            "csv": csv_parser,
            "json": json_parser,
            "deduplicar": deduplicar,
            "metricas": metricas,
            "ips_criticas": ips_criticas,
            "geolocalizacion": geolocalizacion,
            "reporte": reporte,
        }


@pytest.mark.parametrize(
    "excepcion",
    [
        FileNotFoundError("Archivo CSV inexistente"),
        PermissionError("Permisos insuficientes para leer CSV"),
        ValueError("Datos CSV inválidos"),
        TypeError("Tipo de dato CSV incorrecto"),
    ],
)
def test_main_error_lectura_csv(
    componentes_main,
    capsys,
    excepcion,
):
    componentes_main["csv"].return_value.leer.side_effect = excepcion

    resultado = main()
    captura = capsys.readouterr()

    assert resultado == 1
    assert str(excepcion) in captura.err
    assert "Reporte generado en:" not in captura.out

    componentes_main["json"].return_value.leer.assert_not_called()
    componentes_main["metricas"].assert_not_called()
    componentes_main["geolocalizacion"].assert_not_called()
    componentes_main["reporte"].assert_not_called()


@pytest.mark.parametrize(
    "excepcion",
    [
        FileNotFoundError("Archivo JSON inexistente"),
        PermissionError("Permisos insuficientes para leer JSON"),
        ValueError("Datos JSON inválidos"),
        TypeError("Tipo de dato JSON incorrecto"),
    ],
)
def test_main_error_lectura_json(
    componentes_main,
    capsys,
    excepcion,
):
    componentes_main["json"].return_value.leer.side_effect = excepcion

    resultado = main()
    captura = capsys.readouterr()

    assert resultado == 1
    assert str(excepcion) in captura.err
    assert "Reporte generado en:" not in captura.out

    componentes_main["csv"].return_value.leer.assert_called_once()
    componentes_main["deduplicar"].assert_not_called()
    componentes_main["metricas"].assert_not_called()
    componentes_main["reporte"].assert_not_called()


def test_main_error_deduplicacion(
    componentes_main,
    capsys,
):
    componentes_main["deduplicar"].side_effect = ValueError(
        "Evento incompatible con JSON"
    )

    resultado = main()
    captura = capsys.readouterr()

    assert resultado == 1
    assert "Evento incompatible con JSON" in captura.err
    assert "Reporte generado en:" not in captura.out

    componentes_main["metricas"].assert_not_called()
    componentes_main["reporte"].assert_not_called()


def test_main_error_metricas(
    componentes_main,
    capsys,
):
    componentes_main["metricas"].side_effect = ValueError(
        "Estado HTTP inválido"
    )

    resultado = main()
    captura = capsys.readouterr()

    assert resultado == 1
    assert "Estado HTTP inválido" in captura.err
    assert "Reporte generado en:" not in captura.out

    componentes_main["ips_criticas"].assert_not_called()
    componentes_main["geolocalizacion"].assert_not_called()
    componentes_main["reporte"].assert_not_called()


def test_main_error_ips_criticas(
    componentes_main,
    capsys,
):
    componentes_main["ips_criticas"].side_effect = ValueError(
        "Dirección IP inválida"
    )

    resultado = main()
    captura = capsys.readouterr()

    assert resultado == 1
    assert "Dirección IP inválida" in captura.err
    assert "Reporte generado en:" not in captura.out

    componentes_main["geolocalizacion"].assert_not_called()
    componentes_main["reporte"].assert_not_called()


def test_main_error_geolocalizacion(
    componentes_main,
    capsys,
):
    componentes_main[
        "geolocalizacion"
    ].return_value.enriquecer_ips_con_geolocalizacion.side_effect = ValueError(
        "Dirección IP inválida para geolocalización"
    )

    resultado = main()
    captura = capsys.readouterr()

    assert resultado == 1
    assert "Dirección IP inválida para geolocalización" in captura.err
    assert "Reporte generado en:" not in captura.out

    componentes_main["reporte"].assert_not_called()


def test_main_error_construccion_reporte(
    componentes_main,
    capsys,
):
    componentes_main[
        "reporte"
    ].return_value.construir_resumen.side_effect = ValueError(
        "Resumen inválido"
    )

    resultado = main()
    captura = capsys.readouterr()

    assert resultado == 1
    assert "Resumen inválido" in captura.err
    assert "Reporte generado en:" not in captura.out

    componentes_main[
        "reporte"
    ].return_value.guardar_reporte_json.assert_not_called()


@pytest.mark.parametrize(
    "excepcion",
    [
        FileNotFoundError("Ruta del reporte inexistente"),
        PermissionError("Permisos insuficientes para guardar reporte"),
        OSError("Error de escritura del reporte"),
        TypeError("Reporte no serializable"),
        ValueError("Contenido JSON inválido"),
    ],
)
def test_main_error_guardado_reporte(
    componentes_main,
    capsys,
    excepcion,
):
    componentes_main[
        "reporte"
    ].return_value.guardar_reporte_json.side_effect = excepcion

    resultado = main()
    captura = capsys.readouterr()

    assert resultado == 1
    assert str(excepcion) in captura.err
    assert "Reporte generado en:" not in captura.out

    componentes_main[
        "reporte"
    ].return_value.construir_resumen.assert_called_once()


@pytest.mark.parametrize(
    "excepcion",
    [
        RuntimeError("Error inesperado"),
        AttributeError("Atributo inexistente"),
        KeyError("Clave inesperada"),
    ],
)
def test_main_propaga_excepciones_inesperadas(
    componentes_main,
    capsys,
    excepcion,
):
    componentes_main["csv"].return_value.leer.side_effect = excepcion

    with pytest.raises(type(excepcion)):
        main()

    captura = capsys.readouterr()

    assert "Reporte generado en:" not in captura.out
    componentes_main["reporte"].assert_not_called()