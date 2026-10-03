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