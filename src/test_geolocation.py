
from unittest.mock import Mock, patch

import requests

from services.geolocation_service import (
    obtener_geolocalizacion,
    enriquecer_ips_con_geolocalizacion,
)


@patch("services.geolocation_service.requests.get")
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

    assert resultado["status"] == "success"
    assert resultado["country"] == "United States"
    assert resultado["city"] == "Ashburn"
    mock_get.assert_called_once_with(
        "http://ip-api.com/json/8.8.8.8",
        timeout=5,
    )


@patch("services.geolocation_service.requests.get")
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


@patch("services.geolocation_service.requests.get")
def test_obtener_geolocalizacion_error_http(mock_get):
    respuesta = Mock()
    respuesta.status_code = 500
    mock_get.return_value = respuesta

    resultado = obtener_geolocalizacion("8.8.8.8")

    assert resultado is None


@patch("services.geolocation_service.requests.get")
def test_obtener_geolocalizacion_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout

    resultado = obtener_geolocalizacion("8.8.8.8")

    assert resultado is None


@patch("services.geolocation_service.requests.get")
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

    assert set(resultado.keys()) == ips
    assert resultado["8.8.8.8"]["country"] == "United States"
    assert resultado["1.1.1.1"]["country"] == "United States"
    assert mock_get.call_count == 2


def test_obtener_geolocalizacion_error_conexion():
    with patch(
        "services.geolocation_service.requests.get",
        side_effect=requests.exceptions.ConnectionError(
            "Error de conexión"
        ),
    ):
        resultado = obtener_geolocalizacion("8.8.8.8")

    assert resultado is None
