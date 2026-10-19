
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


def test_leer_csv_archivo_inexistente(tmp_path):
    import pytest

    ruta = tmp_path / "archivo_inexistente.csv"

    with pytest.raises(FileNotFoundError, match="No se encontró"):
        leer_logs_csv(ruta)


def test_leer_csv_status_invalido(tmp_path):
    import pytest

    ruta = tmp_path / "logs_invalidos.csv"

    ruta.write_text(
        "ip,status,response_time\n"
        "192.168.1.10,ERROR,120\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="fila 2"):
        leer_logs_csv(ruta)


def test_leer_csv_response_time_invalido(tmp_path):
    import pytest

    ruta = tmp_path / "logs_invalidos.csv"

    ruta.write_text(
        "ip,status,response_time\n"
        "192.168.1.10,500,INVALIDO\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="fila 2"):
        leer_logs_csv(ruta)
