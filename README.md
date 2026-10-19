
# TI-Metrics

Engine de Analítica de Logs y Monitoreo de Infraestructura.

## Descripción

TI-Metrics es una aplicación de consola desarrollada en Python 3
que procesa registros de infraestructura TI en formatos CSV y JSON,
calcula métricas HTTP, identifica direcciones IP críticas y consulta
una API REST pública para obtener información geográfica.

## Hito 1: Ingesta de Datos, Persistencia y API REST

Estado: Desarrollo funcional completado.

### Funcionalidades implementadas

- Lectura de registros desde archivos CSV y JSON.
- Procesamiento de datos mediante listas, diccionarios, tuplas y conjuntos.
- Deduplicación de eventos mediante conjuntos (`set`).
- Cálculo del porcentaje de errores HTTP 500.
- Identificación de direcciones IP críticas.
- Consumo de una API REST mediante `requests`.
- Manejo de excepciones en lectura de archivos y peticiones HTTP.
- Generación de un reporte resumido en formato JSON.

## Tecnologías

- Python 3
- Requests
- Pytest
- pytest-cov
- Git y GitHub

## Estructura del proyecto

- `data/`: archivos CSV, JSON y reportes generados.
- `src/main.py`: punto de entrada de la aplicación.
- `src/parsers/`: lectura de archivos CSV y JSON.
- `src/services/`: métricas, geolocalización y reportes.
- `src/utils/`: funciones auxiliares y deduplicación.
- `src/test_*.py`: pruebas automatizadas.
- `PROMPTS.md`: registro de asistencia de inteligencia artificial.
- `requirements.txt`: dependencias del proyecto.

## Instalación

Desde la carpeta raíz del proyecto:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

```bash
python src/main.py
```

## Resultado de referencia

```text
TI-Metrics iniciado correctamente
Porcentaje HTTP 500: 30.0 %
Cantidad de IP críticas: 2
Reporte generado en: data/report.json
```

## Pruebas automatizadas

```bash
python -m pytest src/ -v --cov=src --cov-report=term-missing
```

Última verificación del Hito 1:

- 31 pruebas aprobadas.
- 0 pruebas fallidas.
- 99 % de cobertura global.

## Próximas etapas

- Hito 2: Refactorización a Programación Orientada a Objetos y UML.
- Hito 3: Consolidación de calidad, auditoría y defensa oral.