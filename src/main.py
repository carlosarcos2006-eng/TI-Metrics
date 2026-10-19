
from parsers.csv_parser import leer_logs_csv
from parsers.json_parser import leer_eventos_json
from services.metrics_service import calcular_porcentaje_http_500
from services.geolocation_service import enriquecer_ips_con_geolocalizacion
from services.report_service import (
    construir_resumen,
    guardar_reporte_json,
)
from utils.data_utils import obtener_ips_criticas


def main():
    print("TI-Metrics iniciado correctamente")

    ruta_csv = "data/logs.csv"
    ruta_json = "data/events.json"
    ruta_reporte = "data/report.json"

    registros = leer_logs_csv(ruta_csv)
    eventos = leer_eventos_json(ruta_json)

    porcentaje_500 = calcular_porcentaje_http_500(registros)
    ips_criticas = obtener_ips_criticas(eventos)

    geolocalizaciones = enriquecer_ips_con_geolocalizacion(
        ips_criticas
    )

    resumen = construir_resumen(
        porcentaje_500,
        ips_criticas,
        geolocalizaciones,
    )

    guardar_reporte_json(resumen, ruta_reporte)

    print("Porcentaje HTTP 500:", porcentaje_500, "%")
    print("Cantidad de IP críticas:", len(ips_criticas))
    print("Reporte generado en:", ruta_reporte)


if __name__ == "__main__":
    main()
