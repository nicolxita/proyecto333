with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix the FAQ answer that got missed
old_text = "No, nuestro Aceite De Orégano con Semilla Negra es completamente neutro y sin sabor, diseñado para disolverse fácilmente en cualquier bebida, fría o caliente, sin alterar su gusto."
new_text = "No, la gran ventaja de estas cápsulas es que son fáciles de tragar y evitan el sabor picante o fuerte que tiene el aceite de orégano líquido tradicional."
html = html.replace(old_text, new_text)

# Also fix the <title> tag as requested by user's preference to not have 6000 Mg everywhere
old_title = "<title>Aceite De Orégano 6000 Mg con Semilla Negra | Regeneración para Piel, Cabello y Articulaciones | Chile - Mundo Aura</title>"
new_title = "<title>Aceite De Orégano con Semilla Negra | Limpieza Digestiva e Inmune | Chile - Mundo Aura</title>"
html = html.replace(old_title, new_title)
# Fallback title just in case it's different
html = html.replace("<title>Aceite De Orégano con Semilla Negra | Regeneración para Piel, Cabello y Articulaciones | Chile - Mundo Aura</title>", new_title)


with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 11 complete")
