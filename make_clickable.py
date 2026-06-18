import re

def make_clickable(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Smooth scroll
    content = content.replace('<html lang="es">', '<html lang="es" class="scroll-smooth">')

    # 2. Add id="reviews" to social proof section
    # <section class="bg-[#F8F9FA] py-12 md:py-16">
    content = content.replace('<section class="bg-[#F8F9FA] py-12 md:py-16">', '<section id="reviews" class="bg-[#F8F9FA] py-12 md:py-16">')

    # 3. Replace the valoraciones div with an anchor tag
    # We want to replace:
    # <div class="flex items-center gap-2 mb-5 text-xs text-gray-600">
    #     <div class="flex text-amber-400 text-base">★★★★★</div>
    #     <span class="font-medium">(12.500+ valoraciones)</span>
    # </div>
    # Since the stars are actual star characters in the file, we can just use regex.

    old_div_pattern = r'<div class="flex items-center gap-2 mb-5 text-xs text-gray-600">\s*<div class="flex text-amber-400 text-base">.*?</div>\s*<span class="font-medium">\(12\.500\+ valoraciones\)</span>\s*</div>'
    
    new_a_tag = """<a href="#reviews" class="flex items-center gap-2 mb-5 text-xs text-gray-600 hover:text-indigo-600 transition-colors cursor-pointer w-fit group">
                            <div class="flex text-amber-400 text-base">★★★★★</div>
                            <span class="font-medium underline decoration-gray-300 underline-offset-2 group-hover:decoration-indigo-400 transition-colors">(12.500+ valoraciones)</span>
                        </a>"""
    
    content = re.sub(old_div_pattern, new_a_tag, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Made clickable in {filepath}")

make_clickable('index.html')
make_clickable('templates/landing.html')
