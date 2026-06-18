import os
import re

with open("templates/landing.html", "r", encoding="utf-8") as f:
    content = f.read()

# Title
content = content.replace("<title>Humidificador Difusor Llama 3D - Mundo Aura</title>", "<title>{{ seo_title }} - Mundo Aura</title>")

# Images
content = content.replace('src="file:///C:/Users/Option/Documents/proyecto333/generated_assets/humidificador_difuso_image_0.jpg"', 'src="{{ image_assets[0] }}"')
content = content.replace('src="https://i.ibb.co/b3j6Y3g/difusor-llama-ambiente.jpg"', 'src="{{ image_assets[1] }}"')
content = content.replace('src="https://i.ibb.co/L5hY58T/difusor-llama-hero.jpg"', 'src="{{ image_assets[0] }}"')

# SKU and Name
content = content.replace("SKU: MA-HDF-087", "SKU: {{ sku }}")
content = content.replace("""<h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 leading-tight tracking-tight mb-2">
                            Humidificador Difusor Llama 3D
                        </h1>""", """<h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 leading-tight tracking-tight mb-2">
                            {{ product_name }}
                        </h1>""")

# Also in the form
content = content.replace("""<span class="block text-xs font-bold text-gray-900 leading-tight">Humidificador Difusor Llama 3D</span>""", """<span class="block text-xs font-bold text-gray-900 leading-tight">{{ product_name }}</span>""")

# Prices
content = content.replace("$34.990", "{{ offer_price }}")
content = content.replace("$69.980", "{{ normal_price }}")
content = content.replace("$52.490", "{{ promo_2_price }}")

# Dates
content = content.replace("26 de Julio", "{{ fecha_inicio }}")
content = content.replace("28 de Julio", "{{ fecha_fin }}")

# Problem section
content = content.replace("¿Tu espacio se siente apagado y sin vida?", "{{ problem_title }}")
content = content.replace("El estrés diario, el aire seco y la monotonía visual agotan tu energía. Mereces un refugio personal que te inspire y te relaje, un lugar donde puedas desconectar y recargar baterías de verdad.", "{{ problem_desc }}")

# Solution section
content = content.replace("LA SOLUCIÓN", "{{ solution_pretitle }}")
content = content.replace("El equilibrio perfecto entre diseño y bienestar.", "{{ solution_title }}")
content = content.replace("Presentamos el Difusor Llama 3D. Más que un humidificador, es una pieza central que transforma cualquier habitación en un santuario de calma con su hipnótico y seguro efecto de llama.", "{{ solution_desc }}")

# Benefits title
content = content.replace("Más que un difusor, una experiencia.", "{{ benefits_title }}")
content = content.replace("Diseñado para calmar tus sentidos y elevar tu entorno.", "{{ benefits_desc }}")

# Benefits block
benefits_block = """<div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                    <div class="bg-white p-6 rounded-2xl border border-gray-100">
                        <h3 class="font-bold text-lg mb-2">Atmósfera Única</h3>
                        <p class="text-sm text-gray-600 leading-relaxed">El efecto de llama 3D crea un ambiente cálido y acogedor al instante, convirtiéndose en el centro de todas las miradas.</p>
                    </div>
                    <div class="bg-white p-6 rounded-2xl border border-gray-100">
                        <h3 class="font-bold text-lg mb-2">Respira Bienestar</h3>
                        <p class="text-sm text-gray-600 leading-relaxed">Añade tus aceites esenciales favoritos para combatir el estrés, mejorar la concentración o simplemente disfrutar de un aroma increíble.</p>
                    </div>
                    <div class="bg-white p-6 rounded-2xl border border-gray-100">
                        <h3 class="font-bold text-lg mb-2">Diseño que Inspira</h3>
                        <p class="text-sm text-gray-600 leading-relaxed">Su estética minimalista y moderna complementa cualquier decoración, desde la oficina en casa hasta el dormitorio.</p>
                    </div>
                    <div class="bg-white p-6 rounded-2xl border border-gray-100">
                        <h3 class="font-bold text-lg mb-2">Silencio y Seguridad</h3>
                        <p class="text-sm text-gray-600 leading-relaxed">Opera de forma ultra silenciosa y cuenta con apagado automático para que puedas relajarte sin preocupaciones.</p>
                    </div>
                </div>"""

new_benefits_block = """<div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {% for benefit in benefits %}
                    <div class="bg-white p-6 rounded-2xl border border-gray-100">
                        <h3 class="font-bold text-lg mb-2">{{ benefit.title }}</h3>
                        <p class="text-sm text-gray-600 leading-relaxed">{{ benefit.description }}</p>
                    </div>
                    {% endfor %}
                </div>"""

content = content.replace(benefits_block, new_benefits_block)

# How it works
content = content.replace("Simple. Intuitivo. Mágico.", "{{ how_it_works_title }}")
content = content.replace("Disfruta de una atmósfera perfecta en solo tres pasos.", "{{ how_it_works_desc }}")

