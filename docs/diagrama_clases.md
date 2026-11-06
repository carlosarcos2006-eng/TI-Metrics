
# Diagrama UML de Clases — TI-Metrics

## Hito 2: Arquitectura Orientada a Objetos

Este diagrama representa las clases principales del sistema TI-Metrics,
sus atributos, métodos y relaciones de herencia.


```mermaid
classDiagram
    direction TB

    class BaseLogParser {
        <<abstract>>
        #_ruta_archivo : str
        +ruta_archivo : str
        +leer()*
    }

    class CSVLogParser {
        +leer()
    }

    class JSONLogParser {
        +leer()
    }

    class MetricsService {
        #_registros : list
        +registros : list
        +calcular_porcentaje_http_500() float
    }

    class GeolocationService {
        #_url_base : str
        #_timeout : int_or_float
        +url_base : str
        +timeout : int_or_float
        +obtener_geolocalizacion(ip)
        +enriquecer_ips_con_geolocalizacion(ips)
    }

    class ReportService {
        #_indentacion : int
        +indentacion : int
        +construir_resumen(porcentaje_500, ips_criticas, geolocalizaciones) dict
        +guardar_reporte_json(resumen, ruta_archivo) None
    }

    BaseLogParser <|-- CSVLogParser
    BaseLogParser <|-- JSONLogParser
```

## Conceptos de Programación Orientada a Objetos

### Abstracción
BaseLogParser define el contrato común de lectura mediante
el método abstracto leer().

### Herencia
CSVLogParser y JSONLogParser heredan de BaseLogParser.

### Polimorfismo
Ambas clases implementan leer(), pero procesan formatos
de archivo diferentes: CSV y JSON.

### Encapsulamiento
Las clases utilizan atributos protegidos y propiedades
@property para controlar el acceso a su estado interno.

### Integración
El módulo src/main.py coordina los analizadores y servicios
para procesar registros, calcular métricas, geolocalizar
direcciones IP críticas y generar el reporte JSON.
