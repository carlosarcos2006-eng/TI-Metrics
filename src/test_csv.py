from parsers.csv_parser import leer_logs_csv
from services.metrics_service import calcular_porcentaje_http_500


ruta = "data/logs.csv"

registros = leer_logs_csv(ruta)

print("Cantidad de registros:", len(registros))

porcentaje_500 = calcular_porcentaje_http_500(registros)

print("Porcentaje de HTTP 500:", porcentaje_500, "%")