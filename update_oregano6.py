with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    "Toma 1 o 2 cápsulas al día con un vaso de agua para nutrir y proteger tu cuerpo de forma completamente natural y sin malos sabores.": "Toma 1 o 2 cápsulas al día junto con tu comida principal. <b>Nunca las tomes con el estómago vacío.</b> Úsalo por ciclos (ej. 3 semanas seguidas y 2 de descanso) para mantener tu flora intestinal protegida."
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 6 complete")
