import pytest

from src.services.metrics_service import (
    MetricsService,
    calcular_porcentaje_http_500,
)

def test_metrics_service_calcula_porcentaje():
    """Comprueba el cálculo mediante el método de la clase."""
    registros = [
        {"status": 200},
        {"status": 500},
        {"status": 404},
        {"status": 500},
    ]

    servicio = MetricsService(registros)

    assert servicio.calcular_porcentaje_http_500() == 50.0

def test_metrics_service_sin_registros():
    """Comprueba el comportamiento con una lista vacía."""
    servicio = MetricsService([])

    assert servicio.calcular_porcentaje_http_500() == 0.0

@pytest.mark.parametrize("registros", [
    "registros_invalidos",
    None,
    123,
    True,
    {},
    (),
])
def test_metrics_service_valida_tipo(registros):
    """Comprueba que el constructor rechaza tipos inválidos."""
    with pytest.raises(
        TypeError,
        match="Los registros deben proporcionarse como una lista"
    ):
        MetricsService(registros)

def test_metrics_service_propiedad_solo_lectura():
    """Comprueba que no se puede reasignar la propiedad."""
    servicio = MetricsService([{"status": 500}])

    assert servicio.registros == [{"status": 500}]

    with pytest.raises(AttributeError):
        servicio.registros = []

def test_metrics_service_protege_lista_original():
    """Comprueba que se conserva una copia de la lista recibida."""
    registros = [{"status": 500}]
    servicio = MetricsService(registros)

    registros.append({"status": 200})

    assert servicio.calcular_porcentaje_http_500() == 100.0

def test_metrics_service_protege_lista_devuelta():
    """Comprueba que modificar la lista consultada no altera la interna."""
    servicio = MetricsService([{"status": 500}])

    registros_obtenidos = servicio.registros
    registros_obtenidos.append({"status": 200})

    assert servicio.calcular_porcentaje_http_500() == 100.0

def test_metrics_service_protege_diccionarios_originales():
    """Comprueba la independencia de los diccionarios recibidos."""
    registros = [{"status": 500}]
    servicio = MetricsService(registros)

    registros[0]["status"] = 200

    assert servicio.registros == [{"status": 500}]
    assert servicio.calcular_porcentaje_http_500() == 100.0

def test_metrics_service_protege_diccionarios_devueltos():
    """Comprueba la independencia de los diccionarios consultados."""
    servicio = MetricsService([{"status": 500}])

    registros_obtenidos = servicio.registros
    registros_obtenidos[0]["status"] = 200

    assert servicio.registros == [{"status": 500}]
    assert servicio.calcular_porcentaje_http_500() == 100.0

@pytest.mark.parametrize("registro", [
    123,
    "registro",
    None,
    True,
    [],
])
def test_metrics_service_registro_tipo_incorrecto(registro):
    with pytest.raises(ValueError, match="registro 1: el registro debe ser un diccionario"):
        MetricsService([registro])

def test_metrics_service_status_faltante():
    registros = [
        {"ip": "8.8.8.8"}
    ]

    with pytest.raises(ValueError, match="registro 1: falta el campo obligatorio 'status'"):
        MetricsService(registros)

@pytest.mark.parametrize("status", [
    "500",
    500.0,
    True,
    False,
    None,
    [],
    {},
])
def test_metrics_service_status_tipo_incorrecto(status):
    registros = [
        {"status": status}
    ]

    with pytest.raises(ValueError, match="registro 1: el estado HTTP debe ser un número entero"):
        MetricsService(registros)

@pytest.mark.parametrize("status", [
    -1,
    0,
    99,
    600,
    999,
])
def test_metrics_service_status_fuera_de_rango(status):
    registros = [
        {"status": status}
    ]

    with pytest.raises(ValueError, match="registro 1: el estado HTTP debe estar entre 100 y 599"):
        MetricsService(registros)

@pytest.mark.parametrize("status", [
    100,
    599,
])
def test_metrics_service_status_limites_validos(status):
    servicio = MetricsService([
        {"status": status}
    ])

    assert servicio.calcular_porcentaje_http_500() == 0.0

def test_metrics_service_todos_errores_500():
    registros = [
        {"status": 500},
        {"status": 500},
        {"status": 500},
    ]

    servicio = MetricsService(registros)

    assert servicio.calcular_porcentaje_http_500() == 100.0

def test_metrics_service_sin_errores_500():
    registros = [
        {"status": 200},
        {"status": 404},
        {"status": 503},
    ]

    servicio = MetricsService(registros)

    assert servicio.calcular_porcentaje_http_500() == 0.0

def test_metrics_service_campos_adicionales():
    registros = [
        {
            "ip": "8.8.8.8",
            "status": 500,
            "response_time": 150
        },
        {
            "ip": "1.1.1.1",
            "status": 200,
            "response_time": 80
        }
    ]

    servicio = MetricsService(registros)

    assert servicio.registros == registros
    assert servicio.calcular_porcentaje_http_500() == 50.0

def test_metrics_service_segundo_registro_invalido():
    registros = [
        {"status": 200},
        {"status": "500"}
    ]
    with pytest.raises(ValueError, match="registro 2: el estado HTTP debe ser un número entero"):
        MetricsService(registros)

def test_metrics_service_wrapper_datos_validos():

    registros = [
        {"status": 500},
        {"status": 200},
        {"status": 500},
        {"status": 404}
    ]

    assert calcular_porcentaje_http_500(registros) == 50.0

def test_metrics_service_wrapper_datos_invalidos():

    registros = [
        {"status": 200},
        {"status": "500"}
    ]

    with pytest.raises(ValueError, match="registro 2: el estado HTTP debe ser un número entero"):
        calcular_porcentaje_http_500(registros)


@pytest.mark.parametrize("registros, esperado", [
    (
        [{"status": 500}, {"status": 200}, {"status": 404}],
        33.33333333333333
    ),
    (
        [{"status": 500}, {"status": 500}, {"status": 200}],
        66.66666666666666
    ),
])
def test_metrics_service_porcentaje_decimal(registros, esperado):
    """Comprueba porcentajes con decimales periódicos."""
    servicio = MetricsService(registros)

    assert servicio.calcular_porcentaje_http_500() == pytest.approx(
        esperado
    )


def test_metrics_service_protege_datos_anidados_originales():
    """Comprueba la independencia de estructuras anidadas recibidas."""
    registros = [
        {
            "status": 500,
            "metadata": {
                "etiquetas": ["critico"]
            }
        }
    ]

    servicio = MetricsService(registros)

    registros[0]["metadata"]["etiquetas"].append("modificado")

    assert servicio.registros == [
        {
            "status": 500,
            "metadata": {
                "etiquetas": ["critico"]
            }
        }
    ]

    assert servicio.calcular_porcentaje_http_500() == 100.0


def test_metrics_service_protege_datos_anidados_devueltos():
    """Comprueba la independencia de estructuras anidadas consultadas."""
    servicio = MetricsService([
        {
            "status": 500,
            "metadata": {
                "etiquetas": ["critico"]
            }
        }
    ])

    registros_obtenidos = servicio.registros

    registros_obtenidos[0]["metadata"]["etiquetas"].append(
        "modificado"
    )

    assert servicio.registros == [
        {
            "status": 500,
            "metadata": {
                "etiquetas": ["critico"]
            }
        }
    ]

    assert servicio.calcular_porcentaje_http_500() == 100.0
