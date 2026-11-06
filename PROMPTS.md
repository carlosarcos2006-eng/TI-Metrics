# Auditoría de Prompts - TI-Metrics

Este documento registra las interacciones realizadas con
herramientas de inteligencia artificial durante el desarrollo
del proyecto TI-Metrics.

Cada registro incluye el prompt utilizado, la respuesta recibida,
el análisis crítico realizado y la solución finalmente integrada
al proyecto.

## Registro de Prompt #1

* **Fecha:** 2026-10-02
* **Módulo/Función:** Estructura inicial del proyecto
* **Prompt Enviado:** "Necesito continuar con el proyecto TI-Metrics y configurar la estructura inicial del repositorio para comenzar el Hito 1."
* **Respuesta de la IA:** La IA indicó cómo organizar el repositorio, configurar el entorno virtual, instalar las dependencias y preparar los archivos iniciales del proyecto.
* **Análisis Crítico:** La propuesta permitió organizar el proyecto siguiendo una estructura separada por responsabilidades. Se verificó que las carpetas y archivos fueran adecuados para los requisitos del proyecto y que Git estuviera correctamente configurado.
* **Solución Final Aplicada:** Se creó y configuró el repositorio TI-Metrics con Git, GitHub, entorno virtual, requirements.txt, .gitignore, README.md, PROMPTS.md y src/main.py.

## Registro de Prompt #2

* **Fecha:** 2026-10-02
* **Módulo/Función:** src/parsers/csv_parser.py - leer_logs_csv()
* **Prompt Enviado:** "Necesito comenzar el Hito 1 de TI-Metrics. Quiero crear un parser para leer el archivo logs.csv y entender paso a paso cómo funciona."
* **Respuesta de la IA:** La IA propuso utilizar el módulo csv de Python y csv.DictReader para leer los registros, convertir los campos status y response_time a enteros y devolver una lista de registros.
* **Análisis Crítico:** Se verificó que DictReader permite utilizar los encabezados del CSV como claves de cada registro. También se identificó la necesidad de convertir status y response_time de texto a enteros para poder realizar posteriormente comparaciones y cálculos numéricos. La solución fue probada con 10 registros y produjo el resultado esperado.
* **Solución Final Aplicada:** Se implementó la función leer_logs_csv() en src/parsers/csv_parser.py. La función abre el archivo CSV, utiliza DictReader, convierte status y response_time a enteros, almacena las filas en una lista y devuelve los registros procesados.

## Registro de Prompt #3

* **Fecha:** 2026-10-02
* **Módulo/Función:** src/services/metrics_service.py - calcular_porcentaje_http_500()
* **Prompt Enviado:** "Necesito calcular el porcentaje de registros que tienen un código HTTP 500 en los logs procesados."
* **Respuesta de la IA:** La IA propuso recorrer los registros, contar aquellos cuyo campo status fuera igual a 500 y calcular el porcentaje respecto al total de registros.
* **Análisis Crítico:** La primera ejecución produjo 0.0% aunque el archivo contenía tres registros con status 500. Se realizó una comprobación de los tipos de datos y se confirmó que status era de tipo int. Al revisar la condición de comparación se detectó que el valor 500 había sido escrito entre comillas, convirtiéndolo en texto. Esto provocaba una comparación entre un entero y una cadena, por lo que la condición nunca se cumplía.
* **Solución Final Aplicada:** Se corrigió la condición para comparar el valor entero 500 sin comillas. Después de la corrección, la función procesó los 10 registros y obtuvo correctamente un porcentaje de HTTP 500 del 30.0%.

## Registro de Prompt #4

* **Fecha:** 2026-10-02
* **Módulo/Función:** src/parsers/json_parser.py - leer_eventos_json()
* **Prompt Enviado:** "Necesito continuar con el Hito 1 de TI-Metrics y crear un parser para leer el archivo events.json. Quiero entender paso a paso cómo funciona."
* **Respuesta de la IA:** La IA propuso utilizar el módulo estándar json de Python y json.load() para abrir el archivo JSON y convertir su contenido en estructuras de Python.
* **Análisis Crítico:** Se verificó que el archivo contiene una lista de objetos JSON y que json.load() es apropiado porque permite leer directamente desde un archivo. También se comprobó que la función debe limitarse a cargar y devolver los datos, manteniendo separada la responsabilidad de procesamiento y análisis.
* **Solución Final Aplicada:** Se implementó leer_eventos_json() en src/parsers/json_parser.py. La función abre events.json utilizando UTF-8, carga su contenido mediante json.load() y devuelve la lista de eventos. La prueba realizada mediante src/test_json.py confirmó que se cargaron correctamente 6 eventos y que el primer registro mantiene la estructura esperada.

## Registro de Prompt #5

* **Fecha:** 2026-10-02
* **Módulo/Función:** src/utils/data_utils.py - obtener_ips_unicas()
* **Prompt Enviado:** "Necesito continuar con el Hito 1 de TI-Metrics y utilizar conjuntos para eliminar IPs duplicadas de los registros de eventos."
* **Respuesta de la IA:** La IA propuso utilizar un conjunto (`set`) para almacenar las direcciones IP mientras se recorren los registros, aprovechando que los conjuntos no permiten elementos duplicados.
* **Análisis Crítico:** Se verificó que un `set` es apropiado para obtener valores únicos y que no debe utilizarse cuando sea necesario conservar un orden específico. También se comprobó que las IPs repetidas de los eventos son almacenadas una sola vez.
* **Solución Final Aplicada:** Se implementó obtener_ips_unicas() en src/utils/data_utils.py. La función recorre los registros, obtiene el campo ip y lo agrega a un conjunto. La prueba confirmó que los 6 eventos contienen 3 IPs únicas.

## Registro de Prompt #6

* **Fecha:** 2026-10-02
* **Módulo/Función:** src/utils/data_utils.py - crear_resumen_evento()
* **Prompt Enviado:** "Necesito continuar con el Hito 1 de TI-Metrics y utilizar tuplas para representar un resumen de cada evento."
* **Respuesta de la IA:** La IA propuso crear una función que extraiga de cada evento la IP, el tipo de evento y su nivel de severidad, almacenándolos en una tupla.
* **Análisis Crítico:** Se verificó que una tupla es adecuada para representar un conjunto fijo de datos relacionados, ya que sus elementos no necesitan modificarse después de ser creados. También se comprobó mediante una prueba que el resultado generado corresponde realmente al tipo tuple.
* **Solución Final Aplicada:** Se implementó crear_resumen_evento() en src/utils/data_utils.py. La función recibe un evento y devuelve una tupla con la IP, el tipo de evento y la severidad. La prueba confirmó que el primer evento genera correctamente la tupla ('8.8.8.8', 'login', 'INFO').

## Registro de Prompt #7

* **Fecha:** 2026-10-02
* **Módulo/Función:** src/utils/data_utils.py - obtener_ips_criticas()
* **Prompt Enviado:** "Necesito continuar con el Hito 1 de TI-Metrics e identificar las IPs que tienen eventos con severidad CRITICAL utilizando conjuntos."
* **Respuesta de la IA:** La IA propuso recorrer los eventos, verificar el campo severity y, cuando su valor fuera CRITICAL, agregar la IP correspondiente a un conjunto.
* **Análisis Crítico:** Se verificó que utilizar un set es apropiado porque una misma IP puede generar varios eventos críticos y debe aparecer una sola vez en el resultado. También se comprobó que la comparación debe realizarse con el texto "CRITICAL", ya que ese es el valor almacenado en el archivo JSON.
* **Solución Final Aplicada:** Se implementó obtener_ips_criticas() en src/utils/data_utils.py. La función recorre los eventos, identifica aquellos cuya severidad es CRITICAL y almacena sus IPs en un conjunto. La prueba confirmó que existen 2 IPs asociadas a eventos críticos: 192.168.1.10 y 203.0.113.25.

