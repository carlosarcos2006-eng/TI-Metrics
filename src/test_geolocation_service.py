
import pytest
from unittest.mock import Mock, patch

from services.geolocation_service import GeolocationService


def test_crear_servicio_con_valores_predeterminados():
    servicio = GeolocationService()

    assert servicio.url_base == "http://ip-api.com/json"
    assert servicio.timeout == 5


def test_crear_servicio_con_configuracion_personalizada():
    servicio = GeolocationService(
        url_base="http://ejemplo.com/api/",
        timeout=10
    )

    assert servicio.url_base == "http://ejemplo.com/api"
    assert servicio.timeout == 10


def test_propiedades_de_solo_lectura():
    servicio = GeolocationService()

    with pytest.raises(AttributeError):
        servicio.url_base = "http://otra-api.com"

    with pytest.raises(AttributeError):
        servicio.timeout = 20


@pytest.mark.parametrize("url_base", ["", "   "])
def test_url_base_vacia(url_base):
    with pytest.raises(ValueError):
        GeolocationService(url_base=url_base)


def test_url_base_tipo_incorrecto():
    with pytest.raises(TypeError):
        GeolocationService(url_base=123)


@pytest.mark.parametrize("timeout", [0, -1])
def test_timeout_no_positivo(timeout):
    with pytest.raises(ValueError):
        GeolocationService(timeout=timeout)


@pytest.mark.parametrize("timeout", ["cinco", None, True])
def test_timeout_tipo_incorrecto(timeout):
    with pytest.raises(TypeError):
        GeolocationService(timeout=timeout)


@patch("services.geolocation_service.requests.get")
def test_metodo_obtener_geolocalizacion(mock_get):
    respuesta = Mock()
    respuesta.status_code = 200
    respuesta.json.return_value = {
        "status": "success",
        "country": "Ecuador",
    }
    mock_get.return_value = respuesta

    servicio = GeolocationService(timeout=10)
    resultado = servicio.obtener_geolocalizacion("8.8.8.8")

    assert resultado["country"] == "Ecuador"
    mock_get.assert_called_once_with(
        "http://ip-api.com/json/8.8.8.8",
        timeout=10,
    )


@patch.object(GeolocationService, "obtener_geolocalizacion")
def test_metodo_enriquecer_ips(mock_obtener):
    mock_obtener.return_value = {"status": "success"}

    servicio = GeolocationService()
    ips = ["8.8.8.8", "1.1.1.1"]

    resultado = servicio.enriquecer_ips_con_geolocalizacion(ips)

    assert set(resultado.keys()) == set(ips)
    assert mock_obtener.call_count == 2
