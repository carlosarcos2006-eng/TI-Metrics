from parsers.json_parser import leer_eventos_json
from utils.data_utils import (
    obtener_ips_unicas,
    crear_resumen_evento,
    obtener_ips_criticas
)


ruta = "data/events.json"

eventos = leer_eventos_json(ruta)

ips_unicas = obtener_ips_unicas(eventos)

resumen = crear_resumen_evento(eventos[0])

ips_criticas = obtener_ips_criticas(eventos)


print("Cantidad de eventos:", len(eventos))
print("IPs únicas:", ips_unicas)
print("Cantidad de IPs únicas:", len(ips_unicas))
print("Resumen del primer evento:", resumen)
print("Tipo del resumen:", type(resumen))
print("IPs con eventos críticos:", ips_criticas)
print("Cantidad de IPs críticas:", len(ips_criticas))