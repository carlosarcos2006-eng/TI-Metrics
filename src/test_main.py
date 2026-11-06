
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
    main()

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

    # Verificar los mensajes de la terminal
    salida = capsys.readouterr().out

    assert "TI-Metrics iniciado correctamente" in salida
    assert "Porcentaje HTTP 500: 30.0 %" in salida
    assert "Cantidad de IP críticas: 1" in salida
    assert "Reporte generado en: data/report.json" in salida