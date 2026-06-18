import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add overflow-x-hidden to body
    content = content.replace('<body class="bg-white text-gray-900 relative">', '<body class="bg-white text-gray-900 relative overflow-x-hidden">')

    # 2. Add min-w-0 to grid items to prevent blowout
    content = content.replace('<div class="lg:col-span-5 w-full lg:ml-0">', '<div class="lg:col-span-5 w-full lg:ml-0 min-w-0">')
    content = content.replace('<div class="lg:col-span-7 flex flex-col-reverse md:flex-row gap-3 md:gap-4 w-full max-w-2xl mx-auto lg:mr-0">', '<div class="lg:col-span-7 flex flex-col-reverse md:flex-row gap-3 md:gap-4 w-full max-w-2xl mx-auto lg:mr-0 min-w-0">')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filepath}")

fix_file('index.html')
fix_file('templates/landing.html')
