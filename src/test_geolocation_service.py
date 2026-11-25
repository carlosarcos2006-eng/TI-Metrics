import pytest
from unittest.mock import Mock, patch, call

from requests.exceptions import JSONDecodeError

from src.services.geolocation_service import (
    GeolocationService,
    obtener_geolocalizacion,
    enriquecer_ips_con_geolocalizacion,
)


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

    assert servicio.url_base == "http://ip-api.com/json"
    assert servicio.timeout == 5


@pytest.mark.parametrize("url_base", ["", "   "])
def test_url_base_vacia(url_base):
    with pytest.raises(ValueError, match="La URL base no puede estar vacía"):
        GeolocationService(url_base=url_base)


def test_url_base_tipo_incorrecto():
    with pytest.raises(TypeError, match="La URL base debe ser una cadena de texto"):
        GeolocationService(url_base=123)


@pytest.mark.parametrize("timeout", [0, -1])
def test_timeout_no_positivo(timeout):
    with pytest.raises(ValueError, match="El timeout debe ser positivo y finito"):
        GeolocationService(timeout=timeout)


@pytest.mark.parametrize("timeout", ["cinco", None, True])
def test_timeout_tipo_incorrecto(timeout):
    with pytest.raises(TypeError, match="El timeout debe ser un número"):
        GeolocationService(timeout=timeout)


@patch("src.services.geolocation_service.requests.get")
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

    assert resultado == {
        "status": "success",
        "country": "Ecuador",
    }
    respuesta.json.assert_called_once_with()
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

    assert resultado == {
        "8.8.8.8": {"status": "success"},
        "1.1.1.1": {"status": "success"},
    }
    assert mock_obtener.call_args_list == [
        call("8.8.8.8"),
        call("1.1.1.1"),
    ]

@pytest.mark.parametrize("timeout", [
    float("inf"),
    float("-inf"),
    float("nan"),
])
def test_timeout_no_finito(timeout):
    with pytest.raises(
        ValueError,
        match="El timeout debe ser positivo y finito"
    ):
        GeolocationService(timeout=timeout)

@pytest.mark.parametrize("url_base", [
    "///",
    "ejemplo.com",
    "ftp://ejemplo.com",
    "http://",
    "https://",
])
def test_url_base_estructura_invalida(url_base):
    with pytest.raises(
        ValueError,
        match="La URL base debe utilizar HTTP o HTTPS"
    ):
        GeolocationService(url_base=url_base)


def test_timeout_decimal_valido():
    servicio = GeolocationService(timeout=2.5)

    assert servicio.timeout == 2.5

@pytest.mark.parametrize("ip", [
    None,
    123,
    True,
    [],
    {},
])
@patch("src.services.geolocation_service.requests.get")
def test_ip_tipo_incorrecto(mock_get, ip):
    servicio = GeolocationService()

    with pytest.raises(TypeError, match="La dirección IP debe ser una cadena de texto"):
        servicio.obtener_geolocalizacion(ip)

    mock_get.assert_not_called()


@pytest.mark.parametrize("ip", [
    "",
    "   ",
    "ip_invalida",
    "999.999.999.999",
    "192.168.1",
    "8.8.8.8/24",
])
@patch("src.services.geolocation_service.requests.get")
def test_ip_formato_invalido(mock_get, ip):
    servicio = GeolocationService()

    with pytest.raises(ValueError, match="Dirección IP inválida"):
        servicio.obtener_geolocalizacion(ip)

    mock_get.assert_not_called()

@patch("src.services.geolocation_service.requests.get")
def test_geolocalizacion_ipv6(mock_get):
    respuesta = Mock()
    respuesta.status_code = 200
    respuesta.json.return_value = {
        "status": "success"
    }

    mock_get.return_value = respuesta

    servicio = GeolocationService()
    ip = "2001:4860:4860::8888"

    assert servicio.obtener_geolocalizacion(ip) == {
        "status": "success"
    }

    mock_get.assert_called_once_with(
        f"http://ip-api.com/json/{ip}",
        timeout=5
    )

@pytest.mark.parametrize("datos", [
    [],
    None,
    123,
    True,
    "respuesta_invalida",
    {},
    {"country": "Ecuador"},
])
@patch("src.services.geolocation_service.requests.get")
def test_respuesta_json_estructura_invalida(mock_get, datos):
    respuesta = Mock()
    respuesta.status_code = 200
    respuesta.json.return_value = datos

    mock_get.return_value = respuesta

    servicio = GeolocationService()

    assert servicio.obtener_geolocalizacion("8.8.8.8") is None

@patch("src.services.geolocation_service.requests.get")
def test_respuesta_json_malformada(mock_get):

    respuesta = Mock()
    respuesta.status_code = 200
    respuesta.json.side_effect = JSONDecodeError(
        "JSON inválido",
        "",
        0
    )

    mock_get.return_value = respuesta

    servicio = GeolocationService()

    assert servicio.obtener_geolocalizacion("8.8.8.8") is None

