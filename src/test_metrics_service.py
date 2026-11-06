
import pytest

from services.metrics_service import MetricsService


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


def test_metrics_service_valida_tipo():
    """Comprueba que el constructor rechaza tipos inválidos."""
    with pytest.raises(TypeError):
        MetricsService("registros_invalidos")


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