def calcular_porcentaje_http_500(registros):
    total_registros = len(registros)

    if total_registros == 0:
        return 0.0

    errores_500 = 0

    for registro in registros:
        if registro["status"] == 500:
            errores_500 += 1

    porcentaje = (errores_500 / total_registros) * 100

    return porcentaje