@pytest.mark.parametrize("ips", [
    None,
    123,
    True,
    "8.8.8.8",
    {"ip": "8.8.8.8"},
])
@patch("src.services.geolocation_service.requests.get")
def test_coleccion_ips_tipo_incorrecto(mock_get, ips):
    servicio = GeolocationService()

    with pytest.raises(TypeError, match="Las direcciones IP deben proporcionarse"):
        servicio.enriquecer_ips_con_geolocalizacion(ips)

    mock_get.assert_not_called()

@pytest.mark.parametrize("ips", [
    [],
    (),
    set(),
    frozenset(),
])
@patch("src.services.geolocation_service.requests.get")
def test_coleccion_ips_vacia(mock_get, ips):
    servicio = GeolocationService()

    assert servicio.enriquecer_ips_con_geolocalizacion(ips) == {}

    mock_get.assert_not_called()

@patch("src.services.geolocation_service.requests.get")
def test_coleccion_con_segunda_ip_invalida(mock_get):
    servicio = GeolocationService()

    ips = [
        "8.8.8.8",
        "ip_invalida"
    ]

    with pytest.raises(ValueError, match="Dirección IP inválida"):
        servicio.enriquecer_ips_con_geolocalizacion(ips)

    mock_get.assert_not_called()

@patch.object(GeolocationService, "obtener_geolocalizacion")
def test_enriquecer_ips_resultados_mixtos(mock_obtener):
    mock_obtener.side_effect = [
        {"status": "success", "country": "United States"},
        None,
        {"status": "success", "country": "Australia"},
    ]

    servicio = GeolocationService()

    ips = [
        "8.8.8.8",
        "192.168.1.10",
        "1.1.1.1",
    ]

    resultado = servicio.enriquecer_ips_con_geolocalizacion(ips)

    assert resultado == {
        "8.8.8.8": {
            "status": "success",
            "country": "United States"
        },
        "192.168.1.10": None,
        "1.1.1.1": {
            "status": "success",
            "country": "Australia"
        }
    }

    assert mock_obtener.call_args_list == [
        call("8.8.8.8"),
        call("192.168.1.10"),
        call("1.1.1.1"),
    ]

def test_normalizacion_url_base():
    servicio = GeolocationService(
        url_base="  https://ejemplo.com/api///  "
    )

    assert servicio.url_base == "https://ejemplo.com/api"

@pytest.mark.parametrize("ips", [
    ("8.8.8.8", "1.1.1.1"),
    frozenset({"8.8.8.8", "1.1.1.1"}),
])
@patch.object(GeolocationService, "obtener_geolocalizacion")
def test_colecciones_ips_validas(mock_obtener, ips):
    mock_obtener.return_value = {
        "status": "success"
    }

    servicio = GeolocationService()

    resultado = servicio.enriquecer_ips_con_geolocalizacion(
        ips
    )

    assert resultado == {
        "8.8.8.8": {"status": "success"},
        "1.1.1.1": {"status": "success"},
    }
    assert mock_obtener.call_count == 2
    mock_obtener.assert_has_calls([
        call("8.8.8.8"),
        call("1.1.1.1"),
    ], any_order=isinstance(ips, frozenset))

@patch("src.services.geolocation_service.requests.get")
def test_coleccion_con_ip_tipo_incorrecto(mock_get):
    servicio = GeolocationService()

    ips = [
        "8.8.8.8",
        123
    ]

    with pytest.raises(
        TypeError,
        match="La dirección IP debe ser una cadena de texto"
    ):
        servicio.enriquecer_ips_con_geolocalizacion(ips)

    mock_get.assert_not_called()

@patch("src.services.geolocation_service.requests.get")
def test_wrappers_geolocalizacion_argumentos_invalidos(mock_get):

    with pytest.raises(ValueError, match="Dirección IP inválida"):
        obtener_geolocalizacion("ip_invalida")

    with pytest.raises(
        TypeError,
        match="Las direcciones IP deben proporcionarse"
    ):
        enriquecer_ips_con_geolocalizacion("8.8.8.8")

    mock_get.assert_not_called()


@patch("src.services.geolocation_service.requests.get")
def test_peticion_con_configuracion_personalizada(mock_get):
    """Comprueba la URL normalizada y el timeout decimal."""
    respuesta = Mock()
    respuesta.status_code = 200
    respuesta.json.return_value = {
        "status": "success",
        "country": "Australia",
        "city": "Sydney",
    }

    mock_get.return_value = respuesta

    servicio = GeolocationService(
        url_base="  https://ejemplo.com/api///  ",
        timeout=2.5,
    )

    resultado = servicio.obtener_geolocalizacion("1.1.1.1")

    assert resultado == {
        "status": "success",
        "country": "Australia",
        "city": "Sydney",
    }

    mock_get.assert_called_once_with(
        "https://ejemplo.com/api/1.1.1.1",
        timeout=2.5,
    )

    respuesta.json.assert_called_once_with()
