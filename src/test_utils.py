from copy import deepcopy
from pathlib import Path
import re

import pytest

from src.parsers.json_parser import leer_eventos_json
from src.utils.data_utils import (
    obtener_ips_unicas,
    crear_resumen_evento,
    obtener_ips_criticas,
    deduplicar_eventos,
    validar_ip,
)

def test_obtener_ips_unicas():
    registros = [
        {"ip": "10.0.0.1"},
        {"ip": "10.0.0.2"},
        {"ip": "10.0.0.1"},
    ]

    resultado = obtener_ips_unicas(registros)

    assert isinstance(resultado, set)
    assert resultado == {"10.0.0.1", "10.0.0.2"}
    assert len(resultado) == 2


def test_obtener_ips_unicas_sin_registros():
    resultado = obtener_ips_unicas([])

    assert resultado == set()


def test_crear_resumen_evento():
    evento = {
        "ip": "10.0.0.1",
        "event": "login",
        "severity": "INFO"
    }

    resultado = crear_resumen_evento(evento)

    assert resultado == ("10.0.0.1", "login", "INFO")
    assert isinstance(resultado, tuple)


def test_obtener_ips_criticas():
    eventos = [
        {"ip": "10.0.0.1", "severity": "CRITICAL"},
        {"ip": "10.0.0.2", "severity": "INFO"},
        {"ip": "10.0.0.1", "severity": "CRITICAL"},
    ]

    resultado = obtener_ips_criticas(eventos)

    assert isinstance(resultado, set)
    assert resultado == {"10.0.0.1"}


def test_obtener_ips_criticas_sin_eventos():
    resultado = obtener_ips_criticas([])

    assert resultado == set()


def test_utilidades_con_eventos_reales():
    ruta = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "events.json"
    )

    eventos = leer_eventos_json(ruta)

    ips_unicas = obtener_ips_unicas(eventos)
    ips_criticas = obtener_ips_criticas(eventos)
    resumen = crear_resumen_evento(eventos[0])

    assert len(eventos) == 6

    assert isinstance(ips_unicas, set)
    assert ips_unicas == {
        "8.8.8.8",
        "192.168.1.10",
        "203.0.113.25",
    }

    assert isinstance(ips_criticas, set)
    assert ips_criticas == {
        "192.168.1.10",
        "203.0.113.25",
    }

    assert isinstance(resumen, tuple)
    assert resumen == ("8.8.8.8", "login", "INFO")

    eventos_unicos = deduplicar_eventos(eventos)

    assert eventos_unicos == eventos
    assert eventos_unicos is not eventos

    assert all(
        unico is original
        for unico, original in zip(eventos_unicos, eventos)
    )

def test_deduplicar_eventos_repetidos():
    eventos = [
        {"ip": "192.168.1.10", "event": "login", "severity": "INFO"},
        {"ip": "192.168.1.10", "event": "login", "severity": "INFO"},
        {"ip": "8.8.8.8", "event": "error", "severity": "CRITICAL"}
    ]

    resultado = deduplicar_eventos(eventos)

    assert isinstance(resultado, list)

    assert resultado == [
        {
            "ip": "192.168.1.10",
            "event": "login",
            "severity": "INFO",
        },
        {
            "ip": "8.8.8.8",
            "event": "error",
            "severity": "CRITICAL",
        },
    ]

    assert resultado[0] is eventos[0]
    assert resultado[1] is eventos[2]
    assert len(eventos) == 3


def test_deduplicar_eventos_sin_duplicados():
    eventos = [
        {"ip": "192.168.1.10", "event": "login"},
        {"ip": "192.168.1.10", "event": "logout"}
    ]

    resultado = deduplicar_eventos(eventos)

    assert resultado == [
        {"ip": "192.168.1.10", "event": "login"},
        {"ip": "192.168.1.10", "event": "logout"},
    ]

    assert resultado is not eventos
    assert resultado[0] is eventos[0]
    assert resultado[1] is eventos[1]


