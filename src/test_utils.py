
from parsers.json_parser import leer_eventos_json
from utils.data_utils import (
    obtener_ips_unicas,
    crear_resumen_evento,
    obtener_ips_criticas
)


def test_obtener_ips_unicas():
    registros = [
        {"ip": "10.0.0.1"},
        {"ip": "10.0.0.2"},
        {"ip": "10.0.0.1"},
    ]

    resultado = obtener_ips_unicas(registros)

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

    assert resultado == {"10.0.0.1"}


def test_obtener_ips_criticas_sin_eventos():
    resultado = obtener_ips_criticas([])

    assert resultado == set()


def test_utilidades_con_eventos_reales():
    eventos = leer_eventos_json("data/events.json")

    ips_unicas = obtener_ips_unicas(eventos)
    ips_criticas = obtener_ips_criticas(eventos)
    resumen = crear_resumen_evento(eventos[0])

    assert len(ips_unicas) == 3
    assert len(ips_criticas) == 2
    assert isinstance(resumen, tuple)
    assert len(resumen) == 3
