
import json

from parsers.json_parser import leer_eventos_json


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
    import pytest

    ruta = tmp_path / "eventos_inexistentes.json"

    with pytest.raises(FileNotFoundError, match="No se encontró"):
        leer_eventos_json(ruta)


def test_leer_json_contenido_invalido(tmp_path):
    import pytest

    ruta = tmp_path / "eventos_invalidos.json"

    ruta.write_text(
        '{"eventos": [}',
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="datos inválidos"):
        leer_eventos_json(ruta)


def test_leer_json_archivo_vacio(tmp_path):
    import pytest

    ruta = tmp_path / "eventos_vacios.json"

    ruta.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="datos inválidos"):
        leer_eventos_json(ruta)