## Registro de Prompt #8

* **Fecha:** 2026-10-02
* **Módulo/Función:** src/services/geolocation_service.py - obtener_geolocalizacion()
* **Prompt Enviado:** "Necesito consumir una API REST para obtener información geográfica de una dirección IP en el proyecto TI-Metrics y manejar correctamente los posibles errores de comunicación."
* **Respuesta de la IA:** La IA propuso utilizar la biblioteca requests para realizar una solicitud GET a la API de geolocalización, establecer un tiempo máximo de espera y manejar excepciones relacionadas con la comunicación.
* **Análisis Crítico:** La primera implementación funcionó correctamente con una IP válida. Durante las pruebas se utilizó la IP 999.999.999.999 y se observó que la API podía responder mediante HTTP 200 aunque el contenido indicara status "fail". Por este motivo se identificó que comprobar únicamente el código HTTP no era suficiente. Se agregó una validación del campo status de la respuesta y se mantuvo el manejo de Timeout y RequestException para evitar que errores externos detengan la aplicación.
* **Solución Final Aplicada:** Se implementó obtener_geolocalizacion() en src/services/geolocation_service.py. La función construye la URL de la API, realiza una petición GET con timeout de 5 segundos, verifica el código HTTP, analiza el JSON recibido, valida que el estado de la API sea "success" y maneja errores de timeout y solicitudes. Las pruebas con una IP válida e inválida confirmaron el comportamiento esperado.

## Registro de Prompt #9

* **Fecha:** 2026-10-02
* **Módulo/Función:** src/services/geolocation_service.py - enriquecer_ips_con_geolocalizacion()
* **Prompt Enviado:** "Necesito integrar la función de geolocalización con varias direcciones IP para enriquecer los registros del proyecto TI-Metrics."
* **Respuesta de la IA:** La IA propuso crear una función que reciba una colección de IPs, recorra cada dirección y utilice la función obtener_geolocalizacion() para consultar la API. Los resultados se almacenarían en un diccionario utilizando cada IP como clave.
* **Análisis Crítico:** Se consideró adecuado separar la responsabilidad de realizar una consulta individual de la responsabilidad de procesar varias IPs. La función obtener_geolocalizacion() mantiene la lógica de comunicación con la API, mientras que enriquecer_ips_con_geolocalizacion() coordina varias consultas. La implementación fue probada con las IPs 8.8.8.8 y 1.1.1.1, obteniendo correctamente información geográfica para ambas.
* **Solución Final Aplicada:** Se implementó enriquecer_ips_con_geolocalizacion() en src/services/geolocation_service.py. La función recibe un conjunto de IPs, crea un diccionario de resultados, consulta la geolocalización de cada IP mediante obtener_geolocalizacion() y devuelve la información asociada a cada dirección. La prueba confirmó que las consultas se procesan correctamente.

## Registro de Prompt #10

* **Fecha:** 2026-10-02
* **Módulo/Función:** src/services/report_service.py - construir_resumen()
* **Prompt Enviado:** "Necesito integrar los resultados del procesamiento de logs, las IPs críticas y la información geográfica en una estructura de resumen para el reporte del proyecto TI-Metrics."
* **Respuesta de la IA:** La IA propuso crear una función independiente que recibiera el porcentaje de errores HTTP 500, el conjunto de IPs críticas y el diccionario de geolocalizaciones, y que los organizara dentro de un único diccionario de resumen.
* **Análisis Crítico:** Se consideró conveniente separar la construcción del resumen de las funciones encargadas de procesar los archivos y consultar la API. También se identificó que las IPs críticas se almacenaban como un conjunto para evitar duplicados, por lo que se convierten a una lista al preparar la estructura del reporte. La prueba confirmó que el resultado final es un diccionario con el porcentaje HTTP 500, las IPs críticas y las geolocalizaciones.
* **Solución Final Aplicada:** Se implementó construir_resumen() en src/services/report_service.py. La función recibe los resultados procesados, crea un diccionario con las claves porcentaje_http_500, ips_criticas y geolocalizaciones, convierte el conjunto de IPs críticas en una lista y devuelve el resumen. La prueba realizada confirmó que la estructura generada es correcta.

## Registro de Prompt #11

* **Fecha:** 2026-10-02
* **Módulo/Función:** src/services/report_service.py - guardar_reporte_json()
* **Prompt Enviado:** "Necesito guardar el resumen generado por TI-Metrics en un archivo JSON dentro de la carpeta data."
* **Respuesta de la IA:** La IA propuso utilizar el módulo estándar json y una función independiente que recibiera el resumen y la ruta del archivo. La función utilizaría open() en modo escritura y json.dump() para convertir el diccionario de Python a formato JSON.
* **Análisis Crítico:** Durante la primera prueba se produjo un FileNotFoundError porque el programa se ejecutó desde la carpeta src y la ruta relativa data/report.json fue interpretada como src/data/report.json. Se identificó que las rutas relativas dependen del directorio actual de ejecución. La solución fue ejecutar la prueba desde la raíz del proyecto, manteniendo la ruta data/report.json porque corresponde a la estructura real del proyecto.
* **Solución Final Aplicada:** Se implementó guardar_reporte_json() en src/services/report_service.py utilizando open() y json.dump(). La función genera el archivo data/report.json con formato legible mediante indent=4. La prueba final confirmó que el archivo se creó correctamente y que os.path.exists() devolvió True.

## Registro de Prompt #12

* **Fecha:** 2026-10-02
* **Módulo/Función:** Prueba de `enriquecer_ips_con_geolocalizacion()` con IPs críticas
* **Prompt Enviado:** "Necesito probar la función de geolocalización utilizando las IPs críticas obtenidas de los eventos del proyecto TI-Metrics."
* **Respuesta de la IA:** La IA indicó realizar una prueba utilizando las IPs críticas 192.168.1.10 y 203.0.113.25, recorrer los resultados obtenidos y verificar cómo responde la API ante cada dirección.
* **Análisis Crítico:** La prueba mostró que las IPs críticas no necesariamente producen el mismo resultado. La IP 192.168.1.10 devolvió None, mientras que 203.0.113.25 devolvió información geográfica proporcionada por la API. Esto confirma que el programa debe aceptar resultados sin geolocalización disponible y no asumir que todas las IPs pueden ser ubicadas.
* **Solución Final Aplicada:** Se probó `enriquecer_ips_con_geolocalizacion()` utilizando las IPs críticas reales del proyecto. La función procesó ambas direcciones correctamente, conservando None cuando la API no proporcionó información y almacenando los datos recibidos cuando la consulta fue exitosa.

## Registro de Prompt #13

