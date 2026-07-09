with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update the description tab (Tab 2: Description)
old_desc = """<h3 class="text-xl font-bold text-gray-900 mb-4">Aceite De Orégano 6000 Mg</h3>
                                <p class="text-[15px] text-gray-700 leading-relaxed mb-6 whitespace-pre-line">
                                    Protección esencial para fortalecer tu sistema inmune, limpiar tu organismo y mejorar tu digestión.
                                </p>"""

new_desc = """<h3 class="text-xl font-bold text-gray-900 mb-4">El Poder del Orégano y la Semilla Negra</h3>
                                <p class="text-[15px] text-gray-700 leading-relaxed mb-4">
                                    Si sufres de <strong>inflamación crónica, gases (SIBO) o defensas bajas</strong>, tu cuerpo está pidiendo un reseteo profundo. Nuestro suplemento combina lo mejor de dos mundos para ofrecerte una solución definitiva y 100% natural.
                                </p>
                                <ul class="space-y-3 text-[14px] text-gray-700 leading-relaxed mb-6">
                                    <li class="flex items-start gap-2">
                                        <span class="text-emerald-500 mt-0.5">✔</span>
                                        <span><strong>Acción Antimicrobiana:</strong> El aceite de orégano actúa como una escoba natural, combatiendo levaduras, parásitos y el sobrecrecimiento bacteriano (SIBO).</span>
                                    </li>
                                    <li class="flex items-start gap-2">
                                        <span class="text-emerald-500 mt-0.5">✔</span>
                                        <span><strong>Efecto Calmante:</strong> El aceite de semilla negra (Black Seed Oil) recubre y desinflama las paredes estomacales, evitando molestias y acidez.</span>
                                    </li>
                                    <li class="flex items-start gap-2">
                                        <span class="text-emerald-500 mt-0.5">✔</span>
                                        <span><strong>Inmunidad de Acero:</strong> Un escudo antioxidante potente que fortalece tus defensas en cambios de estación.</span>
                                    </li>
                                </ul>"""
html = html.replace(old_desc, new_desc)

# 2. Add "con Semilla Negra" to the main h1 and keep 6000 Mg
html = html.replace('<h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 leading-tight tracking-tight mb-2">\n                            Aceite De Orégano 6000 Mg\n                        </h1>', '<h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 leading-tight tracking-tight mb-2">\n                            Aceite De Orégano 6000 Mg con Semilla Negra\n                        </h1>')
html = html.replace('<h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 leading-tight tracking-tight mb-2">Aceite De Orégano 6000 Mg</h1>', '<h1 class="text-2xl md:text-3xl font-extrabold text-gray-900 leading-tight tracking-tight mb-2">Aceite De Orégano 6000 Mg con Semilla Negra</h1>')

# 3. Replace all other instances of 6000 Mg to just "Aceite De Orégano con Semilla Negra"
html = html.replace("Aceite De Orégano 6000 Mg", "Aceite De Orégano con Semilla Negra")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 9 complete")
