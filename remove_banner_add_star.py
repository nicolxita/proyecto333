import re

def update_header_and_banner(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove the side banner
    # It looks like:
    # <!-- Background side banner -->
    # <div class="absolute top-0 left-0 w-[120px] xl:w-[180px] ...
    #     <img src="assets/bg_banner.jpg" ...
    #     <!-- Vertical fade out to white at the bottom -->
    #     <div class="absolute bottom-0 left-0 w-full h-[300px] bg-gradient-to-t from-white to-transparent"></div>
    # </div>
    
    pattern_banner = r'<!-- Background side banner -->\s*<div class="absolute top-0 left-0[^>]+>.*?</div>\s*</div>'
    content = re.sub(pattern_banner, '', content, flags=re.DOTALL)

    # 2. Update Header class to remove the pseudo-elements for the banner border gap
    old_header = '<header class="sticky top-0 z-40 bg-white/80 backdrop-blur-lg after:absolute after:bottom-0 after:right-0 after:w-full lg:after:w-[calc(100%-120px)] xl:after:w-[calc(100%-180px)] after:border-b after:border-gray-100">'
    new_header = '<header class="sticky top-0 z-40 bg-white/80 backdrop-blur-lg border-b border-gray-100">'
    content = content.replace(old_header, new_header)

    # 3. Add the estrella image to the title
    old_title = '<h2 class="text-xl font-bold tracking-tight">MUNDO AURA</h2>'
    new_title = '<h2 class="text-xl font-bold tracking-tight flex items-center">MUNDO <img src="assets/estrella.jpg" alt="*" class="h-5 w-auto object-contain mx-1.5 -mt-0.5 rounded-sm"> AURA</h2>'
    content = content.replace(old_title, new_title)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

update_header_and_banner("index.html")
update_header_and_banner("templates/landing.html")
