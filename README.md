# TI-Metrics

Engine de Analítica de Logs y Monitoreo de Infraestructura.

Proyecto integrador de Programación II y Aplicaciones de Software.

## 1. Descripción general

TI-Metrics es una aplicación de consola desarrollada en Python
para procesar registros de infraestructura de tecnologías de la
información en formatos CSV y JSON.

El sistema calcula métricas HTTP, identifica direcciones IP
asociadas a eventos críticos, consulta una API REST pública
de geolocalización y genera un reporte estructurado en JSON.

La arquitectura actual utiliza Programación Orientada a Objetos
(POO), funciones auxiliares y mecanismos de validación para
favorecer la modularidad, el mantenimiento y la calidad del software.

## 2. Objetivos del proyecto

### Objetivo general

Desarrollar una herramienta de análisis de registros de
infraestructura TI que permita transformar datos de entrada
en información estructurada mediante una arquitectura modular,
orientada a objetos y respaldada por pruebas automatizadas.

### Objetivos específicos

- Procesar registros CSV y eventos JSON.
- Validar la estructura y el contenido de los datos.
- Identificar y eliminar eventos duplicados.
- Calcular el porcentaje de errores HTTP 500.
- Identificar direcciones IP asociadas a eventos críticos.
- Enriquecer información mediante una API REST.
- Generar reportes persistentes en formato JSON.
- Aplicar abstracción, herencia, polimorfismo y encapsulamiento.
- Verificar el comportamiento mediante pruebas automatizadas.
- Documentar la arquitectura, los resultados y las decisiones técnicas.

## 3. Hito 1: Ingesta de Datos, Persistencia y API REST

**Estado:** desarrollo funcional completado.

### Funcionalidades implementadas

- Lectura de registros desde archivos CSV y JSON.
- Procesamiento mediante listas, diccionarios, tuplas y conjuntos.
- Deduplicación de eventos mediante conjuntos (`set`).
- Cálculo del porcentaje de errores HTTP 500.
- Identificación de direcciones IP críticas.
- Consumo de una API REST mediante `requests`.
- Manejo de excepciones en archivos y peticiones HTTP.
- Generación de un reporte resumido en formato JSON.

### Referencia histórica

| Indicador | Resultado |
|---|---:|
| Pruebas aprobadas | 31 |
| Pruebas fallidas | 0 |
| Cobertura global reportada | 99 % |

La cobertura histórica del Hito 1 no es directamente comparable
con la cobertura exclusiva de producción medida en el Hito 2.

## 4. Hito 2: Refactorización a Arquitectura Orientada a Objetos y UML

**Estado:** implementación, pruebas, auditoría técnica, integración
en la rama principal y validación operativa completadas.

