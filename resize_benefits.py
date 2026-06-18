import re

def resize_benefits(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Target literal text
    old_benefits_title = '<h2 class="text-3xl md:text-4xl font-bold tracking-tighter text-gray-900 mb-4">Bienestar en Cada Detalle</h2>'
    new_benefits_title = '<h2 class="text-2xl md:text-3xl font-bold tracking-tighter text-gray-900 mb-3">Bienestar en Cada Detalle</h2>'
    content = content.replace(old_benefits_title, new_benefits_title)

    old_benefits_desc = '<p class="text-lg text-gray-600 leading-relaxed">Más que un humidificador, es una experiencia sensorial diseñada para elevar tu día a día.</p>'
    new_benefits_desc = '<p class="text-base text-gray-600 leading-relaxed">Más que un humidificador, es una experiencia sensorial diseñada para elevar tu día a día.</p>'
    content = content.replace(old_benefits_desc, new_benefits_desc)

    # Target template variables
    old_tpl_title = '<h2 class="text-3xl md:text-4xl font-bold tracking-tighter text-gray-900 mb-4">{{ benefits_title }}</h2>'
    new_tpl_title = '<h2 class="text-2xl md:text-3xl font-bold tracking-tighter text-gray-900 mb-3">{{ benefits_title }}</h2>'
    content = content.replace(old_tpl_title, new_tpl_title)

    old_tpl_desc = '<p class="text-lg text-gray-600 leading-relaxed">{{ benefits_desc }}</p>'
    new_tpl_desc = '<p class="text-base text-gray-600 leading-relaxed">{{ benefits_desc }}</p>'
    content = content.replace(old_tpl_desc, new_tpl_desc)

    # Also reduce section padding if it's the exact one
    # Wait, the benefits section uses <section class="bg-gray-50/70 py-16 md:py-24">
    # I already replaced that generic string in resize_text.py for the problem section. 
    # Let's check if the benefits section still has py-16 md:py-24
    content = content.replace('<section class="bg-gray-50/70 py-16 md:py-24">', '<section class="bg-gray-50/70 py-12 md:py-16">')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Resized benefits in {filepath}")

resize_benefits('index.html')
try:
    resize_benefits('templates/landing.html')
except Exception as e:
    print(e)