how_it_works_block = """<div class="grid md:grid-cols-3 gap-8 text-center">
                <div class="flex flex-col items-center">
                    <div class="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center font-bold text-xl text-gray-900 mb-4">1</div>
                    <h3 class="font-bold text-lg mb-2">Añade Agua</h3>
                    <p class="text-sm text-gray-600 leading-relaxed">Llena el depósito con agua purificada hasta la marca indicada para un rendimiento óptimo.</p>
                </div>
                <div class="flex flex-col items-center">
                    <div class="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center font-bold text-xl text-gray-900 mb-4">2</div>
                    <h3 class="font-bold text-lg mb-2">Agrega Esencia</h3>
                    <p class="text-sm text-gray-600 leading-relaxed">Vierte 2-3 gotas de tu aceite esencial favorito para crear el ambiente deseado.</p>
                </div>
                <div class="flex flex-col items-center">
                    <div class="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center font-bold text-xl text-gray-900 mb-4">3</div>
                    <h3 class="font-bold text-lg mb-2">Enciende y Disfruta</h3>
                    <p class="text-sm text-gray-600 leading-relaxed">Conecta el cable USB-C y relájate al instante con el hipnótico efecto de llama.</p>
                </div>
            </div>"""

new_how_it_works_block = """<div class="grid md:grid-cols-3 gap-8 text-center">
                {% for step in how_it_works_steps %}
                <div class="flex flex-col items-center">
                    <div class="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center font-bold text-xl text-gray-900 mb-4">{{ loop.index }}</div>
                    <h3 class="font-bold text-lg mb-2">{{ step.title }}</h3>
                    <p class="text-sm text-gray-600 leading-relaxed">{{ step.description }}</p>
                </div>
                {% endfor %}
            </div>"""
content = content.replace(how_it_works_block, new_how_it_works_block)

# Highlights
highlights_block = """<div class="grid md:grid-cols-2 gap-12 items-center">
                <div class="w-full h-auto aspect-video md:aspect-square bg-gray-50 rounded-3xl flex items-center justify-center overflow-hidden border border-gray-100">
                    <img src="{{ image_assets[1] }}" alt="Detalle del efecto de llama del difusor" class="w-full h-full object-cover">
                </div>
                <div>
                    <h3 class="text-2xl md:text-3xl font-bold tracking-tighter mb-3">Tecnología de Llama Ultrasónica</h3>
                    <p class="text-gray-600 leading-relaxed">La "llama" es en realidad una bruma ultrafina y fría, creada por vibraciones ultrasónicas e iluminada por LEDs de bajo consumo. Es completamente segura al tacto, ideal para hogares con niños o mascotas.</p>
                </div>
            </div>
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div class="md:order-2 w-full h-auto aspect-video md:aspect-square bg-gray-50 rounded-3xl flex items-center justify-center overflow-hidden border border-gray-100">
                    <img src="{{ image_assets[0] }}" alt="Difusor Llama 3D apagado mostrando su diseño minimalista" class="w-full h-full object-cover">
                </div>
                <div class="md:order-1">
                    <h3 class="text-2xl md:text-3xl font-bold tracking-tighter mb-3">Diseñado para tu Tranquilidad</h3>
                    <p class="text-gray-600 leading-relaxed">Equipado con un chip inteligente, el difusor se apaga automáticamente cuando el nivel de agua es bajo. Su funcionamiento es tan silencioso (<30dB) que apenas notarás que está ahí, perfecto para el dormitorio o la oficina.</p>
                </div>
            </div>"""

new_highlights_block = """{% if highlights and highlights|length >= 2 %}
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div class="w-full h-auto aspect-video md:aspect-square bg-gray-50 rounded-3xl flex items-center justify-center overflow-hidden border border-gray-100">
                    <img src="{{ image_assets[1] }}" alt="{{ highlights[0].title }}" class="w-full h-full object-cover">
                </div>
                <div>
                    <h3 class="text-2xl md:text-3xl font-bold tracking-tighter mb-3">{{ highlights[0].title }}</h3>
                    <p class="text-gray-600 leading-relaxed">{{ highlights[0].description }}</p>
                </div>
            </div>
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div class="md:order-2 w-full h-auto aspect-video md:aspect-square bg-gray-50 rounded-3xl flex items-center justify-center overflow-hidden border border-gray-100">
                    <img src="{{ image_assets[0] }}" alt="{{ highlights[1].title }}" class="w-full h-full object-cover">
                </div>
                <div class="md:order-1">
                    <h3 class="text-2xl md:text-3xl font-bold tracking-tighter mb-3">{{ highlights[1].title }}</h3>
                    <p class="text-gray-600 leading-relaxed">{{ highlights[1].description }}</p>
                </div>
            </div>
            {% endif %}"""
content = content.replace(highlights_block, new_highlights_block)

# Social proof
content = content.replace("Amado por miles de hogares en Chile.", "{{ social_proof_title }}")
content = content.replace("No solo lo decimos nosotros. Ve lo que nuestros clientes opinan.", "{{ social_proof_desc }}")

