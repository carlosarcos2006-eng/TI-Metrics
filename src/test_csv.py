import pytest

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

def test_leer_csv_sin_permisos():
    import pytest
    from unittest.mock import patch

    ruta = "data/logs.csv"

    with patch("builtins.open", side_effect=PermissionError):
        with pytest.raises(
            PermissionError,
            match="No tienes permisos para leer el archivo CSV"
        ):
            leer_logs_csv(ruta)

@pytest.mark.parametrize("encabezados", [
    "status,response_time",
    "ip,response_time",
    "ip,status",
])
def test_leer_csv_encabezados_incompletos(tmp_path, encabezados):
    ruta = tmp_path / "encabezados_incompletos.csv"

    ruta.write_text(
        encabezados + "\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="encabezados"):
        leer_logs_csv(ruta)

def test_leer_csv_archivo_vacio(tmp_path):
    ruta = tmp_path / "archivo_vacio.csv"

    ruta.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="encabezados"):
        leer_logs_csv(ruta)

def test_leer_csv_sin_registros(tmp_path):
    ruta = tmp_path / "sin_registros.csv"

    ruta.write_text(
        "ip,status,response_time\n",
        encoding="utf-8"
    )

    assert leer_logs_csv(ruta) == []

@pytest.mark.parametrize("status", [-200, 99, 600])
def test_leer_csv_status_fuera_de_rango(tmp_path, status):
    ruta = tmp_path / "status_invalido.csv"

    ruta.write_text(
        "ip,status,response_time\n"
        f"192.168.1.10,{status},120\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="fila 2"):
        leer_logs_csv(ruta)

def test_leer_csv_response_time_negativo(tmp_path):
    ruta = tmp_path / "tiempo_negativo.csv"

    ruta.write_text(
        "ip,status,response_time\n"
        "192.168.1.10,200,-120\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="fila 2"):
        leer_logs_csv(ruta)

def test_leer_csv_response_time_cero(tmp_path):
    ruta = tmp_path / "tiempo_cero.csv"

    ruta.write_text(
        "ip,status,response_time\n"
        "192.168.1.10,200,0\n",
        encoding="utf-8"
    )

    registros = leer_logs_csv(ruta)

    assert registros[0]["response_time"] == 0

@pytest.mark.parametrize("ip", ["", "   "])
def test_leer_csv_ip_vacia(tmp_path, ip):
    ruta = tmp_path / "ip_vacia.csv"

    ruta.write_text(
        "ip,status,response_time\n"
        f"{ip},200,120\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="fila 2"):
        leer_logs_csv(ruta)

@pytest.mark.parametrize("ruta", [123, None, True])
def test_leer_csv_ruta_tipo_incorrecto(ruta):
    with pytest.raises(TypeError):
        leer_logs_csv(ruta)

@pytest.mark.parametrize("status", [100, 599])
def test_leer_csv_status_limites_validos(tmp_path, status):
    ruta = tmp_path / "status_limite.csv"

    ruta.write_text(
        "ip,status,response_time\n"
        f"192.168.1.10,{status},120\n",
        encoding="utf-8"
    )

    registros = leer_logs_csv(ruta)

    assert registros[0]["status"] == status

@pytest.mark.parametrize("contenido", [
    "ip,response_time,status\n"
    "192.168.1.10,120\n",

    "ip,status,response_time\n"
    "192.168.1.10,200\n",

    "status,response_time,ip\n"
    "200,120\n",
])
def test_leer_csv_campos_faltantes(tmp_path, contenido):
    ruta = tmp_path / "campos_faltantes.csv"

    ruta.write_text(
        contenido,
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="fila 2"):
        leer_logs_csv(ruta)