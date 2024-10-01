import spacy
import json
import re

file_path = 'requisitos.txt'
output_file = 'acciones_atributos_mejorado.json'

# Leer el contenido del archivo de texto
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Dividir el contenido en requisitos individuales
requisitos = re.split(r'\n\nNombre:', text)
requisitos = [req.strip() for req in requisitos if req.strip()]

# Cargar el modelo de spaCy para español
nlp = spacy.load('es_core_news_sm')

# Función para identificar acciones y atributos
def identificar_acciones_atributos(doc):
    acciones = {token.lemma_ for token in doc if token.pos_ == 'VERB'}
    atributos = {token.lemma_ for token in doc if token.pos_ in ['NOUN', 'ADJ']}
    entidades = [(ent.text, ent.label_) for ent in doc.ents]
    return list(acciones), list(atributos), list(entidades)

# Procesar cada requisito
data = []

for req in requisitos:
    doc = nlp(req)
    
    # Identificar acciones y atributos
    acciones, atributos, entidades = identificar_acciones_atributos(doc)
    
    # Almacenar en la estructura de datos
    data.append({
        'requisito': req,
        'acciones': acciones,
        'atributos': atributos,
        'entidades': entidades
    })

# Guardar la estructura de datos en un archivo JSON
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"Datos guardados en {output_file}")