# Matriz de Cumplimiento del Hito 2 — TI-Metrics

## 1. Identificación de la auditoría

- Proyecto: TI-Metrics.
- Hito: Refactorización a Arquitectura Orientada a Objetos y UML.
- Badge asociado al hito: OOP Architect.
- Fecha planificada: 2026-11-15.
- Fecha de validación: 2026-11-24.
- Rama de desarrollo: `feat/hito2-poo`.
- Versión de referencia del Hito 1: `7ada799`.
- Versión auditada del Hito 2: `7b9832e`.

La presente matriz constituye una evaluación técnica interna.
Los identificadores y criterios utilizados no corresponden a
una rúbrica oficial de calificación del docente.

## 2. Objetivo

Verificar el cumplimiento de los requerimientos del Hito 2,
la correspondencia entre la arquitectura y su documentación,
y la conservación de las funcionalidades principales del Hito 1.

## 3. Requerimientos oficiales del Hito 2

| ID | Requerimiento | Evaluación |
|---|---|---|
| REQ-01 | Refactorización del código procedural hacia POO | Cumple con observaciones |
| REQ-02 | Jerarquía de clases con herencia y polimorfismo | Cumple |
| REQ-03 | Encapsulamiento mediante atributos internos y @property | Cumple |
| REQ-04 | Diagrama de clases UML mediante Mermaid o PlantUML en docs/ | Cumple |

## 4. Matriz detallada de cumplimiento

| ID | Criterio técnico | Evidencia | Estado |
|---|---|---|---|
| REQ-01.01 | Refactorización CSV | CSVLogParser | Cumple |
| REQ-01.02 | Refactorización JSON | JSONLogParser | Cumple |
| REQ-01.03 | Refactorización de métricas | MetricsService | Cumple |
| REQ-01.04 | Refactorización de geolocalización | GeolocationService | Cumple |
| REQ-01.05 | Refactorización de reportes | ReportService | Cumple |
| REQ-01.06 | Integración POO en main | src/main.py | Cumple |
| REQ-01.07 | Conservación funcional del Hito 1 | 15 comparaciones diferenciales | Cumple con observaciones |
| REQ-02.01 | Existencia de una clase base abstracta | BaseLogParser y ABC | Cumple |
| REQ-02.02 | Herencia del parser CSV | CSVLogParser(BaseLogParser) | Cumple |
| REQ-02.03 | Herencia del parser JSON | JSONLogParser(BaseLogParser) | Cumple |
| REQ-02.04 | Sobrescritura del método leer | Implementaciones CSV y JSON | Cumple |
| REQ-02.05 | Demostración de polimorfismo | src/test_poo_parsers.py | Cumple |
| REQ-03.01 | Atributos internos no públicos | Cinco atributos con prefijo _ | Cumple |
| REQ-03.02 | Uso de decoradores @property | Cinco propiedades | Cumple |
| REQ-03.03 | Control de acceso y modificación | Propiedades de solo lectura y copias profundas | Cumple |
| REQ-03.04 | Validación de invariantes | Constructores, métodos y pruebas | Cumple |
| REQ-04.01 | Existencia del diagrama UML | docs/diagrama_clases.md | Cumple |
| REQ-04.02 | Utilización de Mermaid | Diagramas Mermaid | Cumple |
| REQ-04.03 | Ubicación dentro de docs/ | docs/diagrama_clases.md | Cumple |
| REQ-04.04 | Correspondencia con la implementación | Auditoría arquitectónica de la Parte 5 | Cumple |

### 4.1. Resumen de evaluación

| Estado | Cantidad | Porcentaje |
|---|---:|---:|
| Cumple | 19 | 95 % |
| Cumple con observaciones | 1 | 5 % |
| Cumple parcialmente | 0 | 0 % |
| No cumple | 0 | 0 % |
| Pendiente de verificación | 0 | 0 % |
| Total | 20 | 100 % |

