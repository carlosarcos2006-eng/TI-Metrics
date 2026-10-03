from services.geolocation_service import (
    enriquecer_ips_con_geolocalizacion
)


ips_criticas = {
    "192.168.1.10",
    "203.0.113.25"
}


resultados = enriquecer_ips_con_geolocalizacion(ips_criticas)


print("Geolocalización de las IP críticas:")

for ip, datos in resultados.items():
    print(ip, "->", datos)