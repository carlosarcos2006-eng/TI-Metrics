import math
from ipaddress import ip_address


def validar_ip(ip: str) -> None:
    """Valida una dirección IPv4 o IPv6."""

    if not isinstance(ip, str):
        raise TypeError(
            "La dirección IP debe ser una cadena de texto."
        )

    try:
        ip_address(ip)

    except ValueError as error:
        raise ValueError(
            f"Dirección IP inválida: {ip!r}"
        ) from error


def _validar_lista(elementos, nombre):
    if not isinstance(elementos, list):
        raise TypeError(
            f"{nombre} debe proporcionarse como una lista."
        )


def _validar_registro(registro, contexto):
    if not isinstance(registro, dict):
        raise ValueError(
            f"Datos inválidos en {contexto}: "
            "se esperaba un diccionario."
        )


def _validar_campos(registro, campos, contexto):
    for campo in campos:
        if campo not in registro:
            raise ValueError(
                f"Datos inválidos en {contexto}: "
                f"falta el campo obligatorio '{campo}'."
            )

        valor = registro[campo]

        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                f"Datos inválidos en {contexto}: "
                f"el campo '{campo}' debe ser "
                "una cadena de texto no vacía."
            )

        if campo == "ip":
            try:
                validar_ip(valor)

            except ValueError as error:
                raise ValueError(
                    f"Datos inválidos en {contexto}: "
                    f"dirección IP inválida: {valor!r}."
                ) from error


def _convertir_inmutable(valor):
    """Convierte datos JSON en estructuras hashables."""

    if isinstance(valor, dict):
        elementos = []

        for clave, contenido in valor.items():
            if not isinstance(clave, str):
                raise ValueError(
                    "Las claves de un diccionario JSON "
                    "deben ser cadenas de texto."
                )

            elementos.append(
                (clave, _convertir_inmutable(contenido))
            )

        return frozenset(elementos)

    if isinstance(valor, list):
        return tuple(
            _convertir_inmutable(elemento)
            for elemento in valor
        )

    if isinstance(valor, float):
        if not math.isfinite(valor):
            raise ValueError(
                "Los valores numéricos deben ser finitos."
            )

        return valor

    if valor is None or isinstance(valor, (str, int, bool)):
        return valor

    raise TypeError(
        f"Tipo de dato incompatible con JSON: "
        f"{type(valor).__name__}."
    )


def obtener_ips_unicas(registros):
    _validar_lista(registros, "Los registros")

    ips = set()

    for numero, registro in enumerate(registros, start=1):
        contexto = f"el registro {numero}"

        _validar_registro(registro, contexto)
        _validar_campos(registro, ("ip",), contexto)

        ips.add(registro["ip"])

    return ips


def crear_resumen_evento(evento):
    if not isinstance(evento, dict):
        raise TypeError(
            "El evento debe ser un diccionario."
        )

    _validar_campos(
        evento,
        ("ip", "event", "severity"),
        "el evento"
    )

    return (
        evento["ip"],
        evento["event"],
        evento["severity"]
    )


def obtener_ips_criticas(eventos):
    _validar_lista(eventos, "Los eventos")

    ips_criticas = set()

    for numero, evento in enumerate(eventos, start=1):
        contexto = f"el evento {numero}"

        _validar_registro(evento, contexto)

        _validar_campos(
            evento,
            ("ip", "severity"),
            contexto
        )

        if evento["severity"] == "CRITICAL":
            ips_criticas.add(evento["ip"])

    return ips_criticas


def deduplicar_eventos(eventos):
    _validar_lista(eventos, "Los eventos")

    eventos_unicos = []
    eventos_vistos = set()

    for numero, evento in enumerate(eventos, start=1):
        contexto = f"el evento {numero}"

        _validar_registro(evento, contexto)

        try:
            identificador = _convertir_inmutable(evento)

        except (TypeError, ValueError, RecursionError) as error:
            raise ValueError(
                f"Datos inválidos en {contexto}: "
                "el contenido no es compatible con JSON."
            ) from error

        if identificador not in eventos_vistos:
            eventos_vistos.add(identificador)
            eventos_unicos.append(evento)

    return eventos_unicos