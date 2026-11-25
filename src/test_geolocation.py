from unittest.mock import Mock, patch, call

import requests

from src.services.geolocation_service import (
    obtener_geolocalizacion,
    enriquecer_ips_con_geolocalizacion,
)


@patch("src.services.geolocation_service.requests.get")
def test_obtener_geolocalizacion_exitosa(mock_get):
    respuesta = Mock()
    respuesta.status_code = 200
    respuesta.json.return_value = {
        "status": "success",
        "country": "United States",
        "city": "Ashburn",
    }
    mock_get.return_value = respuesta

    resultado = obtener_geolocalizacion("8.8.8.8")

    assert resultado == {
        "status": "success",
        "country": "United States",
        "city": "Ashburn",
    }
    mock_get.assert_called_once_with(
        "http://ip-api.com/json/8.8.8.8",
        timeout=5,
    )


@patch("src.services.geolocation_service.requests.get")
def test_obtener_geolocalizacion_ip_no_encontrada(mock_get):
    respuesta = Mock()
    respuesta.status_code = 200
    respuesta.json.return_value = {
        "status": "fail",
        "message": "private range",
    }
    mock_get.return_value = respuesta

    resultado = obtener_geolocalizacion("192.168.1.10")

    assert resultado is None
    mock_get.assert_called_once_with(
        "http://ip-api.com/json/192.168.1.10",
        timeout=5,
    )
    respuesta.json.assert_called_once_with()


@patch("src.services.geolocation_service.requests.get")
def test_obtener_geolocalizacion_error_http(mock_get):
    respuesta = Mock()
    respuesta.status_code = 500
    mock_get.return_value = respuesta

    resultado = obtener_geolocalizacion("8.8.8.8")

    assert resultado is None
    mock_get.assert_called_once_with(
        "http://ip-api.com/json/8.8.8.8",
        timeout=5,
    )
    respuesta.json.assert_not_called()


@patch("src.services.geolocation_service.requests.get")
def test_obtener_geolocalizacion_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout

    resultado = obtener_geolocalizacion("8.8.8.8")

    assert resultado is None
    mock_get.assert_called_once_with(
        "http://ip-api.com/json/8.8.8.8",
        timeout=5,
    )


@patch("src.services.geolocation_service.requests.get")
def test_enriquecer_ips_con_geolocalizacion(mock_get):
    respuesta = Mock()
    respuesta.status_code = 200
    respuesta.json.return_value = {
        "status": "success",
        "country": "United States",
    }
    mock_get.return_value = respuesta

    ips = {"8.8.8.8", "1.1.1.1"}

    resultado = enriquecer_ips_con_geolocalizacion(ips)

    assert resultado == {
        "8.8.8.8": {
            "status": "success",
            "country": "United States",
        },
        "1.1.1.1": {
            "status": "success",
            "country": "United States",
        },
    }

    assert mock_get.call_count == 2
    mock_get.assert_has_calls([
        call("http://ip-api.com/json/8.8.8.8", timeout=5),
        call("http://ip-api.com/json/1.1.1.1", timeout=5),
    ], any_order=True)

    assert respuesta.json.call_count == 2


def test_obtener_geolocalizacion_error_conexion():
    with patch(
        "src.services.geolocation_service.requests.get",
        side_effect=requests.exceptions.ConnectionError(
            "Error de conexión"
        ),
    ) as mock_get:
        resultado = obtener_geolocalizacion("8.8.8.8")

    assert resultado is None
    mock_get.assert_called_once_with(
        "http://ip-api.com/json/8.8.8.8",
        timeout=5,
    )