* **Fecha:** 2026-10-02
* **Módulo/Función:** Integración del procesamiento de logs, eventos, geolocalización y generación de reportes
* **Prompt Enviado:** "Necesito integrar todo lo desarrollado hasta ahora en el Hito 1 para que el reporte final utilice directamente los datos de logs.csv y events.json, consulte la geolocalización de las IPs críticas y genere report.json."
* **Respuesta de la IA:** La IA propuso modificar la prueba del reporte para utilizar directamente los parsers de CSV y JSON, calcular el porcentaje de HTTP 500, obtener las IPs críticas, consultar su geolocalización, construir el resumen y finalmente guardar el reporte JSON.
* **Análisis Crítico:** Se verificó que la integración no utilizara valores calculados manualmente, sino los resultados obtenidos directamente de los archivos de entrada y de la API REST. La prueba confirmó que se procesaron 10 registros CSV, se obtuvo un porcentaje HTTP 500 del 30.0%, se identificaron 2 IPs críticas y se obtuvo información geográfica para una de ellas, mientras que la otra devolvió None. También se comprobó que el archivo report.json fue generado correctamente.
* **Solución Final Aplicada:** Se actualizó src/test_report.py para coordinar todos los componentes desarrollados durante el Hito 1. El flujo completo lee los archivos de entrada, procesa sus datos, identifica IPs críticas, consulta la API de geolocalización, construye el resumen y genera data/report.json.

## Registro de Prompt #14

* **Fecha:** 2026-10-02
* **Módulo/Función:** Validación de data/report.json
* **Prompt Enviado:** "Necesito verificar que el archivo report.json generado por la integración del Hito 1 tenga la estructura y los resultados esperados."
* **Respuesta de la IA:** La IA indicó revisar el contenido del archivo report.json y comprobar el porcentaje de HTTP 500, las IPs críticas y la información de geolocalización obtenida para cada IP.
* **Análisis Crítico:** Se verificó que el reporte contiene un porcentaje de HTTP 500 de 30.0%, las dos IPs críticas identificadas a partir de events.json y la información de geolocalización obtenida mediante la API. También se comprobó que la IP 192.168.1.10 aparece como null en JSON debido a que la API no proporcionó información, lo cual corresponde al comportamiento esperado. La representación null es equivalente a None en Python al serializar los datos mediante json.dump().
* **Solución Final Aplicada:** Se validó manualmente el contenido de data/report.json después de ejecutar la integración completa. La estructura y los resultados obtenidos coinciden con los datos procesados y con las respuestas proporcionadas por la API.

## Registro de Prompt #15

* **Fecha:** 2026-10-09
* **Módulo/Función:** src/utils/data_utils.py - obtener_ips_criticas()
* **Prompt Enviado**  "Necesito probar el comportamiento de obtener_ips_criticas() cuando recibe eventos válidos, pero ninguno tiene severidad CRITICAL. Quiero verificar que devuelva un conjunto vacío y que las IP repetidas no generen resultados incorrectos."
* **Respuesta de la IA:** La IA propuso ejecutar una prueba aislada con eventos de severidad INFO y WARNING, llamar a la función existente y utilizar una aserción para comprobar que el resultado fuera un conjunto vacío.
* **Análisis Crítico:** Se ejecutó la prueba utilizando tres eventos, dos de ellos asociados a la misma IP. La función devolvió set(), y el tipo del resultado fue set. La aserción se cumplió, por lo que no fue necesario modificar la implementación.
* **Solución Final:** Se verificó mediante una prueba aislada que obtener_ips_criticas() devuelve un conjunto vacío cuando ningún evento tiene severidad CRITICAL. La prueba terminó correctamente y confirmó el comportamiento esperado para este caso.

## Registro de Prompt #16

* **Fecha:** 2026-10-09
* **Módulo/Función:** src/utils/data_utils.py - obtener_ips_criticas()
* **Prompt Enviado**  "Necesito probar que obtener_ips_criticas() no devuelva direcciones IP duplicadas cuando una misma IP aparece en varios eventos con severidad CRITICAL. También quiero comprobar que los eventos no críticos sean excluidos del resultado."
* **Respuesta de la IA:** La IA propuso una prueba aislada con cuatro eventos: dos eventos críticos asociados a la misma IP, otro evento crítico con una IP diferente y un evento INFO. Se utilizaron aserciones para verificar el conjunto esperado y su cantidad de elementos.
* **Análisis Crítico:** La prueba se ejecutó correctamente. La función devolvió las dos IP críticas únicas, ignoró la IP con severidad INFO y no duplicó la dirección que aparecía en dos eventos críticos. Ambas aserciones se cumplieron.
* **Solución Final:** Se validó el comportamiento de obtener_ips_criticas() ante IP repetidas mediante una prueba aislada. No fue necesario modificar el código fuente porque la implementación existente satisface los requisitos de esta prueba.

## Registro de Prompt #17

* **Fecha:** 2026-10-09
* **Módulo/Función:** src/utils/data_utils.py - obtener_ips_unicas()
* **Prompt Enviado**  "Necesito comprobar el comportamiento de obtener_ips_unicas() cuando recibe una lista que contiene un registro sin la clave ip. Quiero identificar qué excepción genera la implementación actual sin modificar el código."
* **Respuesta de la IA:** La IA propuso una prueba aislada con cinco registros que contienen tres direcciones IP diferentes y distintos códigos HTTP. Se utilizaron aserciones para verificar el conjunto esperado y la cantidad de IP únicas.
* **Análisis Crítico:** La prueba se ejecutó correctamente. La función devolvió las tres direcciones IP esperadas, eliminó las repeticiones y no dependió del código HTTP de los registros. Ambas aserciones se cumplieron.
* **Solución Final:** Se validó el comportamiento de obtener_ips_unicas() mediante una prueba aislada. No fue necesario modificar el código fuente porque la implementación existente satisface los requisitos de esta prueba.

## Registro de Prompt #18

* **Fecha:** 2026-10-09
* **Módulo/Función:** src/utils/data_utils.py - obtener_ips_unicas()
* **Prompt Enviado**  "Necesito probar que obtener_ips_unicas() identifique correctamente las direcciones IP distintas de varios registros, incluso cuando algunas se repiten y los registros tienen diferentes códigos HTTP."
* **Respuesta de la IA:** La IA propuso ejecutar una prueba aislada con tres registros, uno de ellos sin la clave ip, y utilizar un bloque try/except para capturar y mostrar la excepción.
* **Análisis Crítico:** La prueba generó un KeyError con el mensaje 'ip'. Esto confirma que la función espera que cada registro contenga la clave requerida. El resultado coincide con la implementación actual y no demuestra por sí solo que exista un defecto, ya que depende del contrato definido para la función.
* **Solución Final:** Se comprobó el comportamiento de la función ante un registro incompleto. No se modificó el código fuente; queda pendiente determinar si el sistema debe rechazar, informar o ignorar registros que no contienen la clave ip.

## Registro de Prompt #19

* **Fecha:** 2026-10-09
* **Módulo/Función:** src/parsers/csv_parser.py - leer_logs_csv()
* **Prompt Enviado**  "Necesito comprobar qué ocurre cuando leer_logs_csv() recibe una ruta de archivo CSV inexistente. Quiero verificar si Python genera FileNotFoundError y capturar la excepción durante una prueba aislada, sin modificar el código fuente."
* **Respuesta de la IA:** La IA propuso ejecutar la función con una ruta inexistente y utilizar un bloque try/except para capturar FileNotFoundError y mostrar la ruta del archivo solicitado.
* **Análisis Crítico:** La prueba generó FileNotFoundError, y el bloque except capturó correctamente la excepción. El resultado confirmó que la función propaga el error cuando el archivo no existe. La captura se realizó en el código de prueba, no dentro de la función original.
* **Solución Final:** Se verificó el comportamiento de leer_logs_csv() ante una ruta inexistente. No se modificó la implementación; queda pendiente decidir si la aplicación debe manejar esta excepción para proporcionar mensajes de error más claros al usuario.

