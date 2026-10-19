
from unittest.mock import patch, call

from main import main


@patch("main.guardar_reporte_json")
@patch("main.construir_resumen")
@patch("main.enriquecer_ips_con_geolocalizacion")
@patch("main.obtener_ips_criticas")
@patch("main.calcular_porcentaje_http_500")
@patch("main.leer_eventos_json")
@patch("main.leer_logs_csv")
def test_main_coordina_modulos(
    mock_leer_logs,
    mock_leer_eventos,
    mock_calcular_porcentaje,
    mock_ips_criticas,
    mock_geolocalizaciones,
    mock_construir_resumen,
    mock_guardar_reporte,
    capsys,
):
    mock_leer_logs.return_value = [{"status": 500}]
    mock_leer_eventos.return_value = [{"ip": "192.168.1.10"}]
    mock_calcular_porcentaje.return_value = 30.0
    mock_ips_criticas.return_value = {"192.168.1.10"}
    mock_geolocalizaciones.return_value = {
        "192.168.1.10": None
    }
    mock_construir_resumen.return_value = {
        "porcentaje_http_500": 30.0,
        "ips_criticas": ["192.168.1.10"],
        "geolocalizaciones": {"192.168.1.10": None},
    }

    main()

    mock_leer_logs.assert_called_once_with("data/logs.csv")
    mock_leer_eventos.assert_called_once_with("data/events.json")

    mock_calcular_porcentaje.assert_called_once_with(
        [{"status": 500}]
    )
    mock_ips_criticas.assert_called_once_with(
        [{"ip": "192.168.1.10"}]
    )

    mock_geolocalizaciones.assert_called_once_with(
        {"192.168.1.10"}
    )

    mock_construir_resumen.assert_called_once_with(
        30.0,
        {"192.168.1.10"},
        {"192.168.1.10": None},
    )

    mock_guardar_reporte.assert_called_once_with(
        mock_construir_resumen.return_value,
        "data/report.json",
    )

    salida = capsys.readouterr().out

    assert "TI-Metrics iniciado correctamente" in salida
    assert "Porcentaje HTTP 500: 30.0 %" in salida
    assert "Cantidad de IP críticas: 1" in salida
    assert "Reporte generado en: data/report.json" in salida