def test_deduplicar_eventos_lista_vacia():
    resultado = deduplicar_eventos([])

    assert resultado == []

@pytest.mark.parametrize("registros", [
    None,
    123,
    True,
    "registros",
    {},
])
def test_ips_unicas_coleccion_invalida(registros):
    with pytest.raises(
        TypeError,
        match='proporcionarse como una lista'
    ):
        obtener_ips_unicas(registros)


@pytest.mark.parametrize("registro", [
    None,
    123,
    True,
    "registro",
    [],
])
def test_ips_unicas_registro_invalido(registro):
    with pytest.raises(
        ValueError,
        match='Datos inválidos en el registro 1: se esperaba un diccionario'
    ):
        obtener_ips_unicas([registro])


def test_ips_unicas_campo_faltante():
    with pytest.raises(ValueError, match="el registro 1: falta el campo obligatorio 'ip'"):
        obtener_ips_unicas([{}])


@pytest.mark.parametrize("ip", [
    None,
    123,
    True,
    [],
    {},
    "",
    "   ",
    "ip_invalida",
    "999.999.999.999",
])
def test_ips_unicas_direccion_invalida(ip):
    if not isinstance(ip, str) or not ip.strip():
        mensaje = (
            "el registro 1: el campo 'ip' debe ser "
            "una cadena de texto no vacía"
        )
    else:
        mensaje = "el registro 1: dirección IP inválida"

    with pytest.raises(ValueError, match=mensaje):
        obtener_ips_unicas([{"ip": ip}])


def test_ips_unicas_ipv6():
    ip = "2001:4860:4860::8888"

    resultado = obtener_ips_unicas([
        {"ip": ip},
        {"ip": ip}
    ])

    assert resultado == {ip}


@pytest.mark.parametrize("evento", [
    None,
    123,
    True,
    [],
    "evento",
])
def test_resumen_evento_tipo_incorrecto(evento):
    with pytest.raises(
        TypeError,
        match='El evento debe ser un diccionario'
    ):
        crear_resumen_evento(evento)


@pytest.mark.parametrize("campo", [
    "ip",
    "event",
    "severity",
])
def test_resumen_evento_campo_faltante(campo):
    evento = {
        "ip": "8.8.8.8",
        "event": "login",
        "severity": "INFO"
    }

    del evento[campo]

    with pytest.raises(ValueError, match=rf"el evento: falta el campo obligatorio '{campo}'"):
        crear_resumen_evento(evento)


@pytest.mark.parametrize("campo", [
    "ip",
    "event",
    "severity",
])
@pytest.mark.parametrize("valor", [
    None,
    123,
    True,
    [],
    {},
    "",
    "   ",
])
def test_resumen_evento_campo_invalido(campo, valor):
    evento = {
        "ip": "8.8.8.8",
        "event": "login",
        "severity": "INFO"
    }

    evento[campo] = valor

    with pytest.raises(
        ValueError,
        match=rf"el evento: el campo '{campo}' debe ser "
              r"una cadena de texto no vacía"
    ):
        crear_resumen_evento(evento)


def test_resumen_evento_ip_formato_invalido():
    evento = {
        "ip": "ip_invalida",
        "event": "login",
        "severity": "INFO"
    }

    with pytest.raises(
        ValueError,
        match='Datos inválidos en el evento: dirección IP inválida'
    ):
        crear_resumen_evento(evento)


@pytest.mark.parametrize("eventos", [
    None,
    123,
    True,
    "eventos",
    {},
])
def test_ips_criticas_coleccion_invalida(eventos):
    with pytest.raises(
        TypeError,
        match='proporcionarse como una lista'
    ):
        obtener_ips_criticas(eventos)


@pytest.mark.parametrize("evento", [
    None,
    123,
    True,
    [],
    "evento",
])
def test_ips_criticas_evento_invalido(evento):
    with pytest.raises(
        ValueError,
        match='Datos inválidos en el evento 1: se esperaba un diccionario'
    ):
        obtener_ips_criticas([evento])


