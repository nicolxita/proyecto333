with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    # Remove probiotics mention
    " En ese descanso, te recomendamos consumir probióticos para repoblar tu intestino de bacterias buenas.": "",
    "En ese descanso, te recomendamos consumir probióticos para repoblar tu intestino de bacterias buenas.": "",
    
    # Change final CTA
    "Inicia tu camino hacia el bienestar": "Protege tu organismo de forma natural hoy mismo",
    "Incorpora Aceite De Orégano 6000 Mg a tu rutina y redescubre la vitalidad que nace desde el interior.": "Dale a tu cuerpo el escudo protector que necesita. Mantén tus defensas altas y tu digestión en equilibrio con el poder puro del orégano."
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 5 complete")
