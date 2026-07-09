import os
import json
import shutil

# Ensure templates folder exists
os.makedirs("templates", exist_ok=True)

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Make it a template
html = html.replace(">Aceite De Orégano con Semilla Negra 6000mg (60 cápsulas)<", ">{{ product_title }}<")
html = html.replace(">Aceite De Orégano 6000 Mg con Semilla Negra<", ">{{ product_title }}<")
html = html.replace(">Aceite De Orégano con Semilla Negra<", ">{{ short_name }}<")
html = html.replace("producto: \"Aceite De Orégano con Semilla Negra\"", 'producto: "{{ short_name }}"')
html = html.replace("dudas%20sobre...%20Aceite De Orégano con Semilla Negra", "dudas%20sobre...%20{{ short_name }}")
html = html.replace("<title>Aceite De Orégano con Semilla Negra | Limpieza Digestiva e Inmune | Chile - Mundo Aura</title>", "<title>{{ seo_title }} - Mundo Aura</title>")

# Prices
html = html.replace("$23.990", "{{ promo_price }}")
html = html.replace("$31.990", "{{ normal_price }}")
html = html.replace("-25%", "{{ discount_badge }}")
html = html.replace("$32.990", "{{ promo2_price }}")

# Description tab
html = html.replace(">El Poder del Orégano y la Semilla Negra<", ">{{ desc_title }}<")
html = html.replace("Si sufres de inflamación crónica, gases (SIBO) o defensas bajas, tu cuerpo está pidiendo un reseteo profundo. Nuestro suplemento combina lo mejor de dos mundos para ofrecerte una solución definitiva y 100% natural.", "{{ desc_subtitle }}")
html = html.replace("Aceite de Orégano, Carvacrol, Aceite de Semilla Negra, Timoquinona, Aceite de Oliva Virgen Extra, Gelatina, Glicerina, Agua Purificada.", "{{ ingredients }}")

# Write to template
with open("templates/landing.html", "w", encoding="utf-8") as f:
    f.write(html)

# Create config json
oregano_config = {
    "product_title": "Aceite De Orégano con Semilla Negra 6000mg (60 cápsulas)",
    "short_name": "Aceite De Orégano con Semilla Negra",
    "seo_title": "Aceite De Orégano con Semilla Negra | Limpieza Digestiva e Inmune",
    "promo_price": "$23.990",
    "normal_price": "$31.990",
    "discount_badge": "-25%",
    "promo2_price": "$32.990",
    "desc_title": "El Poder del Orégano y la Semilla Negra",
    "desc_subtitle": "Si sufres de inflamación crónica, gases (SIBO) o defensas bajas, tu cuerpo está pidiendo un reseteo profundo. Nuestro suplemento combina lo mejor de dos mundos para ofrecerte una solución definitiva y 100% natural.",
    "ingredients": "Aceite de Orégano, Carvacrol, Aceite de Semilla Negra, Timoquinona, Aceite de Oliva Virgen Extra, Gelatina, Glicerina, Agua Purificada."
}

with open("oregano.json", "w", encoding="utf-8") as f:
    json.dump(oregano_config, f, indent=4, ensure_ascii=False)

# Build script
build_script = """import json
import os
import sys

def build_landing(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        
    with open("templates/landing.html", "r", encoding="utf-8") as f:
        template = f.read()
        
    for key, value in config.items():
        template = template.replace(f"{{{{ {key} }}}}", value)
        
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(template)
        
    print(f"✅ index.html generated successfully for {config.get('short_name')}!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        build_landing(sys.argv[1])
    else:
        print("Usage: python build_landing.py <config.json>")
"""
with open("build_landing.py", "w", encoding="utf-8") as f:
    f.write(build_script)

print("Automation setup complete!")
