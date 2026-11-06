
from src.parsers.csv_parser import CSVLogParser
from src.parsers.json_parser import JSONLogParser
from src.services.metrics_service import MetricsService
from src.services.geolocation_service import GeolocationService
from src.services.report_service import ReportService
from src.utils.data_utils import obtener_ips_criticas, deduplicar_eventos



def main():
    print("TI-Metrics iniciado correctamente")

    ruta_csv = "data/logs.csv"
    ruta_json = "data/events.json"
    ruta_reporte = "data/report.json"

    parser_csv = CSVLogParser(ruta_csv)
    parser_json = JSONLogParser(ruta_json)

    registros = parser_csv.leer()
    eventos = parser_json.leer()

    eventos = deduplicar_eventos(eventos)

    servicio_metricas = MetricsService(registros)
    porcentaje_500 = servicio_metricas.calcular_porcentaje_http_500()

    ips_criticas = obtener_ips_criticas(eventos)

    servicio_geolocalizacion = GeolocationService()
    geolocalizaciones = (
        servicio_geolocalizacion.enriquecer_ips_con_geolocalizacion(
            ips_criticas
        )
    )

    servicio_reportes = ReportService()

    resumen = servicio_reportes.construir_resumen(
        porcentaje_500,
        ips_criticas,
        geolocalizaciones,
    )

    servicio_reportes.guardar_reporte_json(
        resumen,
        ruta_reporte,
    )

    print("Porcentaje HTTP 500:", porcentaje_500, "%")
    print("Cantidad de IP críticas:", len(ips_criticas))
    print("Reporte generado en:", ruta_reporte)

if __name__ == "__main__":
    main()