@pytest.mark.parametrize("campo", [
    "ip",
    "severity",
])
def test_ips_criticas_campo_faltante(campo):
    evento = {
        "ip": "8.8.8.8",
        "severity": "CRITICAL"
    }

    del evento[campo]

    with pytest.raises(ValueError, match=rf"el evento 1: falta el campo obligatorio '{campo}'"):
        obtener_ips_criticas([evento])


@pytest.mark.parametrize("campo", [
    "ip",
    "severity",
])
@pytest.mark.parametrize("valor", [
    None,
    123,
    True,
    [],
    {},
    "",
    "   ",
])
def test_ips_criticas_campo_invalido(campo, valor):
    evento = {
        "ip": "8.8.8.8",
        "severity": "CRITICAL"
    }

    evento[campo] = valor

    with pytest.raises(
        ValueError,
        match=rf"el evento 1: el campo '{campo}' debe ser "
              r"una cadena de texto no vacía"
    ):
        obtener_ips_criticas([evento])


def test_ips_criticas_ip_formato_invalido():
    eventos = [
        {
            "ip": "ip_invalida",
            "severity": "CRITICAL"
        }
    ]

    with pytest.raises(
        ValueError,
        match='Datos inválidos en el evento 1: dirección IP inválida'
    ):
        obtener_ips_criticas(eventos)


def test_ips_criticas_valida_eventos_no_criticos():
    eventos = [
        {
            "ip": "ip_invalida",
            "severity": "INFO"
        }
    ]

    with pytest.raises(
        ValueError,
        match='Datos inválidos en el evento 1: dirección IP inválida'
    ):
        obtener_ips_criticas(eventos)


def test_ips_criticas_sensible_mayusculas():
    eventos = [
        {
            "ip": "8.8.8.8",
            "severity": "critical"
        },
        {
            "ip": "1.1.1.1",
            "severity": "CRITICAL"
        }
    ]

    assert obtener_ips_criticas(eventos) == {
        "1.1.1.1"
    }


@pytest.mark.parametrize("eventos", [
    None,
    123,
    True,
    "eventos",
    {},
])
def test_deduplicar_coleccion_invalida(eventos):
    with pytest.raises(
        TypeError,
        match='proporcionarse como una lista'
    ):
        deduplicar_eventos(eventos)


@pytest.mark.parametrize("evento", [
    None,
    123,
    True,
    [],
    "evento",
])
def test_deduplicar_evento_invalido(evento):
    with pytest.raises(
        ValueError,
        match='Datos inválidos en el evento 1: se esperaba un diccionario'
    ):
        deduplicar_eventos([evento])


def test_deduplicar_diccionarios_anidados():
    eventos = [
        {
            "ip": "8.8.8.8",
            "metadata": {
                "usuario": "admin",
                "intentos": 3
            }
        },
        {
            "ip": "8.8.8.8",
            "metadata": {
                "intentos": 3,
                "usuario": "admin"
            }
        }
    ]

    resultado = deduplicar_eventos(eventos)

    assert len(resultado) == 1
    assert resultado[0] is eventos[0]


def test_deduplicar_listas_anidadas():
    eventos = [
        {"datos": [1, 2, 3]},
        {"datos": [1, 2, 3]},
        {"datos": [3, 2, 1]}
    ]

    resultado = deduplicar_eventos(eventos)

    assert resultado == [
        eventos[0],
        eventos[2]
    ]


def test_deduplicar_estructuras_complejas():
    eventos = [
        {
            "datos": [
                {"usuario": "admin"},
                {"usuario": "invitado"}
            ]
        },
        {
            "datos": [
                {"usuario": "admin"},
                {"usuario": "invitado"}
            ]
        }
    ]

    resultado = deduplicar_eventos(eventos)

    assert len(resultado) == 1
    assert resultado[0] is eventos[0]


def test_deduplicar_conserva_primera_instancia():
    evento1 = {"ip": "8.8.8.8"}
    evento2 = {"ip": "8.8.8.8"}

    resultado = deduplicar_eventos([
        evento1,
        evento2
    ])

    assert len(resultado) == 1
    assert resultado[0] is evento1