## Registro de Prompt #20

* **Fecha:** 2026-10-09
* **Módulo/Función:** src/parsers/json_parser.py - leer_eventos_json()
* **Prompt Enviado**  "Necesito comprobar el comportamiento de leer_eventos_json() cuando recibe un archivo JSON con sintaxis incorrecta. Quiero verificar que genere JSONDecodeError, capturar el mensaje y la ubicación del error y eliminar el archivo temporal al finalizar, sin modificar el código fuente."
* **Respuesta de la IA:** La IA propuso crear un archivo temporal con contenido JSON inválido, intentar leerlo mediante leer_eventos_json(), capturar json.JSONDecodeError y mostrar el mensaje, la línea y la columna del error. También se utilizó un bloque finally para eliminar el archivo temporal.
* **Análisis Crítico:** La prueba generó JSONDecodeError con el mensaje "Expecting ',' delimiter", en la línea 1, columna 19. La excepción se capturó correctamente y el archivo temporal se eliminó. Se confirmó que la función original propaga el error de análisis JSON.
* **Solución Final:** Se verificó el comportamiento de leer_eventos_json() ante un archivo JSON mal formado. No fue necesario modificar el código fuente; queda pendiente decidir si la aplicación debe capturar esta excepción para proporcionar mensajes de error más claros.

## Registro de Prompt #21

* **Fecha:** 2026-10-09
* **Módulo/Función:** src/services/metrics_service.py - calcular_porcentaje_http_500()
* **Prompt Enviado**  "Necesito comprobar que calcular_porcentaje_http_500() maneje correctamente una lista vacía, evitando la división por cero y devolviendo el resultado numérico esperado."
* **Respuesta de la IA:** La IA propuso ejecutar una prueba aislada con una lista vacía, mostrar el porcentaje calculado y el tipo de dato devuelto, y utilizar aserciones para verificar que el resultado fuera 0.0 y de tipo float.
* **Análisis Crítico:** La prueba se ejecutó correctamente. La función devolvió 0.0, de tipo float, y ambas aserciones se cumplieron. Esto confirmó que la implementación contempla el caso en el que no existen registros.
* **Solución Final:** Se verificó el comportamiento de calcular_porcentaje_http_500() con una lista vacía. No fue necesario modificar el código fuente, ya que la función evita la división por cero y devuelve el valor definido para este caso.

## Registro de Prompt #22

* **Fecha:** 2026-10-09
* **Módulo/Función:** src/services/metrics_service.py - calcular_porcentaje_http_500()
* **Prompt Enviado**  "Necesito comprobar que calcular_porcentaje_http_500() calcule correctamente el porcentaje cuando recibe registros válidos, pero ninguno tiene estado HTTP 500. Quiero verificar que el resultado sea 0.0 sin que la lista esté vacía."
* **Respuesta de la IA:** La IA propuso una prueba aislada con tres registros que tienen estados HTTP 200, 404 y 201. Se calculó el porcentaje de errores HTTP 500 y se utilizó una aserción para verificar que el resultado fuera 0.0.
* **Análisis Crítico:** La prueba se ejecutó correctamente. La función procesó los tres registros, identificó cero errores HTTP 500 y devolvió 0.0. La aserción se cumplió, confirmando el cálculo para una lista no vacía sin errores 500.
* **Solución Final:** Se verificó el cálculo del porcentaje HTTP 500 cuando existen registros válidos, pero ninguno tiene estado 500. No fue necesario modificar el código fuente porque la implementación produjo el resultado esperado.

## Registro de Prompt #23

* **Fecha:** 2026-10-09
* **Módulo/Función:** src/services/metrics_service.py - calcular_porcentaje_http_500()
* **Prompt Enviado**  "Necesito comprobar que calcular_porcentaje_http_500() calcule correctamente el porcentaje de errores cuando recibe una combinación de estados HTTP 500 y otros códigos. Quiero verificar tanto la cantidad de errores como el porcentaje final."
* **Respuesta de la IA:** La IA propuso una prueba aislada con cuatro registros, dos con estado HTTP 500, uno con estado 200 y otro con estado 404. Se calcularon la cantidad de errores y el porcentaje, y se utilizaron aserciones para verificar ambos resultados.
* **Análisis Crítico:** La prueba se ejecutó correctamente. De los cuatro registros, dos tenían estado HTTP 500. La función devolvió 50.0, y ambas aserciones se cumplieron. El resultado confirmó que el porcentaje se calcula correctamente con estados HTTP mixtos.
* **Solución Final:** Se validó el cálculo del porcentaje HTTP 500 para una lista con distintos estados. No fue necesario modificar el código fuente porque la función identificó correctamente los errores y devolvió el porcentaje esperado.

## Registro de Prompt #24

* **Fecha:** 2026-10-09
* **Módulo/Función:** src/utils/data_utils.py - obtener_ips_unicas()
* **Prompt Enviado**  "Necesito comprobar que obtener_ips_unicas() maneje correctamente una lista vacía y devuelva un conjunto vacío de tipo set, sin generar excepciones."
* **Respuesta de la IA:** La IA propuso una prueba aislada con una lista vacía, mostrando la cantidad de registros, el resultado y su tipo de dato. Se utilizaron dos aserciones para verificar que el resultado fuera un conjunto vacío y que perteneciera al tipo set.
* **Análisis Crítico:** La prueba se ejecutó correctamente. La función devolvió set(), el tipo del resultado fue set y ambas aserciones se cumplieron. Se confirmó que la implementación maneja correctamente una entrada sin registros.
* **Solución Final:** Se verificó el comportamiento de obtener_ips_unicas() con una lista vacía. No fue necesario modificar el código fuente porque la función devolvió el resultado esperado y conservó el tipo de dato adecuado.

## Registro de Prompt #25

* **Fecha:** 2026-10-09
* **Módulo/Función:** Pruebas automatizadas de src/test_csv.py y validación de calcular_porcentaje_http_500() y leer_logs_csv().
* **Prompt Enviado**  "Ejecutar la suite de pytest, revisar por qué no se detectan pruebas automatizadas y convertir las comprobaciones existentes del módulo CSV en pruebas que pytest pueda descubrir."
* **Respuesta de la IA:** Se propuso reemplazar el contenido de src/test_csv.py por tres funciones de prueba: cálculo del porcentaje HTTP 500 con cuatro registros, cálculo con una lista vacía y lectura del CSV comprobando la cantidad de registros y el tipo entero de los estados HTTP.
* **Análisis Crítico:** La propuesta permite pasar de comprobaciones manuales mediante impresiones a pruebas automatizadas con pytest. Las pruebas utilizan assert para comparar resultados esperados y comprobar propiedades de los datos. Sin embargo, solo cubren algunos comportamientos del módulo CSV y no garantizan la ausencia de errores en todo el sistema.
* **Solución Final:** Se implementaron las tres pruebas en src/test_csv.py. La ejecución de python -m pytest -v recopiló tres pruebas y todas finalizaron correctamente: 3 passed in 1.39s.

## Registro de Prompt #26

