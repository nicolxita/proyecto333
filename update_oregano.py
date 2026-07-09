import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Product Name and Copy changes
html = html.replace("Collagen Peptides Multi", "Aceite De Orégano 6000 Mg")
html = html.replace("Humidificador Difusor Aromaterapia Llama 3D", "Aceite De Orégano 6000 Mg")

# 2. Prices
html = html.replace("$34.990", "$23.990")
html = html.replace("$69.980", "$31.990")
html = html.replace("$52.485", "$35.985")

# 3. Benefits / Ticks
html = html.replace("Piel visiblemente renovada", "Refuerza tus Defensas Naturales")
html = html.replace("Movimiento sin límites", "Mejora tu Sistema Inmune y Digestivo")
html = html.replace("Vitalidad que se siente", "6000 Mg de Concentración Pura")

# 4. Reviews Images
html = html.replace('src="assets/l.avif"', 'src="assets/reseñas/l.avif"')
html = html.replace('src="assets/l (1).avif"', 'src="assets/reseñas/l (1).avif"')
html = html.replace('src="assets/l (2).avif"', 'src="assets/reseñas/l (2).avif"')

# 5. Review Descriptions (Update random collagen reviews to oregano)
html = html.replace("Noté mi piel más hidratada y suave.", "Siento que mis defensas están al 100%, súper recomendado.")
html = html.replace("Mis rodillas ya no me duelen tanto, excelente producto.", "Excelente para la digestión, ya no sufro de pesadez.")
html = html.replace("Me encanta que no tiene sabor y se disuelve súper fácil.", "Las cápsulas son fáciles de tragar y no dejan mal sabor.")
html = html.replace("Llevo 3 meses usándolo y mi cabello crece más fuerte.", "Desde que lo tomo no me he resfriado ni una sola vez.")
html = html.replace("¡Increíble! Es el mejor colágeno que he probado.", "Una maravilla, mi sistema inmune lo agradece.")
html = html.replace("Siento más energía durante el día y mi piel brilla.", "El mejor antioxidante natural. Llegó súper rápido.")

# 6. Description blocks
html = html.replace("Descubre el secreto para una piel radiante, articulaciones flexibles y una vitalidad renovada. Nuestro suplemento avanzado combina péptidos bioactivos de alta absorción para nutrir tu cuerpo desde adentro hacia afuera.", "Descubre el poder antibacteriano y antiviral más potente de la naturaleza. Nuestro suplemento avanzado te brinda una dosis extra de bienestar para mantener tus defensas altas y tu digestión impecable.")
html = html.replace("Disuelve una porción en tu bebida favorita, como agua, café o un batido, una vez al día para nutrir tu cuerpo desde el interior.", "Toma una cápsula al día con un vaso de agua para nutrir y proteger tu cuerpo de forma completamente natural y sin malos sabores.")

# 7. FAQs
html = html.replace("¿Cuándo comenzaré a ver los resultados?", "¿Para qué sirve exactamente?")
html = html.replace("Aunque cada cuerpo es distinto, muchas personas notan mejoras en piel y uñas en las primeras 3-4 semanas. Los beneficios articulares pueden tomar un poco más de tiempo en manifestarse.", "El aceite de orégano es conocido por sus fuertes propiedades antioxidantes, antibacterianas y antivirales. Apoya el sistema inmune, mejora la digestión y ayuda a combatir bacterias.")

html = html.replace("¿Tiene algún sabor u olor?", "¿Tienen el sabor fuerte del orégano?")
html = html.replace("No, nuestro Collagen Peptides Multi es completamente neutro y sin sabor, diseñado para disolverse fácilmente en cualquier bebida, fría o caliente, sin alterar su gusto.", "No, la gran ventaja de estas cápsulas es que son fáciles de tragar y evitan el sabor picante o fuerte que tiene el aceite de orégano líquido tradicional.")

html = html.replace("¿Cuál es la dosis recomendada?", "¿Cuál es la dosis recomendada diaria?")
html = html.replace("Recomendamos una porción diaria. Cada envase incluye una cuchara medidora para facilitar su uso y asegurar la dosis correcta para obtener todos sus beneficios.", "Se recomienda consumir 1 cápsula al día, idealmente junto con alguna de las comidas principales.")

html = html.replace("¿Es apto para dietas específicas?", "¿Cuántas cápsulas vienen?")
html = html.replace("Sí, nuestra fórmula es libre de gluten, lácteos, soya y azúcares añadidos. Es compatible con dietas keto y paleo.", "Cada frasco contiene 60 cápsulas, lo que equivale a un suministro para dos meses completos de bienestar.")

html = html.replace("¿Puedo tomarlo si estoy embarazada o en período de lactancia?", "¿Tiene contraindicaciones?")
html = html.replace("Aunque el colágeno es un componente natural, siempre recomendamos consultar con tu médico de cabecera antes de añadir cualquier suplemento a tu rutina durante estas etapas.", "Al ser un producto natural, es muy seguro. Sin embargo, no se recomienda para mujeres embarazadas o en periodo de lactancia. Ante dudas, consulta a tu médico.")

# 8. Regulatory badge fix
html = html.replace("bg-yellow-100 p-2 rounded-lg border border-yellow-200", "bg-indigo-50/50 text-indigo-900 border-indigo-100 p-2.5 rounded-lg border shadow-sm")
html = html.replace("bg-yellow-100 p-1.5 rounded-lg border border-yellow-200", "bg-indigo-50/50 text-indigo-900 border-indigo-100 p-2.5 rounded-lg border shadow-sm")

# 9. Update the {{ product_name }} fallback if exists
html = html.replace("{{ product_name }}", "Aceite De Orégano 6000 Mg")
html = html.replace("{{ offer_price }}", "$23.990")


with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update complete")