def test_deduplicar_conserva_datos_originales():

    eventos = [
        {"datos": [1, 2, 3]},
        {"datos": [1, 2, 3]}
    ]

    copia_original = deepcopy(eventos)

    deduplicar_eventos(eventos)

    assert eventos == copia_original


@pytest.mark.parametrize("valor", [
    {1, 2, 3},
    object(),
    float("inf"),
    float("-inf"),
    float("nan"),
])
def test_deduplicar_datos_no_compatibles_json(valor):
    eventos = [
        {"datos": valor}
    ]

    with pytest.raises(
        ValueError,
        match="el evento 1: el contenido no es compatible con JSON"
    ) as error:
        deduplicar_eventos(eventos)

    if isinstance(valor, float):
        assert isinstance(error.value.__cause__, ValueError)
        assert (
            "Los valores numéricos deben ser finitos"
            in str(error.value.__cause__)
        )
    else:
        assert isinstance(error.value.__cause__, TypeError)
        assert (
            "Tipo de dato incompatible con JSON"
            in str(error.value.__cause__)
        )

@pytest.mark.parametrize("ip", [
    "8.8.8.8",
    "1.1.1.1",
    "192.168.1.10",
    "127.0.0.1",
    "0.0.0.0",
    "255.255.255.255",
    "::1",
    "2001:4860:4860::8888",
])
def test_validar_ip_correcta(ip):

    assert validar_ip(ip) is None


@pytest.mark.parametrize("ip", [
    None,
    123,
    True,
    False,
    [],
    {},
    8.8,
])
def test_validar_ip_tipo_incorrecto(ip):

    with pytest.raises(
        TypeError,
        match='La dirección IP debe ser una cadena de texto'
    ):
        validar_ip(ip)


@pytest.mark.parametrize("ip", [
    "",
    "   ",
    "ip_invalida",
    "999.999.999.999",
    "8.8.8.8/24",
    "8.8.8",
    "256.1.1.1",
    " 8.8.8.8 ",
    "2001:::1",
])
def test_validar_ip_formato_incorrecto(ip):

    with pytest.raises(
        ValueError,
        match=re.escape(f"Dirección IP inválida: {ip!r}")
    ) as error:
        validar_ip(ip)

    assert isinstance(error.value.__cause__, ValueError)

@pytest.mark.parametrize(
    "valor_1, valor_2",
    [
        (1, 1.0),
        (0, 0.0),
        (0.0, -0.0),
        (True, 1),
        (False, 0),
    ]
)
def test_deduplicar_valores_equivalentes(valor_1, valor_2):
    evento_1 = {"cantidad": valor_1}
    evento_2 = {"cantidad": valor_2}

    resultado = deduplicar_eventos(
        [evento_1, evento_2]
    )

    assert len(resultado) == 1
    assert resultado[0] is evento_1


def test_deduplicar_numeros_equivalentes_anidados():
    evento_1 = {
        "datos": {
            "valores": [1, 2, 3]
        }
    }

    evento_2 = {
        "datos": {
            "valores": [1.0, 2.0, 3.0]
        }
    }

    resultado = deduplicar_eventos(
        [evento_1, evento_2]
    )

    assert len(resultado) == 1
    assert resultado[0] is evento_1


@pytest.mark.parametrize(
    "valor_1, valor_2",
    [
        ("1", 1),
        (10, 20),
        (None, 0),
        ([], {}),
        ([1, 2], [2, 1]),
    ]
)
def test_deduplicar_valores_realmente_distintos(
    valor_1, valor_2
):
    evento_1 = {"datos": valor_1}
    evento_2 = {"datos": valor_2}

    resultado = deduplicar_eventos(
        [evento_1, evento_2]
    )

    assert len(resultado) == 2
    assert resultado[0] is evento_1
    assert resultado[1] is evento_2