Los cuatro requerimientos oficiales presentan evidencias
técnicas favorables. Esta evaluación no garantiza una
calificación académica determinada.

## 5. Inventario arquitectónico

| Elemento | Cantidad |
|---|---:|
| Clases principales | 6 |
| Clases abstractas | 1 |
| Clases concretas | 5 |
| Relaciones de herencia | 2 |
| Constructores explícitos | 4 |
| Atributos internos | 5 |
| Propiedades de solo lectura | 5 |
| Métodos ordinarios, incluido el abstracto | 8 |
| Métodos abstractos | 1 |
| Métodos estáticos | 2 |
| Funciones de compatibilidad | 7 |
| Funciones originales conservadas | 12 |
| Nuevas funciones auxiliares | 5 |
| Funciones al nivel del módulo | 17 |
| Declaraciones def totales | 36 |
| Dependencias arquitectónicas internas documentadas | 8 |
| Diagramas Mermaid | 3 |

### 5.1. Clases principales

| Clase | Responsabilidad |
|---|---|
| BaseLogParser | Definir el contrato común de lectura |
| CSVLogParser | Leer y validar registros CSV |
| JSONLogParser | Leer y validar eventos JSON |
| MetricsService | Calcular métricas HTTP |
| GeolocationService | Consultar y enriquecer direcciones IP |
| ReportService | Construir y persistir reportes JSON |

La arquitectura conserva funciones auxiliares sin estado
propio y una función main como punto de coordinación.

No se incorporan relaciones artificiales de composición
o agregación, puesto que no son necesarias para el diseño
actual ni constituyen una exigencia explícita del hito.

## 6. Trazabilidad funcional del Hito 1

Las funcionalidades se identificaron mediante el README
histórico y la inspección de los siete módulos originales.

| ID | Funcionalidad original | Implementación actual |
|---|---|---|
| RF-01 | Lectura CSV y JSON | CSVLogParser y JSONLogParser |
| RF-02 | Procesamiento con listas, diccionarios, tuplas y conjuntos | Parsers, servicios y data_utils |
| RF-03 | Deduplicación mediante conjuntos | deduplicar_eventos |
| RF-04 | Porcentaje HTTP 500 | MetricsService |
| RF-05 | Identificación de IP críticas | obtener_ips_criticas |
| RF-06 | Consumo de API REST mediante requests | GeolocationService |
| RF-07 | Manejo de excepciones | Parsers, servicios y main |
| RF-08 | Generación de reportes JSON | ReportService |

Resultado: ocho de ocho funcionalidades originales
con implementación y evidencias de pruebas identificadas.

## 7. Compatibilidad de las funciones originales

| ID | Función original | Parámetros conservados |
|---|---|---|
| FUN-01 | main | Sin parámetros |
| FUN-02 | leer_logs_csv | ruta_archivo |
| FUN-03 | leer_eventos_json | ruta_archivo |
| FUN-04 | obtener_geolocalizacion | ip |
| FUN-05 | enriquecer_ips_con_geolocalizacion | ips |
| FUN-06 | calcular_porcentaje_http_500 | registros |
| FUN-07 | construir_resumen | porcentaje_500, ips_criticas, geolocalizaciones |
| FUN-08 | guardar_reporte_json | resumen, ruta_archivo |
| FUN-09 | obtener_ips_unicas | registros |
| FUN-10 | crear_resumen_evento | evento |
| FUN-11 | obtener_ips_criticas | eventos |
| FUN-12 | deduplicar_eventos | eventos |

Mediante el módulo ast de Python se compararon las
declaraciones originales y actuales de los parámetros.

- Funciones originales: 12.
- Funciones conservadas: 12.
- Declaraciones de parámetros conservadas: 12.
- Declaraciones de parámetros modificadas: 0.
- Funciones eliminadas: 0.

Esta comprobación no incluye las anotaciones de retorno
ni garantiza compatibilidad de las rutas de importación.

