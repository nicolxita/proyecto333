import re

def resize_texts(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to target the Problem and Solution sections specifically to not affect the Hero section if possible.
    # But actually, text-3xl md:text-4xl is only used in Problem, Solution, Benefits, Objection Handling, etc.
    # The Hero section uses text-2xl md:text-3xl for the main H1. 
    # Wait, if I replace all text-3xl md:text-4xl, it will affect ALL H2s across the page! 
    # The user specifically mentioned problem and solution, but usually landing pages have consistent H2 sizes. 
    # It's better to just replace them in those specific sections.

    # Let's just use string replacement on the exact blocks
    
    # PROBLEM SECTION
    old_problem_title = '<h2 class="text-3xl md:text-4xl font-bold tracking-tighter text-gray-900 mb-4">El Ruido Constante del Mundo Moderno</h2>'
    new_problem_title = '<h2 class="text-2xl md:text-3xl font-bold tracking-tighter text-gray-900 mb-3">El Ruido Constante del Mundo Moderno</h2>'
    content = content.replace(old_problem_title, new_problem_title)

    old_problem_desc = '<p class="text-lg text-gray-600 leading-relaxed">El estrés diario, la ansiedad y la dificultad para desconectar se han vuelto la norma. Tu hogar, que debería ser tu refugio, a menudo no logra ofrecer esa calma que tanto necesitas para recargar energías.</p>'
    new_problem_desc = '<p class="text-base text-gray-600 leading-relaxed">El estrés diario, la ansiedad y la dificultad para desconectar se han vuelto la norma. Tu hogar, que debería ser tu refugio, a menudo no logra ofrecer esa calma que tanto necesitas para recargar energías.</p>'
    content = content.replace(old_problem_desc, new_problem_desc)
    
    # If the user is using templates with {{ problem_title }}, then the text might actually literally be {{ problem_title }}
    # Let's check if the file contains the template variables literally.
    if '{{ problem_title }}' in content:
        content = content.replace('<h2 class="text-3xl md:text-4xl font-bold tracking-tighter text-gray-900 mb-4">{{ problem_title }}</h2>',
                                  '<h2 class="text-2xl md:text-3xl font-bold tracking-tighter text-gray-900 mb-3">{{ problem_title }}</h2>')
        content = content.replace('<p class="text-lg text-gray-600 leading-relaxed">{{ problem_desc }}</p>',
                                  '<p class="text-base text-gray-600 leading-relaxed">{{ problem_desc }}</p>')
        
        content = content.replace('<span class="text-sm font-bold text-indigo-600 tracking-wider mb-2 block">{{ solution_pretitle }}</span>',
                                  '<span class="text-xs font-bold text-indigo-600 tracking-wider mb-2 block">{{ solution_pretitle }}</span>')
        content = content.replace('<h2 class="text-3xl md:text-4xl font-bold tracking-tighter text-gray-900 mb-4">{{ solution_title }}</h2>',
                                  '<h2 class="text-2xl md:text-3xl font-bold tracking-tighter text-gray-900 mb-3">{{ solution_title }}</h2>')
        content = content.replace('<p class="text-lg text-gray-600 leading-relaxed mb-6">{{ solution_desc }}</p>',
                                  '<p class="text-base text-gray-600 leading-relaxed mb-5">{{ solution_desc }}</p>')
    else:
        # Solution section literal text
        old_sol_pre = '<span class="text-sm font-bold text-indigo-600 tracking-wider mb-2 block">Respira Profundo</span>'
        new_sol_pre = '<span class="text-xs font-bold text-indigo-600 tracking-wider mb-2 block">Respira Profundo</span>'
        content = content.replace(old_sol_pre, new_sol_pre)

        old_sol_title = '<h2 class="text-3xl md:text-4xl font-bold tracking-tighter text-gray-900 mb-4">Crea tu Propio Santuario de Calma</h2>'
        new_sol_title = '<h2 class="text-2xl md:text-3xl font-bold tracking-tighter text-gray-900 mb-3">Crea tu Propio Santuario de Calma</h2>'
        content = content.replace(old_sol_title, new_sol_title)

        old_sol_desc = '<p class="text-lg text-gray-600 leading-relaxed mb-6">Presentamos nuestro Humidificador con Efecto Llama 3D. Una pieza de diseño que fusiona la aromaterapia terapéutica con un hipnótico efecto visual de llama, transformando cualquier espacio en un oasis de serenidad y bienestar.</p>'
        new_sol_desc = '<p class="text-base text-gray-600 leading-relaxed mb-5">Presentamos nuestro Humidificador con Efecto Llama 3D. Una pieza de diseño que fusiona la aromaterapia terapéutica con un hipnótico efecto visual de llama, transformando cualquier espacio en un oasis de serenidad y bienestar.</p>'
        content = content.replace(old_sol_desc, new_sol_desc)


    # While we are at it, let's also reduce the padding on the sections to match the smaller text
    # <section class="bg-gray-50/70 py-16 md:py-24"> -> py-12 md:py-16
    content = content.replace('<section class="bg-gray-50/70 py-16 md:py-24">', '<section class="bg-gray-50/70 py-12 md:py-16">')
    content = content.replace('<section class="container mx-auto px-6 py-16 md:py-24">', '<section class="container mx-auto px-6 py-12 md:py-16">')


    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Resized text in {filepath}")

resize_texts('index.html')
try:
    resize_texts('templates/landing.html')
except Exception as e:
    print(e)
