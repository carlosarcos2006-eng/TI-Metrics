
from parsers.csv_parser import leer_logs_csv
from services.metrics_service import calcular_porcentaje_http_500


def test_calcular_porcentaje_http_500():
    registros = [
        {"status": 200},
        {"status": 500},
        {"status": 404},
        {"status": 500},
    ]

    resultado = calcular_porcentaje_http_500(registros)

    assert resultado == 50.0


def test_calcular_porcentaje_http_500_sin_registros():
    registros = []

    resultado = calcular_porcentaje_http_500(registros)

    assert resultado == 0.0


def test_leer_logs_csv():
    ruta = "data/logs.csv"

    registros = leer_logs_csv(ruta)

    assert len(registros) == 10
    assert all(isinstance(registro["status"], int) for registro in registros)
