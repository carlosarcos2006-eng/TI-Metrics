
# TI-Metrics

Engine de Analítica de Logs y Monitoreo de Infraestructura.

## Descripción

TI-Metrics es una aplicación de consola desarrollada en Python 3
que procesa registros de infraestructura TI en formatos CSV y JSON,
calcula métricas HTTP, identifica direcciones IP críticas y consulta
una API REST pública para obtener información geográfica.

El proyecto utiliza una arquitectura orientada a objetos basada en
abstracción, herencia, polimorfismo y encapsulamiento.

## Hito 1: Ingesta de Datos, Persistencia y API REST

**Estado:** Desarrollo funcional completado.

### Funcionalidades implementadas

- Lectura de registros desde archivos CSV y JSON.
- Procesamiento de datos mediante listas, diccionarios, tuplas y conjuntos.
- Deduplicación de eventos mediante conjuntos (`set`).
- Cálculo del porcentaje de errores HTTP 500.
- Identificación de direcciones IP críticas.
- Consumo de una API REST mediante `requests`.
- Manejo de excepciones en lectura de archivos y peticiones HTTP.
- Generación de un reporte resumido en formato JSON.

## Hito 2: Refactorización a Programación Orientada a Objetos y UML

**Estado:** Implementación y pruebas funcionales completadas.

### Arquitectura orientada a objetos

Se refactorizaron los componentes principales del sistema
utilizando clases y principios de Programación Orientada a Objetos.

### Clases implementadas

- `BaseLogParser`: clase abstracta que define el método `leer()`
  y establece un contrato común para los analizadores.

- `CSVLogParser`: hereda de `BaseLogParser` e implementa la
  lectura de registros CSV.

- `JSONLogParser`: hereda de `BaseLogParser` e implementa la
  lectura de eventos JSON.

- `MetricsService`: encapsula los registros y calcula el
  porcentaje de errores HTTP 500.

- `GeolocationService`: consulta una API REST para obtener
  información geográfica de direcciones IP.

- `ReportService`: construye el resumen de métricas y
  genera el reporte JSON.

### Principios de POO aplicados

- **Abstracción:** uso de `BaseLogParser` como clase abstracta.
- **Herencia:** `CSVLogParser` y `JSONLogParser` heredan
  de `BaseLogParser`.
- **Polimorfismo:** implementación del método `leer()`
  según el formato de archivo.
- **Encapsulamiento:** uso de atributos protegidos y
  propiedades `@property`.
- **Composición de objetos:** integración de instancias de
  analizadores y servicios en el flujo principal.

### Diagrama UML

El diagrama de clases fue elaborado utilizando Mermaid
y se encuentra disponible en:

[Diagrama UML de clases](docs/diagrama_clases.md)

## Tecnologías

- Python 3
- Requests
- Pytest
- pytest-cov
- Git y GitHub
- Mermaid

## Estructura del proyecto

- `data/`: archivos CSV, JSON y reportes generados.
- `docs/`: documentación y diagrama UML de clases.
- `src/main.py`: punto de entrada de la aplicación.
- `src/models/`: clases base y abstracciones.
- `src/parsers/`: analizadores de archivos CSV y JSON.
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

Ejecutar desde la raíz del proyecto:

```bash
python -m src.main
```

## Resultado de referencia

```text
TI-Metrics iniciado correctamente
Porcentaje HTTP 500: 30.0 %
Cantidad de IP críticas: 2
Reporte generado en: data/report.json
```

El reporte generado se almacena en `data/report.json`.

## Pruebas automatizadas

Para ejecutar la suite completa:

```bash
python -m pytest src/ -v
```

### Última verificación del Hito 2

- 66 pruebas aprobadas.
- 0 pruebas fallidas.
- Integración orientada a objetos verificada.

Para obtener un reporte de cobertura:

```bash
python -m pytest src/ -v --cov=src --cov-report=term-missing
```

### Referencia histórica del Hito 1

- 31 pruebas aprobadas.
- 0 pruebas fallidas.
- 99 % de cobertura global.

La cobertura del Hito 2 debe comprobarse mediante
una nueva ejecución con pytest-cov.

## Próximas etapas

- Revisión final de la documentación y entregables del Hito 2.
- Hito 3: Consolidación de calidad, auditoría y defensa oral.