def test_deduplicar_diccionario_circular():
    evento = {}
    evento["datos"] = evento

    with pytest.raises(
        ValueError,
        match="el evento 1: el contenido no es compatible con JSON"
    ) as error:
        deduplicar_eventos([evento])

    assert isinstance(error.value.__cause__, RecursionError)

def test_deduplicar_lista_circular():
    datos = []
    datos.append(datos)

    evento = {"datos": datos}

    with pytest.raises(
        ValueError,
        match="el evento 1: el contenido no es compatible con JSON"
    ) as error:
        deduplicar_eventos([evento])

    assert isinstance(error.value.__cause__, RecursionError)

def test_deduplicar_referencia_circular_indirecta():
    evento = {}
    datos = [evento]
    evento["datos"] = datos

    with pytest.raises(
        ValueError,
        match="el evento 1: el contenido no es compatible con JSON"
    ) as error:
        deduplicar_eventos([evento])

    assert isinstance(error.value.__cause__, RecursionError)

@pytest.mark.parametrize(
    "clave",
    [
        123,
        1.5,
        True,
        None,
        ("clave", 1),
    ]
)
def test_deduplicar_claves_json_invalidas(clave):
    evento = {clave: "valor"}

    with pytest.raises(
        ValueError,
        match="el evento 1: el contenido no es compatible con JSON"
    ) as error:
        deduplicar_eventos([evento])

    assert isinstance(error.value.__cause__, ValueError)

def test_deduplicar_clave_anidada_invalida():
    evento = {
        "datos": {
            123: "valor"
        }
    }

    with pytest.raises(
        ValueError,
        match="el evento 1: el contenido no es compatible con JSON"
    ) as error:
        deduplicar_eventos([evento])

    assert isinstance(error.value.__cause__, ValueError)

@pytest.mark.parametrize(
    "valor",
    [
        (1, 2),
        b"datos",
        frozenset({1, 2}),
        complex(1, 2),
    ]
)
def test_deduplicar_tipos_no_admitidos(valor):
    evento = {"datos": valor}

    with pytest.raises(
        ValueError,
        match="el evento 1: el contenido no es compatible con JSON"
    ) as error:
        deduplicar_eventos([evento])

    assert isinstance(error.value.__cause__, TypeError)

def test_deduplicar_referencias_compartidas_validas():
    datos = [1, 2, 3]

    evento_1 = {
        "origen": datos,
        "destino": datos
    }

    evento_2 = {
        "origen": [1, 2, 3],
        "destino": [1, 2, 3]
    }

    resultado = deduplicar_eventos(
        [evento_1, evento_2]
    )

    assert len(resultado) == 1
    assert resultado[0] is evento_1

def test_deduplicar_estructuras_vacias_distintas():
    evento_1 = {"datos": []}
    evento_2 = {"datos": {}}
    evento_3 = {"datos": None}

    resultado = deduplicar_eventos(
        [evento_1, evento_2, evento_3]
    )

    assert len(resultado) == 3
    assert resultado[0] is evento_1
    assert resultado[1] is evento_2
    assert resultado[2] is evento_3

def test_deduplicar_evento_invalido_segunda_posicion():
    evento_1 = {"cantidad": 10}
    evento_2 = {"cantidad": float("nan")}

    with pytest.raises(
        ValueError,
        match="el evento 2: el contenido no es compatible con JSON"
    ) as error:
        deduplicar_eventos(
            [evento_1, evento_2]
        )

    assert isinstance(error.value.__cause__, ValueError)
    assert (
        "Los valores numéricos deben ser finitos"
        in str(error.value.__cause__)
    )

def test_deduplicar_valores_json_validos():
    evento_1 = {
        "datos": [
            None,
            True,
            False,
            "Información",
            10,
            2.5,
            [],
            {}
        ]
    }

    evento_2 = {
        "datos": [
            None,
            True,
            False,
            "Información",
            10,
            2.5,
            [],
            {}
        ]
    }

    resultado = deduplicar_eventos(
        [evento_1, evento_2]
    )

    assert len(resultado) == 1
    assert resultado[0] is evento_1