reviews_block = """<div class="grid md:grid-cols-3 gap-8">
                    <div class="bg-white p-6 rounded-2xl border border-gray-100 space-y-4">
                        <div class="flex text-amber-400">★★★★★</div>
                        <p class="text-gray-800 font-medium">"Transformó por completo mi oficina en casa. Es súper relajante para trabajar y se ve increíble en las videollamadas."</p>
                        <span class="text-sm text-gray-500 font-semibold">Camila R. - Providencia</span>
                    </div>
                    <div class="bg-white p-6 rounded-2xl border border-gray-100 space-y-4">
                        <div class="flex text-amber-400">★★★★★</div>
                        <p class="text-gray-800 font-medium">"Lo compré sin muchas expectativas y me sorprendió. El efecto de la llama es hipnótico y mucho más lindo que en las fotos. 100% recomendado."</p>
                        <span class="text-sm text-gray-500 font-semibold">Javier M. - Las Condes</span>
                    </div>
                    <div class="bg-white p-6 rounded-2xl border border-gray-100 space-y-4">
                        <div class="flex text-amber-400">★★★★★</div>
                        <p class="text-gray-800 font-medium">"El mejor regalo que me han hecho. Lo uso todas las noches con aceite de lavanda para dormir mejor. Además, el envío fue rapidísimo."</p>
                        <span class="text-sm text-gray-500 font-semibold">Sofía L. - Viña del Mar</span>
                    </div>
                </div>"""

new_reviews_block = """<div class="grid md:grid-cols-3 gap-8">
                    {% for review in reviews %}
                    <div class="bg-white p-6 rounded-2xl border border-gray-100 space-y-4">
                        <div class="flex text-amber-400">★★★★★</div>
                        <p class="text-gray-800 font-medium">"{{ review.quote }}"</p>
                        <span class="text-sm text-gray-500 font-semibold">{{ review.author }} - {{ review.location }}</span>
                    </div>
                    {% endfor %}
                </div>"""
content = content.replace(reviews_block, new_reviews_block)

# Objections
content = content.replace("Diseñado para tu tranquilidad.", "{{ objections_title }}")
content = content.replace("Hemos pensado en cada detalle para que tu única preocupación sea relajarte.", "{{ objections_desc }}")

objections_block = """<div class="space-y-6">
                    <div class="flex items-start gap-4">
                        <div class="text-emerald-400 mt-1"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
                        <div>
                            <h4 class="font-bold">Totalmente Seguro</h4>
                            <p class="text-gray-400 text-sm">La 'llama' es una bruma fría iluminada por LED. Es segura al tacto y para niños o mascotas.</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-4">
                        <div class="text-emerald-400 mt-1"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg></div>
                        <div>
                            <h4 class="font-bold">Susurro Silencioso</h4>
                            <p class="text-gray-400 text-sm">Su tecnología ultrasónica opera por debajo de los 30dB, ideal para dormir o concentrarse.</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-4">
                        <div class="text-emerald-400 mt-1"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.7 10.3a2.41 2.41 0 0 0 0 3.41l7.59 7.59a2.41 2.41 0 0 0 3.41 0l7.59-7.59a2.41 2.41 0 0 0 0-3.41l-7.59-7.59a2.41 2.41 0 0 0-3.41 0Z"/></svg></div>
                        <div>
                            <h4 class="font-bold">Materiales Premium</h4>
                            <p class="text-gray-400 text-sm">Construido con plástico ABS de alta calidad libre de BPA, para una durabilidad y seguridad garantizadas.</p>
                        </div>
                    </div>
                </div>"""

new_objections_block = """<div class="space-y-6">
                    {% for objection in objections %}
                    <div class="flex items-start gap-4">
                        <div class="text-emerald-400 mt-1"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
                        <div>
                            <h4 class="font-bold">{{ objection.title }}</h4>
                            <p class="text-gray-400 text-sm">{{ objection.description }}</p>
                        </div>
                    </div>
                    {% endfor %}
                </div>"""
content = content.replace(objections_block, new_objections_block)

# FAQs - this requires regex because the FAQ block is huge
import re
faq_block_match = re.search(r'<div class="space-y-4">.*?</div>\s*</section>\s*<!-- 10. Final CTA Section -->', content, re.DOTALL)
if faq_block_match:
    faq_outer = faq_block_match.group(0)
    
    new_faq_block = """<div class="space-y-4">
                {% for faq in faqs %}
                <details class="group {% if not loop.last %}border-b border-gray-200{% endif %} pb-4">
                    <summary class="flex justify-between items-center cursor-pointer list-none">
                        <span class="font-medium text-gray-900">{{ faq.question }}</span>
                        <span class="transition-transform transform group-open:rotate-180">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                        </span>
                    </summary>
                    <p class="text-gray-600 mt-3 text-sm leading-relaxed">{{ faq.answer }}</p>
                </details>
                {% endfor %}
            </div>
        </section>

        <!-- 10. Final CTA Section -->"""
    content = content.replace(faq_outer, new_faq_block)

# CTA
content = content.replace("Transforma tu hogar hoy.", "{{ cta_title }}")
content = content.replace("Crea tu propio santuario de paz y diseño. Pide tu Difusor Llama 3D con envío gratis y paga de forma segura al recibirlo.", "{{ cta_desc }}")

with open("templates/landing.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Template processed successfully")
