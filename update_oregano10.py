with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix the double "con Semilla Negra"
html = html.replace("Aceite De Orégano con Semilla Negra con Semilla Negra", "Aceite De Orégano 6000 Mg con Semilla Negra")

# Also make sure the title tag is correct if it was duplicated
html = html.replace("<title>Aceite De Orégano con Semilla Negra con Semilla Negra</title>", "<title>Aceite De Orégano 6000 Mg con Semilla Negra</title>")

# Check if there is any other place where 6000 Mg was left out that shouldn't have been
# The user wants "6000 Mg" ONLY in the main title (h1). So the h1 should be:
# Aceite De Orégano 6000 Mg con Semilla Negra
# The <title> tag can also be that.
# Everything else should be "Aceite De Orégano con Semilla Negra"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 10 complete")
