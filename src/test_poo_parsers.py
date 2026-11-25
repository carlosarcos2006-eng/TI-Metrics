import json

import pytest

from src.models.base_log_parser import BaseLogParser
from src.parsers.csv_parser import CSVLogParser
from src.parsers.json_parser import JSONLogParser


def test_base_log_parser_no_se_puede_instanciar():
    with pytest.raises(TypeError):
        BaseLogParser("data/logs.csv")


def test_clase_hija_sin_implementar_leer():
    class ParserIncompleto(BaseLogParser):
        pass

    with pytest.raises(TypeError):
        ParserIncompleto("data/logs.csv")


def test_parsers_heredan_de_base_log_parser():
    assert issubclass(CSVLogParser, BaseLogParser)
    assert issubclass(JSONLogParser, BaseLogParser)


def test_polimorfismo_parsers(tmp_path):
    ruta_csv = tmp_path / "logs.csv"
    ruta_json = tmp_path / "events.json"

    ruta_csv.write_text(
        "ip,status,response_time\n"
        "8.8.8.8,500,120\n",
        encoding="utf-8"
    )

    eventos = [
        {
            "ip": "8.8.8.8",
            "event": "login",
            "severity": "CRITICAL"
        }
    ]

    ruta_json.write_text(
        json.dumps(eventos),
        encoding="utf-8"
    )

    parsers = [
        CSVLogParser(str(ruta_csv)),
        JSONLogParser(str(ruta_json))
    ]

    resultados = []

    for parser in parsers:
        assert isinstance(parser, BaseLogParser)
        resultados.append(parser.leer())

    assert resultados[0] == [
        {
            "ip": "8.8.8.8",
            "status": 500,
            "response_time": 120
        }
    ]

    assert resultados[1] == eventos


@pytest.mark.parametrize("clase_parser", [
    CSVLogParser,
    JSONLogParser
])
def test_encapsulamiento_ruta_archivo(clase_parser):
    ruta = "data/archivo_prueba"

    parser = clase_parser(ruta)

    assert parser.ruta_archivo == ruta

    with pytest.raises(AttributeError):
        parser.ruta_archivo = "data/otro_archivo"

    assert parser.ruta_archivo == ruta


@pytest.mark.parametrize("clase_parser", [
    CSVLogParser,
    JSONLogParser
])
@pytest.mark.parametrize("ruta, excepcion", [
    (123, TypeError),
    (None, TypeError),
    (True, TypeError),
    ("", ValueError),
    ("   ", ValueError)
])
def test_validacion_ruta_archivo(
    clase_parser,
    ruta,
    excepcion
):
    with pytest.raises(excepcion):
        clase_parser(ruta)