* **Fecha:** 2026-10-09
* **Módulo/Función:** Pruebas automatizadas de src/test_json.py y validación de leer_eventos_json().
* **Prompt Enviado**  "Revisar el archivo de pruebas del módulo JSON y convertir las comprobaciones manuales en pruebas automatizadas que permitan verificar la lectura de eventos, la estructura de los datos y el manejo de una lista JSON vacía."
* **Respuesta de la IA:** Se propusieron tres pruebas automatizadas: verificar que el archivo contiene seis eventos y devuelve una lista, comprobar que el primer evento contiene las claves ip, event y severity, y validar la lectura de una lista JSON vacía mediante un archivo temporal creado con tmp_path.
* **Análisis Crítico:** Las pruebas permiten verificar comportamientos normales del lector JSON y un caso límite válido. El uso de tmp_path evita modificar los archivos reales del proyecto. Sin embargo, todavía no se comprueba el comportamiento ante archivos inexistentes o JSON mal formado mediante la suite automatizada.
* **Solución Final:** Se actualizaron las pruebas en src/test_json.py. Al ejecutar python -m pytest -v, se recopilaron seis pruebas entre los módulos CSV y JSON, y todas finalizaron correctamente: 6 passed in 2.06s.

## Registro de Prompt #27

* **Fecha:** 2026-10-09
* **Módulo/Función:** Pruebas automatizadas de src/test_utils.py: obtener_ips_unicas(), crear_resumen_evento() y obtener_ips_criticas().
* **Prompt Enviado**  "Revisar las comprobaciones manuales del módulo de utilidades y convertirlas en pruebas automatizadas con pytest para verificar la eliminación de IP duplicadas, la creación de tuplas, la identificación de IP críticas, los casos con listas vacías y el uso de los eventos reales."
* **Respuesta de la IA:** Se propusieron seis pruebas automatizadas que comprueban las tres funciones de utilidades con datos controlados y con el archivo data/events.json.
* **Análisis Crítico:** Las pruebas verifican resultados concretos y casos límite. El uso de conjuntos permite comprobar que no se repitan las IP, mientras que isinstance() permite verificar el tipo de dato retornado. La prueba con eventos reales depende de la estructura y el contenido actual de data/events.json; por ello, si esos datos cambian, algunas expectativas también podrían necesitar actualizarse.
* **Solución Final:** Se reemplazaron las comprobaciones manuales de src/test_utils.py por seis pruebas automatizadas. La ejecución de python -m pytest -v recopiló doce pruebas en los módulos CSV, JSON y utilidades. Todas finalizaron correctamente: 12 passed in 1.62s.

## Registro de Prompt #28

* **Fecha:** 2026-10-09
* **Módulo/Función:** Pruebas automatizadas de src/test_geolocation.py, para obtener_geolocalizacion() y enriquecer_ips_con_geolocalizacion().
* **Prompt Enviado**  "Revisar el servicio de geolocalización y convertir las comprobaciones manuales en pruebas automatizadas que simulen respuestas exitosas, IP no encontrada, errores HTTP, tiempos de espera y enriquecimiento de varias IP, sin depender de la API real."
* **Respuesta de la IA:** Se propusieron cinco pruebas con unittest.mock, Mock y patch para simular las respuestas HTTP y las excepciones de la biblioteca requests.
* **Análisis Crítico:** Los mocks permiten comprobar el comportamiento del servicio sin depender de Internet. Las pruebas cubren respuestas exitosas, fallos reportados por la API, errores HTTP y tiempos de espera. Sin embargo, aún faltan pruebas para otras excepciones de conexión y no se comprueba todavía la generación de reportes.
* **Solución Final:** Se actualizaron las pruebas de src/test_geolocation.py. La ejecución de python -m pytest -v recopiló 17 pruebas entre los módulos CSV, JSON, utilidades y geolocalización. Todas finalizaron correctamente: 17 passed in 1.13s.

## Registro de Prompt #29

* **Fecha:** 2026-10-09
* **Módulo/Función:** Pruebas automatizadas de src/test_report.py: construir_resumen() y guardar_reporte_json().
* **Prompt Enviado**  "Revisar las comprobaciones manuales del módulo de reportes y convertirlas en pruebas automatizadas que verifiquen la construcción del resumen, la persistencia del reporte JSON y la conservación de caracteres Unicode, evitando modificar el archivo real del proyecto."
* **Respuesta de la IA:** Se propusieron tres pruebas automatizadas con pytest: comprobar la estructura del resumen, verificar que el reporte guardado pueda leerse y coincida con los datos originales, y validar la conservación de texto Unicode. Se utilizó tmp_path para crear archivos temporales.
* **Análisis Crítico:** Las pruebas verifican la estructura del reporte, su persistencia y la conservación de caracteres especiales. El uso de archivos temporales evita sobrescribir data/report.json. Sin embargo, todavía no se han cubierto todos los posibles errores de escritura ni los casos de entradas inválidas.
* **Solución Final:** Se actualizaron las pruebas de src/test_report.py. La ejecución de python -m pytest -v recopiló veinte pruebas de los módulos CSV, JSON, utilidades, geolocalización y reportes. Todas finalizaron correctamente: 20 passed in 0.10s.

## Registro de Prompt #30

* **Fecha:** 2026-10-09
* **Módulo/Función:** Integración principal del proyecto — src/main.py
* **Prompt Enviado**  "Ayúdame a integrar los módulos desarrollados de TI-Metrics en main.py, de manera que el programa lea los archivos CSV y JSON, calcule el porcentaje de errores HTTP 500, identifique las IP críticas, consulte la geolocalización y guarde un reporte JSON. Explícame los cambios paso a paso y cómo verificar que la integración funcione."
* **Respuesta de la IA:** Se propuso una función main() que coordina los analizadores CSV y JSON, los servicios de métricas y geolocalización, las utilidades de procesamiento de datos y el servicio de generación de reportes. También se indicaron comandos para ejecutar el programa, validar el reporte JSON y correr la suite de pruebas con pytest -v.
* **Análisis Crítico:** La propuesta permite centralizar la ejecución del sistema sin duplicar la lógica implementada en los módulos existentes. Se verificó que el programa calcula un 30.0 % de errores HTTP 500, identifica dos IP críticas y genera data/report.json. La salida del reporte también mostró que 192.168.1.10 no tiene geolocalización pública disponible. Aunque la API devolvió coordenadas para 203.0.113.25, esta IP pertenece al bloque TEST-NET-3 reservado para documentación, por lo que esos datos no representan una ubicación real. Finalmente, las 20 pruebas automatizadas pasaron correctamente.
* **Solución Final:** Se integraron los módulos existentes en src/main.py y se ejecutó python src/main.py. Se verificó el contenido y la validez de data/report.json mediante python -m json.tool data/report.json. Después se ejecutó pytest -v, obteniendo 20 pruebas aprobadas y 0 fallidas. La integración quedó verificada para los datos y escenarios probados.

## Registro de Prompt #31

