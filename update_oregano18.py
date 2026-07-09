with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the specific occurrences
html = html.replace("Aceite De Orégano 6000 Mg con Semilla Negra", "Aceite De Orégano con Aceite de Semilla Negra 6000 Mg")
html = html.replace("Aceite De Orégano con Semilla Negra", "Aceite De Orégano con Aceite de Semilla Negra 6000 Mg")
# Fix potential double replacement if the first one was already caught by the second (it's safe here because the first one has 6000 Mg in the middle, while the second doesn't).
# Actually, let's just do a clean replace for the second one, which will also hit the title, whatsapp, js payload, etc.

# Write it back
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 18 complete")
