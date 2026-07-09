with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Reviews
old_review_1 = "Llevo un mes tomándolo y mis uñas están súper fuertes, ya no se me quiebran como antes. Lo mezclo con el café de la mañana y ni se siente."
new_review_1 = "Estuve meses con el estómago súper inflamado (creo que era SIBO) y esto fue lo único que me ayudó. Llevo 2 semanas tomándolo y ya no me hincho después de almorzar."

old_review_2 = "Al principio era escéptica, pero el dolor de rodilla que tenía ha disminuido un montón. Puedo caminar mucho más ahora. Lo recomiendo de verdad."
new_review_2 = "Al principio dudaba por el sabor, pero al ser en cápsulas es súper fácil de tragar y no se siente nada del orégano. Mi digestión ha mejorado muchísimo, ya no sufro de pesadez."

old_review_3 = "Me llegó al día siguiente! Lo que más he notado es la piel, como más luminosa y suave. Se disuelve súper bien y no deja grumos."
new_review_3 = "Me llegó al día siguiente! Lo empecé a tomar porque siempre me resfriaba con los cambios de clima y mis defensas andaban bajas. Llevo mi primer ciclo y me siento excelente, súper recomendado."

html = html.replace(old_review_1, new_review_1)
html = html.replace(old_review_2, new_review_2)
html = html.replace(old_review_3, new_review_3)

# 2. Add Ingredients to Description
ingredients = """<h4 class="text-sm font-bold text-gray-900 mt-6 mb-2">Ingredientes:</h4>
                                <p class="text-[14px] text-gray-700 leading-relaxed mb-6">
                                    Aceite de Orégano, Carvacrol, Aceite de Semilla Negra, Timoquinona, Aceite de Oliva Virgen Extra, Gelatina, Glicerina, Agua Purificada.
                                </p>"""

old_desc = """<li class="flex items-start gap-2">
                                        <span class="text-emerald-500 mt-0.5">✔</span>
                                        <span><strong>Inmunidad de Acero:</strong> Un escudo antioxidante potente que fortalece tus defensas en cambios de estación.</span>
                                    </li>
                                </ul>"""
new_desc = old_desc + "\n                                " + ingredients

html = html.replace(old_desc, new_desc)

# 3. Fix the title specifically to what the user requested
html = html.replace(">Aceite De Orégano 6000 Mg con Semilla Negra<", ">Aceite De Orégano con Semilla Negra 6000mg (60 cápsulas)<")

# 4. Remove 6000 Mg from the pink ticks
html = html.replace("6000 Mg de Concentración Pura", "Adiós a la Hinchazón y Gases")


with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 12 complete")