La arquitectura del Hito 2 fue incorporada en main mediante el
[Pull Request #1](https://github.com/carlosarcos2006-eng/TI-Metrics/pull/1),
conservando el historial de desarrollo.

La consolidación documental y la validación técnica del Hito 2
se encuentran completadas. La entrega académica y su evaluación
corresponden a una etapa independiente.

**Badge asociado al hito:** OOP Architect.

### Mejoras implementadas

- Refactorización de los componentes principales mediante clases.
- Implementación de una clase abstracta para los analizadores.
- Aplicación de herencia y polimorfismo.
- Encapsulamiento mediante atributos no públicos y propiedades.
- Validaciones de tipos, estructuras, rangos y direcciones IP.
- Fortalecimiento del manejo de excepciones.
- Conservación de funciones auxiliares y funciones de compatibilidad.
- Ampliación de las pruebas unitarias y de integración.
- Elaboración y actualización de diagramas UML mediante Mermaid.
- Auditoría de requerimientos y compatibilidad funcional.

### Evaluación de requerimientos

| Requerimiento oficial | Evaluación técnica interna |
|---|---|
| Refactorización completa hacia POO | Cumple con observaciones |
| Jerarquía de clases, herencia y polimorfismo | Cumple |
| Encapsulamiento mediante propiedades | Cumple |
| Diagrama de clases UML dentro de docs/ | Cumple |

La auditoría interna comprende 20 criterios técnicos:
19 cumplen sin observaciones y 1 cumple con observaciones.

La observación corresponde a diferencias intencionales de
compatibilidad entre ambos hitos.

Esta evaluación técnica no sustituye la calificación oficial
del docente.

## 5. Arquitectura orientada a objetos

La arquitectura contiene seis clases principales:
una clase abstracta y cinco clases concretas.

### Clases implementadas

| Clase | Tipo | Responsabilidad |
|---|---|---|
| BaseLogParser | Abstracta | Define el contrato común de lectura y valida la ruta. |
| CSVLogParser | Concreta | Lee y valida registros CSV. |
| JSONLogParser | Concreta | Lee y valida eventos JSON. |
| MetricsService | Concreta | Encapsula registros y calcula métricas HTTP. |
| GeolocationService | Concreta | Consulta y procesa información de geolocalización. |
| ReportService | Concreta | Construye y persiste reportes JSON. |

### Principios de POO aplicados

**Abstracción:** `BaseLogParser` utiliza `ABC` y
`@abstractmethod` para definir el contrato `leer()`.

**Herencia:** `CSVLogParser` y `JSONLogParser` heredan
de `BaseLogParser`.

**Polimorfismo:** ambos analizadores implementan `leer()`
de acuerdo con su formato de entrada.

**Encapsulamiento:** las clases utilizan atributos no públicos
y propiedades de solo lectura mediante `@property`.

**Coordinación de objetos y dependencias:** `main()` crea
instancias de los analizadores y servicios para coordinar
el procesamiento. Esta interacción representa dependencias
de uso, no una relación estructural de composición UML.

### Encapsulamiento

| Clase | Atributo interno | Propiedad de solo lectura |
|---|---|---|
| BaseLogParser | `_ruta_archivo` | `ruta_archivo` |
| MetricsService | `_registros` | `registros` |
| GeolocationService | `_url_base` | `url_base` |
| GeolocationService | `_timeout` | `timeout` |
| ReportService | `_indentacion` | `indentacion` |

El prefijo `_` representa una convención de acceso no público
en Python, no una restricción absoluta de acceso.

`MetricsService` utiliza copias defensivas mediante `deepcopy()`
para proteger sus registros frente a modificaciones externas.

### Validaciones y manejo de excepciones

| Componente | Validaciones principales |
|---|---|
| BaseLogParser | Tipo y contenido de la ruta. |
| CSVLogParser | Encabezados, campos, códigos HTTP y tiempos de respuesta. |
| JSONLogParser | Estructura JSON, registros y campos obligatorios. |
| MetricsService | Tipo de colección, registros y códigos HTTP. |
| GeolocationService | URL, timeout, direcciones IP y respuestas de la API. |
| ReportService | Porcentajes, direcciones IP, estructura y serialización JSON. |
| data_utils | Estructuras, campos, direcciones IP y deduplicación. |
| main | Manejo de errores esperados y códigos de salida. |

Los analizadores verifican que los campos IP no estén vacíos.
La validación del formato de las direcciones IP se realiza
en los componentes que requieren dicha comprobación.

Las funciones auxiliares sin estado se mantienen como funciones,
evitando introducir clases innecesarias.

## 6. Flujo de procesamiento

El punto de entrada de la aplicación es `src/main.py`.

1. Inicializar los analizadores CSV y JSON.
2. Leer los registros de `data/logs.csv`.
3. Leer los eventos de `data/events.json`.
4. Eliminar eventos duplicados.
5. Calcular el porcentaje de errores HTTP 500.
6. Identificar las direcciones IP críticas.
7. Consultar la información de geolocalización.
8. Construir el resumen de resultados.
9. Guardar el reporte en `data/report.json`.
10. Mostrar los resultados en la consola.

El programa devuelve el código de salida `0` cuando finaliza
correctamente y `1` ante los errores esperados que captura.

Los errores inesperados que no pertenecen a las excepciones
gestionadas pueden propagarse.

## 7. Tecnologías y requisitos del entorno

### Entorno verificado

| Tecnología | Versión utilizada |
|---|---|
| Python | 3.14.0 |
| requests | 2.34.2 |
| pytest | 9.1.1 |
| pytest-cov | 7.1.0 |
| Sistema operativo | macOS |
| Entorno virtual | venv |

También se utilizan Git, GitHub, Mermaid y PyCharm como
herramientas de desarrollo, control de versiones y documentación.

### Dependencias externas

- `requests`: consumo de servicios HTTP.
- `pytest`: ejecución de pruebas automatizadas.
- `pytest-cov`: medición de cobertura.

Las dependencias se encuentran declaradas en `requirements.txt`.

El archivo no fija versiones específicas. Las versiones indicadas
corresponden al entorno verificado, no a requisitos mínimos
ni a una garantía de compatibilidad con otras versiones.

La comprobación `python -m pip check` no detectó dependencias
incompatibles o faltantes en el entorno utilizado.

## 8. Estructura del repositorio

El repositorio contiene 29 archivos versionados, incluyendo
11 archivos de pruebas automatizadas.

```text
TI-Metrics/
├── .gitignore
├── PROMPTS.md
├── README.md
├── requirements.txt
├── data/
│   ├── events.json
│   ├── logs.csv
│   └── report.json
├── docs/
│   ├── diagrama_clases.md
│   └── matriz_cumplimiento_hito2.md
└── src/
    ├── main.py
    ├── models/
    │   ├── __init__.py
    │   └── base_log_parser.py
    ├── parsers/
    │   ├── csv_parser.py
    │   └── json_parser.py
    ├── services/
    │   ├── geolocation_service.py
    │   ├── metrics_service.py
    │   └── report_service.py
    ├── utils/
    │   └── data_utils.py
    ├── test_csv.py
    ├── test_geolocation.py
    ├── test_geolocation_service.py
    ├── test_integracion.py
    ├── test_json.py
    ├── test_main.py
    ├── test_metrics_service.py
    ├── test_poo_parsers.py
    ├── test_report.py
    ├── test_report_service.py
    └── test_utils.py
```

| Directorio | Responsabilidad |
|---|---|
| data/ | Archivos de entrada y reporte generado. |
| docs/ | Documentación técnica especializada. |
| src/models/ | Clases base y abstracciones. |
| src/parsers/ | Lectura y validación de archivos. |
| src/services/ | Métricas, geolocalización y reportes. |
| src/utils/ | Funciones auxiliares y validaciones compartidas. |
| src/test_*.py | Pruebas unitarias y de integración. |

## 9. Instalación

### 9.1. Clonar el repositorio

```bash
git clone https://github.com/carlosarcos2006-eng/TI-Metrics.git
cd TI-Metrics
```

El Hito 2 se encuentra integrado en la rama principal `main`.

Para seleccionar y actualizar esta rama:

```bash
git switch main
git pull --ff-only origin main
```

La rama `feat/hito2-poo` se conserva como referencia histórica
del desarrollo de la arquitectura orientada a objetos.

### 9.2. Crear un entorno virtual

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
py -m venv .venv
.venv/Scripts/Activate.ps1
```

Las instrucciones para Linux y Windows son referencias de
configuración. La validación documentada se realizó en macOS.

### 9.3. Instalar las dependencias

Desde la raíz del proyecto y con el entorno virtual activo:

```bash
python -m pip install -r requirements.txt
```

### 9.4. Comprobar las dependencias

```bash
python -m pip check
```

Resultado esperado:

```text
No broken requirements found.
```

## 10. Ejecución y resultados de referencia

Ejecutar desde la raíz del repositorio:

```bash
python -m src.main
```

### Datos de entrada de referencia

| Indicador | Cantidad |
|---|---:|
| Registros CSV | 10 |
| Registros HTTP 500 | 3 |
| Eventos JSON | 6 |
| Direcciones IP únicas en eventos JSON | 3 |
| Direcciones IP críticas | 2 |

### Salida de referencia

```text
TI-Metrics iniciado correctamente
Porcentaje HTTP 500: 30.0 %
Cantidad de IP críticas: 2
Reporte generado en: data/report.json
```

El porcentaje de errores HTTP 500 se obtiene dividiendo
la cantidad de registros con estado 500 entre el total
de registros y multiplicando el resultado por 100.

Para los datos de referencia:

```text
(3 / 10) * 100 = 30.0 %
```

### Reporte generado

El archivo `data/report.json` contiene tres campos principales:

- `porcentaje_http_500`
- `ips_criticas`
- `geolocalizaciones`

Las direcciones IP críticas de referencia son:

- `192.168.1.10`
- `203.0.113.25`

La primera pertenece a un rango privado y la segunda a un
rango reservado para documentación (TEST-NET-3).

No deben interpretarse las respuestas simuladas de geolocalización
como ubicaciones geográficas reales de estas direcciones.

Los resultados de geolocalización dependen de la respuesta
del servicio externo y pueden contener valores `null`.

La ejecución puede sobrescribir el reporte existente.

### Validación operativa definitiva

**Fecha planificada:** 22 de noviembre de 2026.

**Fecha de ejecución técnica:** 24 de noviembre de 2026.

Se ejecutó la aplicación desde la rama principal main,
utilizando los archivos originales del proyecto y sin
simular las peticiones HTTP de esta ejecución.

| Indicador | Resultado |
|---|---:|
| Código de salida | 0 |
| Registros CSV procesados | 10 |
| Direcciones IP únicas en CSV | 4 |
| Registros HTTP 200 | 5 |
| Registros HTTP 401 | 1 |
| Registros HTTP 404 | 1 |
| Registros HTTP 500 | 3 |
| Porcentaje HTTP 500 | 30.0 % |
| Eventos JSON procesados | 6 |
| Eventos INFO | 2 |
| Eventos WARNING | 2 |
| Eventos CRITICAL | 2 |
| Eventos duplicados encontrados | 0 |
| Direcciones IP únicas en JSON | 3 |
| Direcciones IP críticas | 2 |
| Resultados de geolocalización | 2 |
| Resultados de geolocalización no nulos | 1 |
| Resultados de geolocalización nulos | 1 |

Los resultados CSV y JSON fueron contrastados mediante
comprobaciones independientes y coincidieron con los
resultados de los componentes de producción.

La ausencia de duplicados en los datos originales no demuestra
por sí sola la eliminación de eventos duplicados. Este
comportamiento se verifica mediante pruebas automatizadas.

### Auditoría del reporte generado

El reporte original y el generado tuvieron un tamaño de
677 bytes y conservaron los mismos resultados funcionales
en los campos evaluados.

Se identificaron dos observaciones técnicas:

- **GEO-OBS-01:** la respuesta no nula correspondiente a
  203.0.113.25 no constituye evidencia de una ubicación
  geográfica real, debido a que pertenece a TEST-NET-3.
  La dirección privada 192.168.1.10 produjo un resultado nulo.
- **REP-OBS-01:** el orden de las direcciones IP críticas
  cambió debido al ordenamiento determinista de los conjuntos
  en ReportService. Los reportes no fueron idénticos a nivel
  binario ni como estructuras JSON completas.

Se conservó temporalmente una copia del reporte generado
fuera del repositorio y se restauró el reporte original.

La restauración fue verificada mediante comparación binaria,
comparación JSON y huellas SHA-256 coincidentes.

El respaldo temporal no constituye almacenamiento permanente.
La auditoría no garantiza la disponibilidad futura de la API.

## 11. Pruebas automatizadas y cobertura

### Ejecutar la suite completa

```bash
python -m pytest src/ -v
```

### Ejecutar con cobertura de producción

```bash
python -m pytest src/ -q --cov=src/models --cov=src/parsers --cov=src/services --cov=src/utils --cov=src.main --cov-report=term-missing
```

El comando limita la medición a los módulos de producción,
excluyendo los archivos de pruebas del cálculo.

### Última validación técnica documentada

**Fecha:** 13 de noviembre de 2026.

| Indicador | Resultado |
|---|---:|
| Archivos de pruebas | 11 |
| Pruebas aprobadas | 478 |
| Pruebas fallidas | 0 |
| Sentencias de producción | 358 |
| Sentencias cubiertas | 357 |
| Sentencias no cubiertas | 1 |
| Cobertura de producción | 99.72 % |

### Validación posterior a la integración

Después de incorporar el Pull Request #1, se ejecutó nuevamente
la suite completa de pruebas desde la rama main.

| Indicador | Resultado |
|---|---:|
| Rama evaluada | main |
| Merge commit evaluado | 92a0e1d |
| Pruebas aprobadas | 478 |
| Pruebas fallidas | 0 |
| Sentencias de producción | 358 |
| Sentencias cubiertas | 357 |
| Sentencias no cubiertas | 1 |
| Cobertura de producción | 99.72 % |
| Tiempo de ejecución observado | 1.09 s |

Los resultados de aprobación y cobertura coinciden con la
validación realizada antes de la integración definitiva.

No se detectaron regresiones mediante la suite automatizada.
Esta comprobación no sustituye la validación operativa final
ni garantiza la ausencia absoluta de defectos.

### Validación definitiva del Hito 2

**Fecha planificada:** 22 de noviembre de 2026.

**Fecha de ejecución técnica:** 24 de noviembre de 2026.

| Indicador | Resultado |
|---|---:|
| Rama evaluada | main |
| Commit de referencia | 1352107 |
| Archivos de pruebas | 11 |
| Pruebas aprobadas | 478 |
| Pruebas fallidas | 0 |
| Sentencias de producción | 358 |
| Sentencias cubiertas | 357 |
| Sentencias no cubiertas | 1 |
| Cobertura calculada | 99.72 % |
| Cobertura mostrada por la herramienta | 99 % |
| Tiempo de la suite con cobertura | 0.57 s |

Los resultados definitivos coinciden con los obtenidos
durante las validaciones anteriores.

No se detectaron regresiones mediante la suite automatizada.
Los tiempos observados no constituyen una evaluación formal
del rendimiento del sistema.

La ejecución operativa y las pruebas automatizadas aportan
evidencia complementaria, sin garantizar la ausencia
absoluta de defectos.

### Distribución de pruebas

| Componente | Pruebas aprobadas |
|---|---:|
| Analizadores CSV, JSON y POO | 90 |
| Métricas | 43 |
| Geolocalización | 65 |
| Reportes | 92 |
| Funciones auxiliares | 161 |
| Aplicación principal | 22 |
| Integración | 5 |
| **Total** | **478** |

### Interpretación de la cobertura

La cobertura calculada corresponde a:

```text
(357 / 358) * 100 = 99.72 %
```

La única sentencia no cubierta corresponde al `pass`
del método abstracto `leer()` de `BaseLogParser`.

Se conserva dicha implementación abstracta sin introducir
ejecuciones artificiales para alcanzar el 100 %.

La cobertura mide sentencias ejecutadas durante las pruebas.
No garantiza la ausencia de errores ni equivale a una
cobertura completa de ramas o escenarios posibles.

### Estrategias de pruebas

- Pruebas unitarias.
- Pruebas parametrizadas.
- Validación de entradas correctas e incorrectas.
- Simulación de dependencias mediante mocks.
- Verificación de excepciones y mensajes.
- Verificación de abstracción, herencia y polimorfismo.
- Comprobación de copias defensivas y encapsulamiento.
- Pruebas de integración con archivos temporales.
- Simulación de respuestas HTTP sin depender de la API real.

## 12. Compatibilidad funcional entre hitos

Se realizó una auditoría comparativa entre la versión
procedural del Hito 1 y la arquitectura POO del Hito 2.

| Indicador | Resultado |
|---|---:|
| Funciones originales conservadas | 12/12 |
| Firmas de parámetros conservadas | 12/12 |
| Funcionalidades originales documentadas | 8/8 |
| Funciones de compatibilidad | 7 |
| Comparaciones diferenciales satisfactorias | 15/15 |
| Diferencias intencionales documentadas | 12 |

Las siete funciones de compatibilidad permiten conservar
los nombres de las operaciones procedurales refactorizadas
mediante llamadas a las clases correspondientes.

Los escenarios comparados conservaron los resultados
funcionales esperados, incluyendo el 30.0 % de errores HTTP 500
y las dos direcciones IP críticas.

La conservación de nombres y parámetros no implica una
retrocompatibilidad absoluta.

Existen diferencias intencionales en las rutas de importación,
validaciones de entradas, códigos de salida, ordenamiento
de resultados y tratamiento de datos.

Los detalles y limitaciones de la comparación se encuentran
en la matriz de cumplimiento del Hito 2.

## 13. Documentación técnica

| Documento | Contenido |
|---|---|
| [Diagrama UML](docs/diagrama_clases.md) | Clases, dependencias y flujo de procesamiento. |
| [Matriz de cumplimiento](docs/matriz_cumplimiento_hito2.md) | Requerimientos, criterios técnicos y compatibilidad. |
| [Registro de asistencia de IA](PROMPTS.md) | Prompts, respuestas, análisis crítico y soluciones finales. |

La documentación UML incluye tres diagramas Mermaid:

1. Diagrama de clases.
2. Diagrama de dependencias arquitectónicas.
3. Diagrama del flujo de procesamiento.

La matriz de cumplimiento documenta los cuatro requerimientos
oficiales del Hito 2 y los resultados de la auditoría interna.

## 14. Registro de asistencia de inteligencia artificial

La asistencia de inteligencia artificial utilizada durante
el desarrollo se documenta en [PROMPTS.md](PROMPTS.md).

Cada registro contiene:

- Fecha.
- Módulo o función.
- Prompt enviado.
- Respuesta de la IA.
- Análisis crítico.
- Solución final.

Las propuestas generadas se someten a revisión, adaptación
y validación técnica antes de incorporarse al proyecto.

Al finalizar el Hito 2, PROMPTS.md contiene 54 registros
con numeración consecutiva y sin identificadores duplicados.

| Indicador | Resultado |
|---|---:|
| Registros del Hito 1 | 35 |
| Registros adicionales del Hito 2 | 19 |
| Total de registros | 54 |

El registro final, correspondiente al Prompt #54, documenta
la validación operativa, las pruebas definitivas, la auditoría
del reporte y las limitaciones identificadas.

Las fechas planificadas se distinguen de las fechas de
ejecución técnica cuando ambas no coinciden.

## 15. Limitaciones técnicas

- La geolocalización depende de la disponibilidad de una API externa.
- La configuración predeterminada de la API utiliza HTTP sin cifrado.
- Las respuestas simuladas no constituyen geolocalizaciones reales.
- Una respuesta exitosa para una IP reservada para documentación
  no demuestra una ubicación geográfica real.
- El orden de las direcciones IP críticas puede diferir entre
  versiones sin modificar los resultados funcionales evaluados.
- Las rutas relativas requieren ejecutar desde la raíz del proyecto
  o desde un entorno que reproduzca la estructura esperada.
- El reporte JSON no se guarda mediante escritura atómica.
- El directorio de destino del reporte debe existir.
- La cobertura de sentencias no garantiza la ausencia de errores.
- Las comparaciones diferenciales no prueban compatibilidad absoluta.
- Las dependencias no tienen versiones fijadas en requirements.txt.

Estas limitaciones se documentan para mantener la transparencia
técnica y orientar futuras mejoras.

## 16. Estado del proyecto y próximas etapas

| Etapa | Estado |
|---|---|
| Hito 1: Ingesta de datos, persistencia y API REST | Completado |
| Hito 2: Implementación de arquitectura POO | Completado |
| Hito 2: Validaciones y pruebas automatizadas | Completado |
| Hito 2: Diagramas UML y auditoría de requerimientos | Completado |
| Hito 2: Consolidación documental | Completado |
| Hito 2: Integración en la rama principal | Completado |
| Hito 2: Regresión posterior a la integración | Completado |
| Hito 2: Validación operativa definitiva | Completado |
| Hito 2: Entrega y evaluación académica | Pendiente |
| Hito 3: Consolidación de calidad, auditoría y defensa oral | Pendiente |

La integración del Hito 2 en la rama principal se encuentra
completada mediante el Pull Request #1.

El Hito 2 cuenta con una arquitectura orientada a objetos,
documentación UML, una matriz de cumplimiento, 478 pruebas
automatizadas aprobadas y una cobertura de producción del
99.72 %.

La validación operativa confirmó los resultados esperados
para los archivos originales y documentó las limitaciones
identificadas durante la ejecución.

El repositorio conserva los 29 archivos versionados previstos
y los 54 registros de asistencia de inteligencia artificial.

La preparación de la defensa académica se realizará como
una actividad independiente del desarrollo técnico.

La evaluación oficial del Hito 2 corresponde al docente.
Las siguientes actividades de desarrollo estarán orientadas
a los requerimientos del Hito 3.
