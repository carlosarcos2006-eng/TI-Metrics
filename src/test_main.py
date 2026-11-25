from unittest.mock import Mock, call, patch

import pytest
from src.main import main


@patch("src.main.ReportService", autospec=True)
@patch("src.main.GeolocationService", autospec=True)
@patch("src.main.obtener_ips_criticas", autospec=True)
@patch("src.main.MetricsService", autospec=True)
@patch("src.main.deduplicar_eventos", autospec=True)
@patch("src.main.JSONLogParser", autospec=True)
@patch("src.main.CSVLogParser", autospec=True)
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
    registros = [
        {"status": estado}
        for estado in [
            200, 500, 200, 404, 500,
            200, 201, 500, 200, 403,
        ]
    ]
    eventos = [
        {
            "ip": "192.168.1.10",
            "event": "login",
            "severity": "CRITICAL",
        }
    ]

    eventos.append(eventos[0].copy())

    eventos_deduplicados = [eventos[0]]

    # Configurar lectura CSV y JSON
    mock_csv_parser.return_value.leer.return_value = registros
    mock_json_parser.return_value.leer.return_value = eventos

    # Configurar deduplicación
    mock_deduplicar.return_value = eventos_deduplicados

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

    # Registrar el orden de interacción entre componentes.
    coordinador = Mock()

    coordinador.attach_mock(mock_csv_parser, "csv")
    coordinador.attach_mock(mock_json_parser, "json")
    coordinador.attach_mock(mock_deduplicar, "deduplicar")
    coordinador.attach_mock(mock_metrics_service, "metricas")
    coordinador.attach_mock(mock_ips_criticas, "ips_criticas")
    coordinador.attach_mock(
        mock_geolocation_service,
        "geolocalizacion",
    )
    coordinador.attach_mock(mock_report_service, "reporte")

    # Ejecutar el programa principal.
    resultado = main()

    assert coordinador.mock_calls == [
        call.csv("data/logs.csv"),
        call.json("data/events.json"),
        call.csv().leer(),
        call.json().leer(),
        call.deduplicar(eventos),
        call.metricas(registros),
        call.metricas().calcular_porcentaje_http_500(),
        call.ips_criticas(eventos_deduplicados),
        call.geolocalizacion(),
        call.geolocalizacion().enriquecer_ips_con_geolocalizacion(
            ips_criticas
        ),
        call.reporte(),
        call.reporte().construir_resumen(
            30.0,
            ips_criticas,
            geolocalizaciones,
        ),
        call.reporte().guardar_reporte_json(
            resumen,
            "data/report.json",
        ),
    ]

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
    mock_ips_criticas.assert_called_once_with(eventos_deduplicados)

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

    assert captura.out.splitlines() == [
        "TI-Metrics iniciado correctamente",
        "Porcentaje HTTP 500: 30.0 %",
        "Cantidad de IP críticas: 1",
        "Reporte generado en: data/report.json",
    ]

    # Verificar ejecución satisfactoria
    assert resultado == 0
    assert captura.err == ""


# Pruebas de manejo de excepciones


@pytest.fixture
def componentes_main():
    """Simula los componentes utilizados por main()."""

    with (
        patch("src.main.CSVLogParser", autospec=True) as csv_parser,
        patch("src.main.JSONLogParser", autospec=True) as json_parser,
        patch("src.main.deduplicar_eventos", autospec=True) as deduplicar,
        patch("src.main.MetricsService", autospec=True) as metricas,
        patch("src.main.obtener_ips_criticas", autospec=True) as ips_criticas,
        patch("src.main.GeolocationService", autospec=True) as geolocalizacion,
        patch("src.main.ReportService", autospec=True) as reporte,
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
    assert captura.err == f"Error en TI-Metrics: {excepcion}\n"
    assert captura.out == "TI-Metrics iniciado correctamente\n"

    componentes_main["csv"].return_value.leer.assert_called_once_with()
    componentes_main["json"].return_value.leer.assert_not_called()
    componentes_main["deduplicar"].assert_not_called()
    componentes_main["ips_criticas"].assert_not_called()
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
    assert captura.err == f"Error en TI-Metrics: {excepcion}\n"
    assert captura.out == "TI-Metrics iniciado correctamente\n"

    componentes_main["csv"].return_value.leer.assert_called_once_with()
    componentes_main["json"].return_value.leer.assert_called_once_with()
    componentes_main["deduplicar"].assert_not_called()
    componentes_main["ips_criticas"].assert_not_called()
    componentes_main["geolocalizacion"].assert_not_called()
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
    assert captura.err == "Error en TI-Metrics: Evento incompatible con JSON\n"
    assert captura.out == "TI-Metrics iniciado correctamente\n"

    componentes_main["metricas"].assert_not_called()
    componentes_main["ips_criticas"].assert_not_called()
    componentes_main["geolocalizacion"].assert_not_called()
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
    assert captura.err == "Error en TI-Metrics: Estado HTTP inválido\n"
    assert captura.out == "TI-Metrics iniciado correctamente\n"

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
    assert captura.err == "Error en TI-Metrics: Dirección IP inválida\n"
    assert captura.out == "TI-Metrics iniciado correctamente\n"

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
    assert captura.err == "Error en TI-Metrics: Dirección IP inválida para geolocalización\n"
    assert captura.out == "TI-Metrics iniciado correctamente\n"

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
    assert captura.err == "Error en TI-Metrics: Resumen inválido\n"
    assert captura.out == "TI-Metrics iniciado correctamente\n"

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
    assert captura.err == f"Error en TI-Metrics: {excepcion}\n"
    assert captura.out == "TI-Metrics iniciado correctamente\n"

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

    with pytest.raises(type(excepcion)) as error:
        main()

    assert error.value is excepcion

    captura = capsys.readouterr()

    assert captura.out == "TI-Metrics iniciado correctamente\n"
    assert captura.err == ""

    componentes_main["json"].return_value.leer.assert_not_called()
    componentes_main["deduplicar"].assert_not_called()
    componentes_main["metricas"].assert_not_called()
    componentes_main["ips_criticas"].assert_not_called()
    componentes_main["geolocalizacion"].assert_not_called()
    componentes_main["reporte"].assert_not_called()
