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