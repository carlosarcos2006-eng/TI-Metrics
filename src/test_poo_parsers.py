import pytest

from src.models.base_log_parser import BaseLogParser

from src.parsers.csv_parser import CSVLogParser

from src.parsers.json_parser import JSONLogParser

def test_base_log_parser_no_se_puede_instanciar():
    with pytest.raises(TypeError):
        BaseLogParser("data/logs.csv")

def test_parsers_heredan_de_base_log_parser():
    assert issubclass(CSVLogParser, BaseLogParser)
    assert issubclass(JSONLogParser, BaseLogParser)

def test_polimorfismo_parsers():
    parsers = [CSVLogParser("data/logs.csv"), JSONLogParser("data/events.json")]
    resultados = []

    for parser in parsers:
        datos = parser.leer()
        resultados.append(datos)

    assert len(resultados[0]) == 10
    assert len(resultados[1]) == 6

def test_encapsulamiento_ruta_archivo():
    parser = CSVLogParser("data/logs.csv")
    assert parser.ruta_archivo == "data/logs.csv"
    with pytest.raises(AttributeError):
        parser.ruta_archivo = "data/otro_archivo.csv"
    assert parser.ruta_archivo == "data/logs.csv"

def test_validacion_ruta_archivo():
    with pytest.raises(TypeError):
        CSVLogParser(123)
    with pytest.raises(ValueError):
        CSVLogParser("")
    with pytest.raises(ValueError):
        JSONLogParser("  ")