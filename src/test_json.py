import json
import pytest
from unittest.mock import patch
from src.parsers.json_parser import leer_eventos_json

@pytest.mark.parametrize("contenido", [
    {},
    "evento",
    123,
    True,
    None,
])
def test_leer_json_estructura_invalida(tmp_path, contenido):
    ruta = tmp_path / "estructura_invalida.json"

    ruta.write_text(
        json.dumps(contenido),
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="lista"):
        leer_eventos_json(ruta)

@pytest.mark.parametrize("evento", [
    123,
    "login",
    None,
    True,
    [],
])
def test_leer_json_evento_tipo_incorrecto(tmp_path, evento):
    ruta = tmp_path / "evento_invalido.json"

    ruta.write_text(
        json.dumps([evento]),
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError,
        match="evento 1: el evento debe ser un diccionario"
    ):
        leer_eventos_json(ruta)

@pytest.mark.parametrize("campo", [
    "ip",
    "event",
    "severity",
])
def test_leer_json_campo_faltante(tmp_path, campo):
    ruta = tmp_path / "campo_faltante.json"

    evento = {
        "ip": "8.8.8.8",
        "event": "login",
        "severity": "INFO"
    }

    del evento[campo]

    ruta.write_text(
        json.dumps([evento]),
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError,
        match=f"evento 1: falta el campo obligatorio '{campo}'"
    ):
        leer_eventos_json(ruta)

@pytest.mark.parametrize("campo", [
    "ip",
    "event",
    "severity",
])
@pytest.mark.parametrize("valor", [
    "",
    "   ",
    None,
    123,
    True,
    [],
    {},
])
def test_leer_json_campo_valor_invalido(
        tmp_path, campo, valor
):
    ruta = tmp_path / "valor_invalido.json"

    evento = {
        "ip": "8.8.8.8",
        "event": "login",
        "severity": "INFO"
    }

    evento[campo] = valor

    ruta.write_text(
        json.dumps([evento]),
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError,
        match=f"evento 1: el campo '{campo}' debe ser una cadena no vacía"
    ):
        leer_eventos_json(ruta)

@pytest.mark.parametrize("ruta", [
    123,
    None,
    True,
])
def test_leer_json_ruta_tipo_incorrecto(ruta):
    with pytest.raises(TypeError):
        leer_eventos_json(ruta)

def test_leer_json_sin_permisos():
    ruta = "data/events.json"

    with patch("builtins.open", side_effect=PermissionError):
        with pytest.raises(
            PermissionError,
            match="No tienes permisos para leer el archivo JSON"
        ):
            leer_eventos_json(ruta)

def test_leer_json_campos_adicionales(tmp_path):
    ruta = tmp_path / "campos_adicionales.json"

    eventos = [
        {
            "ip": "8.8.8.8",
            "event": "login",
            "severity": "INFO",
            "timestamp": "2026-09-27 08:15:30",
            "origen": "servidor_01"
        }
    ]

    ruta.write_text(
        json.dumps(eventos),
        encoding="utf-8"
    )

    assert leer_eventos_json(ruta) == eventos

def test_leer_json_eventos_duplicados(tmp_path):
    ruta = tmp_path / "eventos_duplicados.json"

    evento = {
        "ip": "8.8.8.8",
        "event": "login",
        "severity": "INFO"
    }

    eventos = [evento, evento.copy()]

    ruta.write_text(
        json.dumps(eventos),
        encoding="utf-8"
    )
    assert leer_eventos_json(ruta) == eventos

def test_leer_eventos_json():
    ruta = "data/events.json"

    eventos = leer_eventos_json(ruta)

    assert len(eventos) == 6
    assert isinstance(eventos, list)

def test_primer_evento_json():
    ruta = "data/events.json"

    eventos = leer_eventos_json(ruta)

    assert "ip" in eventos[0]
    assert "event" in eventos[0]
    assert "severity" in eventos[0]

def test_leer_json_con_lista_vacia(tmp_path):
    ruta = tmp_path / "eventos_vacios.json"

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump([], archivo)

    eventos = leer_eventos_json(ruta)

    assert eventos == []
    assert isinstance(eventos, list)

def test_leer_json_archivo_inexistente(tmp_path):
    ruta = tmp_path / "eventos_inexistentes.json"

    with pytest.raises(FileNotFoundError, match="No se encontró"):
        leer_eventos_json(ruta)

def test_leer_json_contenido_invalido(tmp_path):
    ruta = tmp_path / "eventos_invalidos.json"

    ruta.write_text(
        '{"eventos": [}',
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="datos inválidos"):
        leer_eventos_json(ruta)

def test_leer_json_archivo_vacio(tmp_path):
    ruta = tmp_path / "eventos_vacios.json"

    ruta.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="datos inválidos"):
        leer_eventos_json(ruta)

def test_leer_json_segundo_evento_invalido(tmp_path):
    ruta = tmp_path / "segundo_evento_invalido.json"

    eventos = [
        {
            "ip": "8.8.8.8",
            "event": "login",
            "severity": "INFO"
        },
        {
            "ip": "192.168.1.10",
            "event": "server_error",
            "severity": ""
        }
    ]

    ruta.write_text(
        json.dumps(eventos),
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError,
        match="evento 2: el campo 'severity' debe ser una cadena no vacía"
    ):
        leer_eventos_json(ruta)