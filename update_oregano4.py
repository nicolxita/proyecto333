with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    # Replace the previous Dosis FAQ
    "¿Cuál es la dosis recomendada diaria?": "¿Cómo y cuándo debo tomar las cápsulas?",
    "Se recomienda consumir 1 a 2 cápsulas al día, idealmente junto con las comidas principales. Al ser muy potente, se aconseja tomarlo por ciclos (por ejemplo, 3 semanas de uso y 1 de descanso).": "Lo habitual es tomar 1 cápsula al día junto con tu comida más contundente (ej. el almuerzo). <br><br><b>Regla de oro:</b> Nunca las tomes con el estómago vacío. Al ser un extracto muy potente, acompañarlo con comida y agua evita cualquier sensación de acidez o reflujo.",
    
    # Replace the previous supply FAQ, adjust it to mention cycle lengths
    "¿Cuántas cápsulas vienen?": "¿Por cuánto tiempo seguido debo tomarlo?",
    "Cada frasco contiene 60 cápsulas, lo que equivale a un suministro para un mes completo (tomando 2 diarias) o dos meses (tomando 1 diaria).": "Debido a su gran potencia antibacteriana, se usa por ciclos para proteger tu flora intestinal:<br><br>• <b>Limpieza digestiva (hinchazón):</b> 2 a 3 semanas seguidas.<br>• <b>Refuerzo Inmune (resfríos):</b> 7 a 10 días.<br><br><b>El periodo de descanso:</b> Tras tomarlo por 3 semanas, descansa 2 semanas. En ese descanso, te recomendamos consumir probióticos para repoblar tu intestino de bacterias buenas.",
    
    # Update Contraindicaciones to be simpler since the cycle logic is now in the previous question
    "Al ser un limpiador natural muy potente, no se recomienda su uso continuo ininterrumpido por meses ni para mujeres embarazadas o lactantes. Lo ideal es tomarlo por periodos (2 a 4 semanas) y descansar. Consulta a tu médico ante cualquier duda.": "Al ser un limpiador natural muy potente, no se recomienda para mujeres embarazadas o en periodo de lactancia. Recuerda siempre respetar los periodos de descanso indicados y no tomarlo de forma continua por meses. Ante cualquier duda, consulta a tu médico."
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 4 complete")