## 8. Pruebas diferenciales

Se recuperó el código histórico del Hito 1 desde Git
y se comparó con la implementación actual.

| ID | Comprobación | Resultado |
|---|---|---|
| DIF-01 | Lectura CSV | Coincide |
| DIF-02 | Lectura JSON | Coincide |
| DIF-03 | Porcentaje HTTP 500 | Coincide |
| DIF-04 | Métricas con lista vacía | Coincide |
| DIF-05 | IP únicas CSV | Coincide |
| DIF-06 | IP únicas JSON | Coincide |
| DIF-07 | Resumen de evento | Coincide |
| DIF-08 | IP críticas | Coincide |
| DIF-09 | Deduplicación original | Coincide |
| DIF-10 | Deduplicación con repeticiones | Coincide |
| DIF-11 | Geolocalización individual simulada | Coincide |
| DIF-12 | Enriquecimiento de IP | Coincide |
| DIF-13 | Construcción del resumen | Coincide |
| DIF-14 | Persistencia JSON | Coincide |
| DIF-15 | Ejecución integral de main | Coincide |

### 8.1. Resultados comparativos

| Indicador | Hito 1 | Hito 2 |
|---|---|---|
| Porcentaje HTTP 500 | 30.0 % | 30.0 % |
| Cantidad de IP críticas | 2 | 2 |
| Retorno de main en ejecución exitosa | None | 0 |
| Ruta lógica del reporte | data/report.json | data/report.json |

- Comparaciones realizadas: 15.
- Resultados equivalentes: 15.
- Diferencias no esperadas en las comparaciones: 0.
- Peticiones HTTP reales: 0.
- Reportes del repositorio sobrescritos: 0.

### 8.2. Metodología y alcance

- Recuperación del código histórico mediante git show.
- Carga de módulos originales independientes en memoria.
- Simulación de respuestas HTTP mediante unittest.mock.
- Utilización de los mismos datos de entrada.
- Normalización del orden de las IP críticas.
- Generación de reportes en directorios temporales.
- Comparación de estructuras JSON y mensajes de consola.
- Evaluación separada del retorno de main.

Las comprobaciones fueron ejecutadas mediante un script
independiente de pytest. Sus resultados no incrementan
el número de pruebas registradas por pytest.

Las respuestas geográficas simuladas no representan
ubicaciones reales verificadas.

## 9. Diferencias intencionales de compatibilidad

| ID | Diferencia | Justificación |
|---|---|---|
| COMP-01 | Rutas de importación mediante src | Organización modular |
| COMP-02 | Ejecución mediante python -m src.main | Ejecución como módulo |
| COMP-03 | Retorno explícito de main | Códigos de éxito y error |
| COMP-04 | Validaciones adicionales en CSV | Integridad de registros |
| COMP-05 | Validaciones estructurales en JSON | Integridad de eventos |
| COMP-06 | Validaciones de métricas | Protección del cálculo |
| COMP-07 | Validación de IP y configuración de API | Robustez del servicio |
| COMP-08 | Tratamiento de respuestas inesperadas | Manejo defensivo de datos |
| COMP-09 | Ordenamiento de IP críticas de conjuntos | Resultados deterministas |
| COMP-10 | Validación y serialización previa del reporte | Protección de persistencia |
| COMP-11 | Validaciones adicionales en utilidades | Integridad de datos |
| COMP-12 | Deduplicación recursiva | Soporte de estructuras anidadas |

No se afirma retrocompatibilidad absoluta. Determinadas
entradas aceptadas por el Hito 1 pueden ser rechazadas
intencionalmente por las validaciones del Hito 2.

## 10. Pruebas de regresión

Comando ejecutado desde la raíz del repositorio:

```bash
python -m pytest src/ -q --cov=src/models --cov=src/parsers --cov=src/services --cov=src/utils --cov=src.main --cov-report=term-missing
```

### 10.1. Resultado

