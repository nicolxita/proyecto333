with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    "El Escudo Natural que Necesitas": "Tu Reset Intestinal Definitivo",
    "¿Sientes que tus defensas bajan con facilidad o tienes problemas digestivos?": "¿Vives con el estómago inflamado, gases después de comer o sientes que todo te cae mal?",
    "Protección esencial para fortalecer tu sistema inmune, limpiar tu organismo y mejorar tu digestión.": "Un limpiador natural que actúa como una \"escoba\", eliminando bacterias malas mientras desinflama y calma las paredes de tu intestino.",
    
    "Alta Concentración:": "Acción de Limpieza Profunda:",
    "6000 mg de pureza que tu cuerpo asimila de manera óptima.": "Combate de raíz el sobrecrecimiento de bacterias (SIBO) y levaduras (Candidiasis).",
    
    "Cápsulas Sin Mal Sabor:": "Desinflama y Protege:",
    "Disfruta los enormes beneficios del orégano sin sufrir por su sabor intenso.": "Su fórmula calmante protege tus paredes intestinales para que no sufras durante el proceso.",
    
    "Defensas y Digestión:": "Adiós a la Hinchazón:",
    "Un solo paso diario para un bienestar completo, natural y duradero.": "Recupera tu balance microbiótico y vuelve a disfrutar de tus comidas sin malestares crónicos."
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 8 complete")
