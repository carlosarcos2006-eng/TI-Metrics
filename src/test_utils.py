
from parsers.json_parser import leer_eventos_json
from utils.data_utils import (
    obtener_ips_unicas,
    crear_resumen_evento,
    obtener_ips_criticas
)
from src.utils.data_utils import deduplicar_eventos

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

def test_deduplicar_eventos_repetidos():
    eventos = [
        {"ip": "192.168.1.10", "event": "login", "severity": "INFO"},
        {"ip": "192.168.1.10", "event": "login", "severity": "INFO"},
        {"ip": "8.8.8.8", "event": "error", "severity": "CRITICAL"}
    ]

    resultado = deduplicar_eventos(eventos)

    assert len(resultado) == 2
    assert resultado[0] == eventos[0]
    assert resultado[1] == eventos[2]


def test_deduplicar_eventos_sin_duplicados():
    eventos = [
        {"ip": "192.168.1.10", "event": "login"},
        {"ip": "192.168.1.10", "event": "logout"}
    ]

    resultado = deduplicar_eventos(eventos)

    assert resultado == eventos


def test_deduplicar_eventos_lista_vacia():
    resultado = deduplicar_eventos([])

    assert resultado == []