* **Fecha:** 2026-10-10
* **Módulo/Función:** Revisión de calidad y cobertura de pruebas — proyecto TI-Metrics.
* **Prompt Enviado**  "Continuemos con el proyecto TI-Metrics después de integrar el flujo principal, publicar el commit 22f4d70 y confirmar que las 20 pruebas automatizadas pasan."
* **Respuesta de la IA:** Se propuso iniciar una revisión de calidad mediante el análisis de cobertura de pruebas con pytest-cov, antes de decidir qué módulos necesitan refactorización o pruebas adicionales.
* **Análisis Crítico:** Tener pruebas aprobadas demuestra que los casos implementados funcionan, pero no garantiza que todas las líneas y ramas relevantes estén cubiertas. Primero se deben medir los resultados y comprobar si la herramienta está disponible en el entorno virtual.
* **Solución Final:** Ejecutar python -m pytest --cov=src --cov-report=term-missing, analizar los porcentajes y las líneas no cubiertas, y priorizar las mejoras según los resultados obtenidos, manteniendo como referencia una cobertura mínima del 80 %.

## Registro de Prompt #32

* **Fecha:** 2026-10-10
* **Módulo/Función:** Análisis de cobertura de pruebas y planificación de pruebas de integración — src/main.py.
* **Prompt Enviado**  "Interpretar el informe de cobertura de TI-Metrics, identificar los módulos que necesitan pruebas adicionales y continuar el proyecto paso a paso."
* **Respuesta de la IA:** Se analizó el resultado de 20 pruebas aprobadas y una cobertura total del 89 %. Se identificó que src/main.py tiene un 0 % de cobertura y que src/services/geolocation_service.py tiene un 90 %. Se priorizó revisar la integración principal antes de añadir nuevas pruebas.
* **Análisis Crítico:** Una cobertura alta no garantiza por sí sola la ausencia de errores. La función principal debe probarse sin depender de llamadas de red reales ni de cambios en los archivos de datos.
* **Solución Final:** Inspeccionar src/main.py, diseñar pruebas de integración con dependencias simuladas y ejecutar nuevamente la suite para verificar que el comportamiento existente se conserva y mejora la cobertura.

## Registro de Prompt #33

* **Fecha:** 2026-10-10
* **Módulo/Función:** Pruebas de integración de main.py y manejo de errores de geolocalización.
* **Prompt Enviado**  "Diseñar pruebas con mocks para aumentar la cobertura de src/main.py y comprobar el manejo de errores de conexión en src/services/geolocation_service.py."
* **Respuesta de la IA:** Se propuso crear src/test_main.py para verificar la coordinación de los módulos y añadir test_obtener_geolocalizacion_error_conexion() para simular requests.exceptions.ConnectionError.
* **Análisis Crítico:** Las pruebas permiten verificar el comportamiento sin depender de llamadas reales a la API. La cobertura llegó al 99 %; main.py mantiene una línea sin ejecutar porque la prueba llama directamente a la función y no ejecuta el archivo como programa.
* **Solución Final:** Se añadieron las pruebas de integración y de error de conexión. La suite completa terminó con 22 pruebas aprobadas, cobertura global del 99 % y cobertura del 100 % en geolocation_service.py. No fue necesario modificar la implementación del servicio.

## Registro de Prompt #34

* **Fecha:** 2026-10-10
* **Módulo/Función:** Auditoría general de TI-Metrics — Hito 1.
* **Prompt Enviado**  "Revisar el proyecto TI-Metrics completo y compararlo con los requisitos del Hito 1, considerando que el avance se presentará el 21 de octubre y que no se debe adelantar el Hito 2."
* **Respuesta de la IA:** Se revisaron los módulos de lectura CSV/JSON, procesamiento de datos, métricas, consumo de API REST, generación de reportes, pruebas y documentación. Se identificó que el flujo principal está implementado y que conviene revisar el manejo de excepciones de archivos y la deduplicación de eventos.
* **Análisis Crítico:** La existencia de pruebas automatizadas y una cobertura elevada no garantiza por sí sola el cumplimiento completo de la consigna. Es necesario contrastar las funcionalidades con la rúbrica y evitar refactorizaciones de POO que pertenecen al Hito 2.
* **Solución Final:** Se realizó una auditoría sin modificar el código. Se decidió conservar la arquitectura actual y priorizar únicamente las verificaciones y correcciones necesarias para el Hito 1.

## Registro de Prompt #35

* **Fecha:** 2026-10-10
* **Módulo/Función:** Manejo de excepciones, deduplicación de eventos y pruebas automatizadas — Hito 1.
* **Prompt Enviado**  "Ayúdame a completar los requisitos pendientes del Hito 1 de TI-Metrics. Necesito mejorar el manejo de excepciones en los lectores CSV y JSON, implementar la deduplicación de eventos mediante conjuntos (set), integrar la función en main.py y comprobar que el sistema continúa funcionando mediante pruebas automatizadas."
* **Respuesta de la IA:** Se propuso incorporar bloques try/except en csv_parser.py y json_parser.py para controlar archivos inexistentes, problemas de permisos y datos inválidos. Se implementó deduplicar_eventos() en data_utils.py, utilizando un conjunto de identificadores construidos mediante tuplas. También se recomendó integrar esta función en main.py antes de identificar las IPs críticas y ampliar las pruebas con pytest.
* **Análisis Crítico:** Se decidió conservar las excepciones en lugar de devolver listas vacías cuando falla la lectura, para evitar generar métricas incorrectas. La deduplicación compara eventos completos y no solamente sus direcciones IP, porque una misma IP puede generar diferentes eventos legítimos. Se comprobó que los seis eventos del archivo original son únicos. La implementación de deduplicación es adecuada para los datos actuales, cuyos valores son simples; si se incorporan estructuras anidadas, será necesario adaptar la construcción del identificador. Las pruebas permiten comprobar los casos normales y las situaciones de error sin modificar los archivos originales.
* **Solución Final:** Se actualizaron los lectores CSV y JSON, se añadió deduplicar_eventos() y se integró su ejecución en main.py. Se incorporaron nueve pruebas nuevas, alcanzando 31 pruebas aprobadas, cero fallidas y 99 % de cobertura global. Finalmente, se ejecutó python src/main.py, obteniendo un porcentaje de errores HTTP 500 del 30.0 %, dos IPs críticas y la generación correcta de data/report.json.


## Registro de Prompt #36

* **Fecha:** 2026-11-02
* **Módulo/Función:** Implementación de la clase abstracta BaseLogParser, encapsulamiento y validación de atributos — Hito 2.
* **Prompt Enviado:** "Ayúdame a iniciar la refactorización orientada a objetos del Hito 2 de TI-Metrics. Necesito crear una clase base abstracta para los lectores CSV y JSON, implementar un constructor que valide la ruta del archivo, aplicar encapsulamiento mediante @property y definir un método abstracto leer() que deban implementar las clases hijas."
* **Respuesta de la IA:** Se propuso crear el paquete src/models y desarrollar la clase BaseLogParser en base_log_parser.py utilizando ABC y abstractmethod del módulo abc. Se implementó el constructor __init__ para validar que la ruta sea una cadena de texto no vacía, el atributo protegido _ruta_archivo para almacenar su valor y la propiedad ruta_archivo mediante el decorador @property para permitir su consulta sin modificación directa. También se definió el método abstracto leer(), estableciendo un contrato común para los lectores de archivos CSV y JSON.
* **Análisis Crítico:** Se revisó la implementación para comprobar que cumpliera los principios de abstracción, herencia y encapsulamiento. Durante las pruebas se identificó un problema al utilizar self.ruta_archivo = ruta_archivo dentro del constructor, debido a que la propiedad no tenía un setter definido. Se corrigió la asignación mediante self._ruta_archivo = ruta_archivo, conservando la propiedad pública de solo lectura. También se verificó que la clase abstracta no pudiera instanciarse directamente y que el constructor rechazara rutas vacías o valores de tipos incorrectos. Se decidió mantener una única clase base para evitar duplicar la validación de atributos en los lectores especializados.
* **Solución Final:** Se creó el paquete src/models con los archivos __init__.py y base_log_parser.py. Se implementó BaseLogParser como clase abstracta con validación de la ruta del archivo, encapsulamiento mediante @property y el método abstracto leer(). La clase quedó preparada para ser heredada por CSVLogParser y JSONLogParser. Posteriormente, se ejecutó la suite completa de pruebas del proyecto mediante python -m pytest src/ -v, obteniendo 31 pruebas aprobadas y cero fallidas.


