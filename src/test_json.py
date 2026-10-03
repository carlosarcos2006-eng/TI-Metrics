from parsers.json_parser import leer_eventos_json


ruta = "data/events.json"

eventos = leer_eventos_json(ruta)

print("Cantidad de eventos:", len(eventos))
print("Primer evento:")
print(eventos[0])