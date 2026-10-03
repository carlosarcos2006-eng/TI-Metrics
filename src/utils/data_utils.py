def obtener_ips_unicas(registros):
    ips = set()

    for registro in registros:
        ips.add(registro["ip"])

    return ips


def crear_resumen_evento(evento):
    return (
        evento["ip"],
        evento["event"],
        evento["severity"]
    )

def obtener_ips_criticas(eventos):
    ips_criticas = set()

    for evento in eventos:
        if evento["severity"] == "CRITICAL":
            ips_criticas.add(evento["ip"])

    return ips_criticas