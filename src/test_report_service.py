import json
from unittest.mock import Mock

import pytest

from src.services.report_service import (
    ReportService,
    construir_resumen,
    guardar_reporte_json,
)


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

    assert servicio.indentacion == 4


@pytest.mark.parametrize("indentacion", [-1, -4])
def test_indentacion_negativa(indentacion):
    with pytest.raises(
        ValueError,
        match='La\\ indentación\\ no\\ puede\\ ser\\ negativa'
    ):
        ReportService(indentacion=indentacion)


@pytest.mark.parametrize("indentacion", ["cuatro", None, 2.5, True])
def test_indentacion_tipo_incorrecto(indentacion):
    with pytest.raises(
        TypeError,
        match='La\\ indentación\\ debe\\ ser\\ un\\ número\\ entero'
    ):
        ReportService(indentacion=indentacion)


def test_metodo_construir_resumen():
    servicio = ReportService()

    resumen = servicio.construir_resumen(
        30.0,
        {"192.168.1.10"},
        {"192.168.1.10": None}
    )

    assert resumen == {
        "porcentaje_http_500": 30.0,
        "ips_criticas": ["192.168.1.10"],
        "geolocalizaciones": {
            "192.168.1.10": None
        },
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

def test_construir_resumen_ordena_conjunto_ips():
    """Comprueba el orden determinista de las IP de un conjunto."""
    servicio = ReportService()

    ips_criticas = {
        "203.0.113.25",
        "192.168.1.10",
        "8.8.8.8",
        "1.1.1.1",
    }

    resumen = servicio.construir_resumen(
        30.0,
        ips_criticas,
        {}
    )

    assert resumen["ips_criticas"] == [
        "1.1.1.1",
        "192.168.1.10",
        "203.0.113.25",
        "8.8.8.8",
    ]

def test_construir_resumen_conserva_orden_lista_ips():
    """Comprueba que se conserva el orden de una lista recibida."""
    servicio = ReportService()

    ips_criticas = [
        "8.8.8.8",
        "1.1.1.1",
        "192.168.1.10",
    ]

    resumen = servicio.construir_resumen(
        30.0,
        ips_criticas,
        {}
    )

    assert resumen["ips_criticas"] == [
        "8.8.8.8",
        "1.1.1.1",
        "192.168.1.10",
    ]

    assert ips_criticas == [
        "8.8.8.8",
        "1.1.1.1",
        "192.168.1.10",
    ]

    assert resumen["ips_criticas"] is not ips_criticas

@pytest.mark.parametrize("porcentaje", [
    "30",
    None,
    True,
    False,
    [],
    {},
])
def test_porcentaje_tipo_incorrecto(porcentaje):
    servicio = ReportService()

    with pytest.raises(
        TypeError,
        match='El\\ porcentaje\\ HTTP\\ 500\\ debe\\ ser\\ un\\ número'
    ):
        servicio.construir_resumen(
            porcentaje,
            [],
            {}
        )

@pytest.mark.parametrize("porcentaje", [
    -1,
    100.1,
    101,
    float("inf"),
    float("-inf"),
    float("nan"),
])
def test_porcentaje_valor_invalido(porcentaje):
    servicio = ReportService()

    with pytest.raises(
        ValueError,
        match='El\\ porcentaje\\ HTTP\\ 500\\ debe\\ ser\\ finito\\ y\\ estar\\ entre\\ 0\\ y\\ 100'
    ):
        servicio.construir_resumen(
            porcentaje,
            [],
            {}
        )

@pytest.mark.parametrize("porcentaje", [
    0,
    100,
    25.5,
])
def test_porcentaje_valido(porcentaje):
    servicio = ReportService()

    resumen = servicio.construir_resumen(
        porcentaje,
        [],
        {}
    )

    assert resumen["porcentaje_http_500"] == porcentaje

@pytest.mark.parametrize("ips", [
    None,
    123,
    True,
    "8.8.8.8",
    {"ip": "8.8.8.8"},
])
def test_ips_criticas_coleccion_invalida(ips):
    servicio = ReportService()

    with pytest.raises(
        TypeError,
        match='Las\\ IP\\ críticas\\ deben\\ proporcionarse'
    ):
        servicio.construir_resumen(
            30.0,
            ips,
            {}
        )

@pytest.mark.parametrize("ip", [
    None,
    123,
    True,
    [],
    {},
])
def test_ip_critica_tipo_incorrecto(ip):
    servicio = ReportService()

    with pytest.raises(
        TypeError,
        match='La\\ dirección\\ IP\\ debe\\ ser\\ una\\ cadena\\ de\\ texto'
    ):
        servicio.construir_resumen(
            30.0,
            ["8.8.8.8", ip],
            {}
        )

@pytest.mark.parametrize("ip", [
    "",
    "   ",
    "ip_invalida",
    "999.999.999.999",
    "8.8.8.8/24",
])
def test_ip_critica_formato_invalido(ip):
    servicio = ReportService()

    with pytest.raises(
        ValueError,
        match='Dirección\\ IP\\ inválida'
    ):
        servicio.construir_resumen(
            30.0,
            [ip],
            {}
        )

@pytest.mark.parametrize("ips", [
    [],
    (),
    set(),
    frozenset(),
])
def test_colecciones_ips_vacias(ips):
    servicio = ReportService()

    resumen = servicio.construir_resumen(
        0.0,
        ips,
        {}
    )

    assert resumen == {
        "porcentaje_http_500": 0.0,
        "ips_criticas": [],
        "geolocalizaciones": {}
    }

@pytest.mark.parametrize("geolocalizaciones", [
    None,
    [],
    "Ecuador",
    123,
    True,
])
def test_geolocalizaciones_tipo_incorrecto(
        geolocalizaciones
):
    servicio = ReportService()

    with pytest.raises(
        TypeError,
        match='Las\\ geolocalizaciones\\ deben\\ proporcionarse\\ como\\ un\\ diccionario'
    ):
        servicio.construir_resumen(
            30.0,
            [],
            geolocalizaciones
        )

@pytest.mark.parametrize("clave", [
    123,
    None,
    True,
])
def test_geolocalizacion_clave_tipo_incorrecto(clave):
    servicio = ReportService()

    with pytest.raises(
        TypeError,
        match='La\\ dirección\\ IP\\ debe\\ ser\\ una\\ cadena\\ de\\ texto'
    ):
        servicio.construir_resumen(
            30.0,
            [],
            {clave: None}
        )

@pytest.mark.parametrize("clave", [
    "",
    "ip_invalida",
    "999.999.999.999",
])
def test_geolocalizacion_clave_formato_invalido(clave):
    servicio = ReportService()

    with pytest.raises(
        ValueError,
        match='Dirección\\ IP\\ inválida'
    ):
        servicio.construir_resumen(
            30.0,
            [],
            {clave: None}
        )

@pytest.mark.parametrize("valor", [
    [],
    "Ecuador",
    123,
    True,
])
def test_geolocalizacion_valor_incorrecto(valor):
    servicio = ReportService()

    with pytest.raises(
        TypeError,
        match='La\\ geolocalización\\ de\\ 8\\.8\\.8\\.8\\ debe\\ ser\\ un\\ diccionario\\ o\\ None'
    ):
        servicio.construir_resumen(
            30.0,
            ["8.8.8.8"],
            {"8.8.8.8": valor}
        )

def test_construir_resumen_con_ipv6():
    servicio = ReportService()

    ip = "2001:4860:4860::8888"

    resumen = servicio.construir_resumen(
        30.0,
        [ip],
        {ip: None}
    )

    assert resumen["ips_criticas"] == [ip]
    assert resumen["geolocalizaciones"] == {
        ip: None
    }

@pytest.mark.parametrize("resumen", [
    None,
    [],
    "reporte",
    123,
    True,
])
def test_guardar_resumen_tipo_incorrecto(
        tmp_path,
        resumen
):
    servicio = ReportService()
    ruta = tmp_path / "reporte.json"

    with pytest.raises(
        TypeError,
        match='El\\ resumen\\ debe\\ ser\\ un\\ diccionario'
    ):
        servicio.guardar_reporte_json(
            resumen,
            ruta
        )

    assert not ruta.exists()



@pytest.mark.parametrize("ruta", [None, 123, True, [], {}])
def test_ruta_reporte_tipo_incorrecto(ruta, monkeypatch):

    servicio = ReportService()

    apertura = Mock(
        side_effect=AssertionError(
            "No se debe abrir un archivo con una ruta de tipo incorrecto."
        )
    )

    with monkeypatch.context() as m:
        m.setattr("builtins.open", apertura)

        with pytest.raises(
            TypeError,
            match='La\\ ruta\\ del\\ reporte\\ debe\\ ser\\ una\\ cadena\\ de\\ texto'
        ):
            servicio.guardar_reporte_json({}, ruta)

    apertura.assert_not_called()



@pytest.mark.parametrize("ruta", ["", "   "])
def test_ruta_reporte_vacia(ruta, monkeypatch):

    servicio = ReportService()

    apertura = Mock(
        side_effect=AssertionError(
            "No se debe abrir un archivo con una ruta vacía."
        )
    )

    with monkeypatch.context() as m:
        m.setattr("builtins.open", apertura)

        with pytest.raises(
            ValueError,
            match='La\\ ruta\\ del\\ reporte\\ no\\ puede\\ estar\\ vacía'
        ):
            servicio.guardar_reporte_json({}, ruta)

    apertura.assert_not_called()


def test_guardar_reporte_directorio_inexistente(tmp_path):
    servicio = ReportService()

    ruta = (
        tmp_path
        / "directorio_inexistente"
        / "reporte.json"
    )

    with pytest.raises(
        FileNotFoundError,
        match="No se encontró la ruta del reporte"
    ):
        servicio.guardar_reporte_json(
            {},
            ruta
        )

    assert not ruta.exists()

def test_guardar_reporte_sin_permisos(
        tmp_path,
        monkeypatch
):
    servicio = ReportService()
    ruta = tmp_path / "reporte.json"

    apertura = Mock(side_effect=PermissionError())

    with monkeypatch.context() as m:
        m.setattr("builtins.open", apertura)

        with pytest.raises(
            PermissionError,
            match="No tienes permisos para guardar el reporte"
        ) as error:
            servicio.guardar_reporte_json({}, ruta)

    apertura.assert_called_once_with(
        str(ruta),
        mode="w",
        encoding="utf-8",
    )

    assert isinstance(error.value.__cause__, PermissionError)
    assert not ruta.exists()

def test_guardar_reporte_no_serializable(tmp_path):
    servicio = ReportService()
    ruta = tmp_path / "reporte.json"

    resumen = {
        "datos": {1, 2, 3}
    }

    with pytest.raises(
        TypeError,
        match='El\\ resumen\\ contiene\\ datos\\ no\\ serializables\\ a\\ JSON'
    ):
        servicio.guardar_reporte_json(
            resumen,
            ruta
        )

    assert not ruta.exists()

@pytest.mark.parametrize("valor", [
    float("inf"),
    float("-inf"),
    float("nan"),
])
def test_guardar_reporte_valores_no_finitos(
        tmp_path,
        valor
):
    servicio = ReportService()
    ruta = tmp_path / "reporte.json"

    resumen = {
        "valor": valor
    }

    with pytest.raises(
        ValueError,
        match='El\\ resumen\\ contiene\\ valores\\ inválidos\\ para\\ JSON'
    ):
        servicio.guardar_reporte_json(
            resumen,
            ruta
        )

    assert not ruta.exists()

def test_conservar_reporte_ante_error_serializacion(
        tmp_path
):
    servicio = ReportService()
    ruta = tmp_path / "reporte.json"

    contenido_original = '{"estado": "valido"}'

    ruta.write_text(
        contenido_original,
        encoding="utf-8"
    )

    resumen_invalido = {
        "datos": {1, 2, 3}
    }

    with pytest.raises(
        TypeError,
        match='El\\ resumen\\ contiene\\ datos\\ no\\ serializables\\ a\\ JSON'
    ):
        servicio.guardar_reporte_json(
            resumen_invalido,
            ruta
        )

    assert ruta.read_text(
        encoding="utf-8"
    ) == contenido_original

def test_indentacion_cero(tmp_path):
    servicio = ReportService(indentacion=0)

    assert servicio.indentacion == 0

    ruta = tmp_path / "reporte_indentacion_cero.json"

    resumen = {
        "mensaje": "Geolocalización de Quito",
        "porcentaje_http_500": 30.0,
    }

    servicio.guardar_reporte_json(resumen, ruta)

    contenido_texto = ruta.read_text(encoding="utf-8")

    assert json.loads(contenido_texto) == resumen

    assert contenido_texto == (
        '{\n'
        '"mensaje": "Geolocalización de Quito",\n'
        '"porcentaje_http_500": 30.0\n'
        '}'
    )

@pytest.mark.parametrize("ips, resultado_esperado", [
    (
        ("8.8.8.8", "1.1.1.1"),
        ["8.8.8.8", "1.1.1.1"]
    ),
    (
        frozenset({"8.8.8.8", "1.1.1.1"}),
        ["1.1.1.1", "8.8.8.8"]
    ),
])
def test_construir_resumen_colecciones_validas(
        ips,
        resultado_esperado
):
    servicio = ReportService()

    resumen = servicio.construir_resumen(
        30.0,
        ips,
        {}
    )

    assert resumen["ips_criticas"] == resultado_esperado


def test_guardar_reporte_ruta_texto(tmp_path):
    servicio = ReportService()

    ruta = tmp_path / "reporte_texto.json"

    resumen = {
        "porcentaje_http_500": 30.0
    }

    servicio.guardar_reporte_json(
        resumen,
        str(ruta)
    )

    assert json.loads(
        ruta.read_text(encoding="utf-8")
    ) == resumen


def test_conservar_reporte_ante_valor_no_finito(tmp_path):
    servicio = ReportService()

    ruta = tmp_path / "reporte.json"

    contenido_original = '{"estado": "valido"}'

    ruta.write_text(
        contenido_original,
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError,
        match='El\\ resumen\\ contiene\\ valores\\ inválidos\\ para\\ JSON'
    ):
        servicio.guardar_reporte_json(
            {"valor": float("nan")},
            ruta
        )

    assert ruta.read_text(
        encoding="utf-8"
    ) == contenido_original


def test_wrapper_construir_resumen_invalido():

    with pytest.raises(
        ValueError,
        match='El\\ porcentaje\\ HTTP\\ 500\\ debe\\ ser\\ finito\\ y\\ estar\\ entre\\ 0\\ y\\ 100'
    ):
        construir_resumen(
            101,
            [],
            {}
        )


def test_wrapper_guardar_reporte_invalido(tmp_path):

    ruta = tmp_path / "reporte.json"

    with pytest.raises(
        TypeError,
        match='El\\ resumen\\ contiene\\ datos\\ no\\ serializables\\ a\\ JSON'
    ):
        guardar_reporte_json(
            {"datos": {1, 2, 3}},
            ruta
        )

    assert not ruta.exists()
