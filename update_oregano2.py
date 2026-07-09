with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    "El Ritual Diario de Regeneración": "El Escudo Natural que Necesitas",
    "¿Sientes que tu piel, energía y articulaciones ya no son las de antes?": "¿Sientes que tus defensas bajan con facilidad o tienes problemas digestivos?",
    "Nutrición esencial para restaurar la vitalidad de tu piel, cabello y articulaciones.": "Protección esencial para fortalecer tu sistema inmune, limpiar tu organismo y mejorar tu digestión.",
    "Máxima Absorción Celular:": "Alta Concentración:",
    "Péptidos puros que tu cuerpo realmente aprovecha.": "6000 mg de pureza que tu cuerpo asimila de manera óptima.",
    "Fórmula Pura y Limpia:": "Cápsulas Sin Mal Sabor:",
    "Sin aditivos, azúcares ni saborizantes artificiales.": "Disfruta los enormes beneficios del orégano sin sufrir por su sabor intenso.",
    "Belleza y Movimiento:": "Defensas y Digestión:",
    "Un solo gesto para un bienestar integral.": "Un solo paso diario para un bienestar completo, natural y duradero."
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 2 complete")
