with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    "Se recomienda consumir 1 cápsula al día, idealmente junto con alguna de las comidas principales.": "Se recomienda consumir 1 a 2 cápsulas al día, idealmente junto con las comidas principales. Al ser muy potente, se aconseja tomarlo por ciclos (por ejemplo, 3 semanas de uso y 1 de descanso).",
    "Cada frasco contiene 60 cápsulas, lo que equivale a un suministro para dos meses completos de bienestar.": "Cada frasco contiene 60 cápsulas, lo que equivale a un suministro para un mes completo (tomando 2 diarias) o dos meses (tomando 1 diaria).",
    "Al ser un producto natural, es muy seguro. Sin embargo, no se recomienda para mujeres embarazadas o en periodo de lactancia. Ante dudas, consulta a tu médico.": "Al ser un limpiador natural muy potente, no se recomienda su uso continuo ininterrumpido por meses ni para mujeres embarazadas o lactantes. Lo ideal es tomarlo por periodos (2 a 4 semanas) y descansar. Consulta a tu médico ante cualquier duda.",
    "Toma una cápsula al día con un vaso de agua": "Toma 1 o 2 cápsulas al día con un vaso de agua"
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 3 complete")