- Pruebas aprobadas: 478.
- Pruebas fallidas: 0.
- Tiempo de ejecución: 0.50 segundos.
- Archivos de pruebas: 11.
- Sentencias de producción: 358.
- Sentencias cubiertas: 357.
- Sentencias no cubiertas: 1.
- Cobertura calculada: 99.72 %.
- Cobertura mostrada por la herramienta: 99 %.

### 10.2. Cobertura por archivo

| Archivo | Sentencias | No cubiertas | Cobertura mostrada |
|---|---:|---:|---:|
| src/main.py | 35 | 0 | 100 % |
| src/models/__init__.py | 0 | 0 | 100 % |
| src/models/base_log_parser.py | 14 | 1 | 93 % |
| src/parsers/csv_parser.py | 37 | 0 | 100 % |
| src/parsers/json_parser.py | 32 | 0 | 100 % |
| src/services/geolocation_service.py | 61 | 0 | 100 % |
| src/services/metrics_service.py | 32 | 0 | 100 % |
| src/services/report_service.py | 64 | 0 | 100 % |
| src/utils/data_utils.py | 83 | 0 | 100 % |
| Total | 358 | 1 | 99 % |

La única sentencia no cubierta corresponde a la línea 23
de BaseLogParser, específicamente al cuerpo del método
abstracto leer.

No se fuerza su ejecución artificial para aumentar
el porcentaje de cobertura.

La cobertura corresponde a sentencias de producción.
No equivale a cobertura completa de ramas ni garantiza
la ausencia de defectos.

## 11. Decisiones arquitectónicas

| Decisión | Justificación |
|---|---|
| Conservar las funciones de compatibilidad | Mantener las interfaces funcionales originales |
| Conservar data_utils como módulo | Sus operaciones no requieren estado propio |
| Conservar main como función | Su responsabilidad es coordinar el procesamiento |
| Mantener propiedades de solo lectura | Proteger el estado de las instancias |
| No introducir composición artificial | Evitar relaciones innecesarias |
| No forzar cobertura del 100 % | Priorizar pruebas con significado funcional |
| No modificar algoritmos originales sin justificación | Evitar regresiones innecesarias |

## 12. Limitaciones de la auditoría

- Las pruebas diferenciales cubren escenarios seleccionados.
- No se garantiza equivalencia para todas las entradas.
- No se comparan los reportes byte por byte.
- No se verifica la disponibilidad real de la API externa.
- La API predeterminada utiliza HTTP sin cifrado.
- Los atributos con prefijo _ siguen una convención de Python.
- Las propiedades de solo lectura no impiden el acceso
  directo deliberado a los atributos internos.
- La persistencia del reporte no constituye escritura atómica.
- El ordenamiento de conjuntos modifica intencionalmente
  el orden potencial de las IP críticas del Hito 1.
- La interpretación académica definitiva de la refactorización
  completa corresponde al docente.
- La evaluación interna no sustituye una rúbrica oficial.

## 13. Conclusión

La auditoría identifica evidencias favorables para los
cuatro requerimientos oficiales del Hito 2.

Se evaluaron veinte criterios técnicos: diecinueve cumplen
sin observaciones y uno cumple con observaciones de
compatibilidad.

Las doce funciones originales conservan sus nombres y
declaraciones de parámetros. Las quince comparaciones
diferenciales presentan resultados equivalentes en los
escenarios evaluados.

La arquitectura cuenta con seis clases, dos relaciones
de herencia, cinco propiedades y tres diagramas Mermaid.

Las 478 pruebas automatizadas se ejecutaron
satisfactoriamente, con una cobertura de producción
calculada del 99.72 %.

No se identificaron incumplimientos que justifiquen
modificaciones adicionales del código de producción
durante esta parte de la auditoría.

## 14. Documentación relacionada

- [Diagrama UML de clases](diagrama_clases.md)
- [README del proyecto](../README.md)
- [Registro de asistencia de IA](../PROMPTS.md)