## Registro de Prompt #37

* **Fecha:** 2026-11-02
* **Módulo/Función:** Refactorización del lector CSV mediante herencia, polimorfismo y compatibilidad con el Hito 1 — Hito 2.
* **Prompt Enviado:** "Ayúdame a refactorizar el módulo csv_parser.py del proyecto TI-Metrics utilizando programación orientada a objetos. Necesito crear una clase CSVLogParser que herede de BaseLogParser, implementar el método leer(), conservar las validaciones y excepciones existentes y mantener la función leer_logs_csv() para que las pruebas y los demás módulos del Hito 1 continúen funcionando."
* **Respuesta de la IA:** Se propuso modificar src/parsers/csv_parser.py para incorporar la clase CSVLogParser, heredada de BaseLogParser. Se implementó el método leer() utilizando csv.DictReader para procesar los registros del archivo CSV y convertir los campos status y response_time a valores enteros. Se conservaron las excepciones para archivos inexistentes, problemas de permisos y datos inválidos, incluyendo el número de fila cuando ocurre un error de conversión. También se mantuvo la función leer_logs_csv() como mecanismo de compatibilidad, encargada de crear una instancia de CSVLogParser y ejecutar su método leer().
* **Análisis Crítico:** Se decidió conservar el comportamiento del lector original para evitar afectar los módulos y pruebas desarrollados durante el Hito 1. La conversión de status y response_time a enteros se mantuvo sin modificaciones, respetando los tipos de datos utilizados anteriormente. Durante la implementación se identificaron y corrigieron errores relacionados con la asignación del atributo protegido en BaseLogParser, el manejo de FileNotFoundError y la conservación de la función leer_logs_csv(). Se comprobó que CSVLogParser implementa el método abstracto leer() definido por la clase base, lo que permite utilizar una interfaz común con otros lectores. La compatibilidad se verificó mediante las pruebas automatizadas existentes.
* **Solución Final:** Se refactorizó src/parsers/csv_parser.py incorporando la clase CSVLogParser, que hereda de BaseLogParser e implementa su propio método leer(). Se conservaron las validaciones, las excepciones y la función leer_logs_csv() para mantener la compatibilidad con el Hito 1. Se ejecutó python -m pytest src/test_csv.py -v, obteniendo seis pruebas aprobadas y cero fallidas. Posteriormente, se ejecutó python -m pytest src/ -v, confirmando que las 31 pruebas del proyecto continuaban aprobándose sin errores.


## Registro de Prompt #38

* **Fecha:** 2026-11-02
* **Módulo/Función:** Refactorización del lector JSON mediante herencia, sobrescritura de métodos y manejo de excepciones — Hito 2.
* **Prompt Enviado:** "Ayúdame a refactorizar el módulo json_parser.py del proyecto TI-Metrics utilizando programación orientada a objetos. Necesito implementar una clase JSONLogParser que herede de BaseLogParser, sobrescribir el método leer(), conservar el manejo de excepciones y mantener la función leer_eventos_json() para garantizar la compatibilidad con los módulos y pruebas del Hito 1."
* **Respuesta de la IA:** Se propuso modificar src/parsers/json_parser.py para incorporar la clase JSONLogParser, heredada de BaseLogParser. Se implementó el método leer() utilizando json.load() para cargar los eventos almacenados en archivos JSON. Se conservaron las excepciones FileNotFoundError y PermissionError, además del manejo de json.JSONDecodeError, que se transforma en ValueError para informar sobre contenido JSON inválido. También se mantuvo la función leer_eventos_json(), encargada de crear una instancia de JSONLogParser y ejecutar su método leer(), conservando la interfaz utilizada durante el Hito 1.
* **Análisis Crítico:** Se decidió conservar el comportamiento original del lector JSON para evitar modificaciones innecesarias en los módulos existentes. Durante la primera ejecución de las pruebas automatizadas se obtuvieron tres pruebas aprobadas y tres fallidas. Los errores indicaban que la función devolvía None en lugar de una lista de eventos. Al revisar la implementación se identificó que faltaba la instrucción return eventos al finalizar el método leer(). Se corrigió este problema y se ejecutaron nuevamente las pruebas. La segunda ejecución confirmó que el método devolvía correctamente tanto los eventos del archivo original como las listas vacías. También se comprobó que las excepciones continuaban funcionando correctamente ante archivos inexistentes, contenido inválido y archivos vacíos.
* **Solución Final:** Se refactorizó src/parsers/json_parser.py incorporando la clase JSONLogParser, que hereda de BaseLogParser e implementa su propio método leer(). Se conservaron el manejo de excepciones y la función leer_eventos_json() para garantizar la compatibilidad con el Hito 1. Después de corregir la ausencia de return eventos, se ejecutó python -m pytest src/test_json.py -v, obteniendo seis pruebas aprobadas y cero fallidas. Finalmente, se ejecutó python -m pytest src/ -v, confirmando que las 31 pruebas del proyecto continuaban aprobándose correctamente, con cero fallidas y un tiempo de ejecución de 0.25 segundos.


## Registro de Prompt #39

* **Fecha:** 2026-11-02
* **Módulo/Función:** Pruebas automatizadas de abstracción, herencia, polimorfismo, encapsulamiento y validación de atributos — Hito 2.
* **Prompt Enviado:** "Ayúdame a desarrollar pruebas automatizadas para comprobar que las clases BaseLogParser, CSVLogParser y JSONLogParser cumplen los principios de programación orientada a objetos. Necesito verificar la abstracción, la herencia, el polimorfismo, el encapsulamiento mediante @property y las validaciones del constructor, utilizando pytest y conservando las pruebas existentes del proyecto TI-Metrics."
* **Respuesta de la IA:** Se propuso crear el archivo src/test_poo_parsers.py e implementar cinco pruebas automatizadas. La primera comprueba que BaseLogParser no puede instanciarse directamente porque contiene un método abstracto. La segunda utiliza issubclass() para verificar que CSVLogParser y JSONLogParser heredan de BaseLogParser. La tercera demuestra el polimorfismo mediante una lista de objetos de ambas clases y la ejecución del método leer(), comprobando que se obtienen diez registros CSV y seis eventos JSON. La cuarta verifica que la propiedad ruta_archivo permite consultar su valor, pero rechaza modificaciones directas mediante AttributeError. La quinta comprueba que el constructor rechaza rutas de tipos incorrectos, cadenas vacías y cadenas que contienen únicamente espacios, utilizando TypeError y ValueError.
* **Análisis Crítico:** Se decidió crear un archivo independiente para las pruebas de programación orientada a objetos, evitando mezclar las comprobaciones de diseño con las pruebas funcionales existentes de los lectores CSV y JSON. Durante la implementación de la prueba de encapsulamiento se produjo un AssertionError porque la última comparación esperaba incorrectamente la ruta data/logs.csv.csv en lugar de data/logs.csv. Se revisó el resultado y se identificó que el problema correspondía al valor esperado en la prueba, no al comportamiento de la propiedad. Se corrigió la comparación y se ejecutaron nuevamente las pruebas, obteniendo cuatro pruebas aprobadas. Posteriormente, se añadió una quinta prueba para comprobar las validaciones heredadas del constructor. Se verificó que los cinco casos de prueba se ejecutaran satisfactoriamente y que las clases reutilizaran correctamente los mecanismos definidos en BaseLogParser. Estas pruebas verifican comportamientos específicos de la implementación, pero no garantizan la ausencia de todos los posibles defectos.
* **Solución Final:** Se creó el archivo src/test_poo_parsers.py con cinco pruebas automatizadas que verifican abstracción, herencia, polimorfismo, encapsulamiento y validación de atributos. Se ejecutó python -m pytest src/test_poo_parsers.py -v, obteniendo cinco pruebas aprobadas y cero fallidas. Finalmente, se ejecutó python -m pytest src/ -v para comprobar la compatibilidad con el resto del proyecto. El resultado fue de 36 pruebas aprobadas, cero fallidas y un tiempo de ejecución de 0.23 segundos, conservando las 31 pruebas anteriores del Hito 1 e incorporando cinco pruebas nuevas del Hito 2.


