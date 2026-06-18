import re
import json

# Full dataset of Chilean regions and communes to include
# Excluding blocked regions: Arica, Tarapaca, Antofagasta, Aysen, Magallanes
# And excluding specific communes.

regions_data = {
    "coquimbo": {
        "name": "Región de Coquimbo",
        "communes": ["La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paihuano", "Vicuña", "Illapel", "Canela", "Los Vilos", "Salamanca", "Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado"]
    },
    "valparaiso": {
        "name": "Región de Valparaíso",
        # Excludes: Isla de Pascua, Juan Fernández
        "communes": ["Valparaíso", "Casablanca", "Concón", "Puchuncaví", "Quintero", "Viña del Mar", "Los Andes", "Calle Larga", "Rinconada", "San Esteban", "La Ligua", "Cabildo", "Papudo", "Petorca", "Zapallar", "Quillota", "Calera", "Hijuelas", "La Cruz", "Nogales", "San Antonio", "Algarrobo", "Cartagena", "El Quisco", "El Tabo", "Santo Domingo", "San Felipe", "Catemu", "Llaillay", "Panquehue", "Putaendo", "Santa María", "Quilpué", "Limache", "Olmué", "Villa Alemana"]
    },
    "metropolitana": {
        "name": "Región Metropolitana",
        "communes": ["Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón", "Santiago", "Vitacura", "Puente Alto", "Pirque", "San José de Maipo", "Colina", "Lampa", "Tiltil", "San Bernardo", "Buin", "Calera de Tango", "Paine", "Melipilla", "Alhué", "Curacaví", "María Pinto", "San Pedro", "Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor"]
    },
    "ohiggins": {
        "name": "Región de O'Higgins",
        "communes": ["Rancagua", "Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros", "Las Cabras", "Machalí", "Malloa", "Mostazal", "Olivar", "Peumo", "Pichidegua", "Quinta de Tilcoco", "Rengo", "Requínoa", "San Vicente", "Pichilemu", "La Estrella", "Litueche", "Marchigüe", "Navidad", "Paredones", "San Fernando", "Chépica", "Chimbarongo", "Lolol", "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque", "Santa Cruz"]
    },
    "maule": {
        "name": "Región del Maule",
        "communes": ["Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael", "Cauquenes", "Chanco", "Pelluhue", "Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén", "Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre", "Yerbas Buenas"]
    },
    "nuble": {
        "name": "Región de Ñuble",
        # Excludes: San Fabián
        "communes": ["Chillán", "Bulnes", "Cobquecura", "Coelemu", "Coihueco", "Chillán Viejo", "El Carmen", "Ninhue", "Ñiquén", "Pemuco", "Pinto", "Portezuelo", "Quillón", "Quirihue", "Ránquil", "San Carlos", "San Ignacio", "San Nicolás", "Treguaco", "Yungay"]
    },
    "biobio": {
        "name": "Región del Bío-Bío",
        # Excludes: Alto Biobío
        "communes": ["Concepción", "Coronel", "Chiguayante", "Florida", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé", "Hualpén", "Lebu", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Los Álamos", "Tirúa", "Los Ángeles", "Antuco", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel"]
    },
    "araucania": {
        "name": "Región de La Araucanía",
        "communes": ["Temuco", "Carahue", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre Las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Cholchol", "Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"]
    },
    "losrios": {
        "name": "Región de Los Ríos",
        "communes": ["Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli", "La Unión", "Futrono", "Lago Ranco", "Río Bueno"]
    },
    "loslagos": {
        "name": "Región de Los Lagos",
        # Excludes: Chaitén, Futaleufú, Palena
        "communes": ["Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Los Muermos", "Llanquihue", "Maullín", "Puerto Varas", "Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao", "Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo", "Hualaihué"]
    }
}

options_html = '<option value="">Selecciona</option>\n'
for key, data in regions_data.items():
    options_html += f'                    <option value="{key}">{data["name"]}</option>\n'

js_dict = {}
for key, data in regions_data.items():
    js_dict[key] = data["communes"]

js_content = json.dumps(js_dict, ensure_ascii=False, indent=4)

script = f"""
<script>
  // Base de datos de comunas por región (Optimizada según exclusiones)
  const comunasPorRegion = {js_content};

  const regionSelect = document.getElementById('region');
  const comunaSelect = document.getElementById('comuna');

  if (regionSelect && comunaSelect) {{
      regionSelect.addEventListener('change', function() {{
        const regionSeleccionada = this.value;
        comunaSelect.innerHTML = '<option value="">Selecciona Comuna</option>';
        if (regionSeleccionada && comunasPorRegion[regionSeleccionada]) {{
          comunaSelect.disabled = false;
          comunasPorRegion[regionSeleccionada].forEach(function(comuna) {{
            const option = document.createElement('option');
            option.value = comuna.toLowerCase().replace(/\s+/g, '-');
            option.textContent = comuna;
            comunaSelect.appendChild(option);
          }});
        }} else {{
          comunaSelect.disabled = true;
        }}
      }});
  }}
</script>
</body>
"""

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the region select options
    # Find <select id="region" ...> ... </select>
    pattern_select = r'(<select id="region"[^>]*>).*?(</select>)'
    
    # Replacement for options
    replacement = r'\g<1>\n' + options_html + r'                \g<2>'
    
    content = re.sub(pattern_select, replacement, content, flags=re.DOTALL)

    # 2. Replace the JS script at the end
    pattern_script = r'<script>\s*const comunasPorRegion.*?</body>'
    
    content = re.sub(pattern_script, lambda m: script, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated regions in {filepath}")

update_file('index.html')
update_file('templates/landing.html')
