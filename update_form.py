import re

def update_form(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Phone number update
    old_phone = r'<input type="tel" id="codPhone" required class="([^"]+)" placeholder="Ej: \+56 9 1234 5678">'
    new_phone = r'''<input type="tel" id="codPhone" required class="\1" placeholder="+56 9 1234 5678" value="+56 " oninput="let v = this.value; if(!v.startsWith('+56 ')) { this.value = '+56 '; return; } let num = v.substring(4).replace(/[^0-9]/g, ''); this.value = '+56 ' + num;">'''
    
    # 2. Region / Comuna update
    # The existing region/comuna HTML is:
    # <div>
    #     <label class="block text-[10px] font-bold text-gray-700 uppercase tracking-wider mb-1">Región y Comuna</label>
    #     <input type="text" id="codCity" required class="..." placeholder="Ej: Metropolitana / Providencia">
    # </div>
    
    old_region = r'<div>\s*<label class="block text-\[10px\] font-bold text-gray-700 uppercase tracking-wider mb-1">Regi.n y Comuna</label>\s*<input type="text" id="codCity"[^>]+>\s*</div>'
    
    # Matching the styling from the original form instead of the user's pink-400 template to maintain consistency
    new_region = """<div class="grid grid-cols-2 gap-3">
            <div>
                <label for="region" class="block text-[10px] font-bold text-gray-700 uppercase tracking-wider mb-1">Región *</label>
                <select id="region" name="region" required class="w-full bg-white border border-gray-200 rounded-lg px-3 py-2.5 text-sm text-gray-900 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-colors appearance-none cursor-pointer">
                    <option value="">Selecciona</option>
                    <option value="metropolitana">R. Metropolitana</option>
                    <option value="valparaiso">R. Valparaíso</option>
                    <option value="biobio">R. Bío-Bío</option>
                </select>
            </div>
            <div>
                <label for="comuna" class="block text-[10px] font-bold text-gray-700 uppercase tracking-wider mb-1">Comuna *</label>
                <select id="comuna" name="comuna" required disabled class="w-full bg-white border border-gray-200 rounded-lg px-3 py-2.5 text-sm text-gray-900 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-colors appearance-none cursor-pointer disabled:opacity-50 disabled:bg-gray-50 disabled:cursor-not-allowed">
                    <option value="">Selecciona</option>
                </select>
            </div>
        </div>"""

    # 3. Add JS script
    script = """
<script>
  const comunasPorRegion = {
    metropolitana: [
      "Santiago", "Providencia", "Las Condes", "Vitacura", "Ñuñoa", 
      "Maipú", "La Florida", "Puente Alto", "San Miguel", "Recoleta"
    ],
    valparaiso: [
      "Valparaíso", "Viña del Mar", "Concón", "Quilpué", "Villa Alemana", 
      "San Antonio", "Quillota", "San Felipe", "Los Andes"
    ],
    biobio: [
      "Concepción", "Talcahuano", "San Pedro de la Paz", "Chiguayante", 
      "Coronel", "Los Ángeles", "Chillán", "Lebu"
    ]
  };

  const regionSelect = document.getElementById('region');
  const comunaSelect = document.getElementById('comuna');

  if (regionSelect && comunaSelect) {
      regionSelect.addEventListener('change', function() {
        const regionSeleccionada = this.value;
        comunaSelect.innerHTML = '<option value="">Selecciona Comuna</option>';
        if (regionSeleccionada && comunasPorRegion[regionSeleccionada]) {
          comunaSelect.disabled = false;
          comunasPorRegion[regionSeleccionada].forEach(function(comuna) {
            const option = document.createElement('option');
            option.value = comuna.toLowerCase().replace(/\s+/g, '-');
            option.textContent = comuna;
            comunaSelect.appendChild(option);
          });
        } else {
          comunaSelect.disabled = true;
        }
      });
  }
</script>
</body>"""

    content = re.sub(old_phone, new_phone, content)
    content = re.sub(old_region, new_region, content)
    
    if "comunasPorRegion" not in content:
        content = content.replace('</body>', script)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated form in {filepath}")

update_form('index.html')
update_form('templates/landing.html')