## Registro de Prompt #40

* **Fecha:** 2026-11-02
* **Módulo/Función:** Refactorización orientada a objetos del servicio de métricas y pruebas automatizadas — Hito 2.
* **Prompt Enviado:** "Ayúdame a revisar y refactorizar el módulo metrics_service.py del proyecto TI-Metrics para implementar una clase MetricsService que utilice encapsulamiento mediante @property, conserve el cálculo del porcentaje de errores HTTP 500 y mantenga la compatibilidad con las funciones y pruebas del Hito 1. También necesito crear pruebas automatizadas con pytest y corregir los errores que aparezcan durante la implementación."
* **Respuesta de la IA:** Se propuso implementar una clase MetricsService con un constructor que recibe y valida una lista de registros, un atributo protegido _registros, una propiedad registros de solo lectura y un método calcular_porcentaje_http_500(). También se recomendó conservar la función procedural original como interfaz de compatibilidad, delegando el cálculo a la nueva clase. Posteriormente, se propuso crear el archivo src/test_metrics_service.py con seis pruebas para verificar el cálculo de porcentajes, el comportamiento con listas vacías, la validación de tipos, el encapsulamiento y la protección de la estructura de las listas mediante copias superficiales.
* **Análisis Crítico:** Antes de modificar el servicio, se revisaron sus dependencias en main.py, test_main.py y test_csv.py para evitar incompatibilidades. Durante la primera ejecución de las seis pruebas existentes de CSV, cuatro aprobaron y dos fallaron debido a un AttributeError. El error se produjo porque el constructor intentaba asignar un valor a self.registros, una propiedad definida con @property sin setter. Se identificó que el atributo interno correcto era self._registros y se corrigió la asignación. Después de esta modificación, las seis pruebas de test_csv.py aprobaron. Se comprobó también que el uso de list.copy() genera copias superficiales, por lo que protege la estructura de la lista, pero no impide modificar directamente los diccionarios contenidos en ella. Esta limitación deberá considerarse si se requiere un encapsulamiento más estricto.
* **Solución Final:** Se refactorizó src/services/metrics_service.py mediante la clase MetricsService, manteniendo la función calcular_porcentaje_http_500(registros) para conservar la compatibilidad con el Hito 1. Se creó src/test_metrics_service.py con seis pruebas automatizadas, todas aprobadas. Finalmente, se ejecutó python -m pytest src/ -v y se obtuvieron 42 pruebas aprobadas, cero fallidas y un tiempo total de 0.12 segundos. Se confirmó que los módulos existentes continúan superando sus pruebas después de la refactorización.


## Registro de Prompt #41

* **Fecha:** 2026-11-02
* **Módulo/Función:** `src/services/geolocation_service.py` y `src/test_geolocation_service.py` — Refactorización orientada a objetos del servicio de geolocalización.
* **Prompt Enviado:** "Necesito continuar la refactorización del Hito 2 de TI-Metrics. Analiza el servicio de geolocalización y sus pruebas existentes para implementar una clase GeolocationService con encapsulamiento, propiedades @property y validación de parámetros, conservando la compatibilidad con las funciones del Hito 1."
* **Respuesta de la IA:** Se propuso implementar la clase `GeolocationService` con atributos protegidos `_url_base` y `_timeout`, propiedades de solo lectura y métodos para consultar y enriquecer direcciones IP. Se conservaron las funciones originales como interfaces de compatibilidad. También se proporcionaron pruebas unitarias utilizando `pytest` y `unittest.mock`.
* **Análisis Crítico:** Durante las primeras ejecuciones se detectaron errores de escritura en la URL de la API y en el nombre `requests.exceptions`. Las pruebas permitieron identificar estos problemas mediante mensajes de error y comprobar las correcciones. Se verificó que las solicitudes HTTP continuaran siendo simuladas durante las pruebas. Se mantuvo la URL HTTP original por compatibilidad, reconociendo que no proporciona cifrado.
* **Solución Final:** Se implementó `GeolocationService` con configuración validada, encapsulamiento y métodos de instancia. Se conservaron las funciones del Hito 1 y se añadieron 13 pruebas nuevas. Las 6 pruebas originales de geolocalización aprobaron y la suite completa del proyecto finalizó con 55 pruebas aprobadas y ningún fallo.



## Registro de Prompt #42

* **Fecha:** 2026-11-02
* **Módulo/Función:** `src/services/report_service.py` y `src/test_report_service.py` — Refactorización orientada a objetos del servicio de reportes.
* **Prompt Enviado:** "Necesito continuar la refactorización del Hito 2 de TI-Metrics. Analiza el servicio de reportes y sus pruebas existentes para implementar una clase ReportService con encapsulamiento, propiedades @property y validación de parámetros, conservando la compatibilidad con las funciones del Hito 1."
* **Respuesta de la IA:** Se propuso implementar la clase `ReportService` con el atributo protegido `_indentacion`, una propiedad de solo lectura y métodos para construir resúmenes y guardar archivos JSON. Se conservaron las funciones originales como interfaces de compatibilidad y se proporcionaron pruebas unitarias con `pytest`.
* **Análisis Crítico:** Durante la primera ejecución de las pruebas se detectó que el método `guardar_reporte_json()` contenía únicamente la instrucción `pass`, por lo que no generaba archivos. Se revisó el código y se reemplazó dicha instrucción por la implementación de escritura mediante `json.dump()`. Las pruebas confirmaron que los reportes se guardan correctamente, conservando los caracteres Unicode y permitiendo configurar la indentación.
* **Solución Final:** Se implementó `ReportService` con encapsulamiento, validación del constructor, propiedad `@property` y métodos de instancia. Se mantuvieron las funciones originales para conservar la compatibilidad con el Hito 1. Se añadieron 11 pruebas nuevas, las 3 pruebas originales de reportes aprobaron y la suite completa de TI-Metrics finalizó con 66 pruebas aprobadas y ningún fallo.
