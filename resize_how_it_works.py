import re

def resize_how_it_works(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Main titles literal
    content = content.replace('<h2 class="text-3xl md:text-4xl font-bold tracking-tighter text-gray-900 mb-4">Simple, Intuitivo, Efectivo</h2>',
                              '<h2 class="text-2xl md:text-3xl font-bold tracking-tighter text-gray-900 mb-3">Simple, Intuitivo, Efectivo</h2>')
    content = content.replace('<p class="text-lg text-gray-600 leading-relaxed">Disfrutar de tu momento de calma es tan fácil como seguir estos tres pasos.</p>',
                              '<p class="text-base text-gray-600 leading-relaxed">Disfrutar de tu momento de calma es tan fácil como seguir estos tres pasos.</p>')

    # Main titles templates
    content = content.replace('<h2 class="text-3xl md:text-4xl font-bold tracking-tighter text-gray-900 mb-4">{{ how_it_works_title }}</h2>',
                              '<h2 class="text-2xl md:text-3xl font-bold tracking-tighter text-gray-900 mb-3">{{ how_it_works_title }}</h2>')
    content = content.replace('<p class="text-lg text-gray-600 leading-relaxed">{{ how_it_works_desc }}</p>',
                              '<p class="text-base text-gray-600 leading-relaxed">{{ how_it_works_desc }}</p>')

    # Steps literal
    # We will just regex replace the step titles to text-base instead of text-lg
    # <h3 class="font-bold text-lg mb-2">Paso 1: Añade Agua</h3>
    content = re.sub(r'<h3 class="font-bold text-lg mb-2">', r'<h3 class="font-bold text-base mb-2">', content)
    
    # Steps template
    content = content.replace('<h3 class="font-bold text-lg mb-2">{{ step.title }}</h3>',
                              '<h3 class="font-bold text-base mb-2">{{ step.title }}</h3>')

    # Note: text-sm for step description is already quite small, we'll leave it as text-sm.
    # The circle with numbers: text-xl -> text-lg
    content = content.replace('w-16 h-16 rounded-full flex items-center justify-center font-bold text-xl',
                              'w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg')
    # Actually wait, maybe just w-14 h-14 to not shrink it too much
    content = content.replace('w-16 h-16 rounded-full flex items-center justify-center font-bold text-xl text-gray-900 mb-4',
                              'w-12 h-12 mx-auto rounded-full flex items-center justify-center font-bold text-lg text-gray-900 mb-3')
                              
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Resized how it works in {filepath}")

resize_how_it_works('index.html')
try:
    resize_how_it_works('templates/landing.html')
except Exception as e:
    print(e)
