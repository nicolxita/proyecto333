import re

def update_header(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the header container width
    # From <div class="container mx-auto px-6 py-4 flex justify-between items-center">
    # To <div class="w-full px-6 md:px-10 lg:px-16 py-4 flex justify-between items-center">
    content = content.replace(
        '<div class="container mx-auto px-6 py-4 flex justify-between items-center">',
        '<div class="w-full px-6 md:px-10 lg:px-16 py-4 flex justify-between items-center">'
    )

    # 2. Increase title size
    # From <h2 class="text-xl font-bold tracking-tight flex items-center">
    # To <h2 class="text-3xl font-extrabold tracking-tight flex items-center">
    content = content.replace(
        '<h2 class="text-xl font-bold tracking-tight flex items-center">',
        '<h2 class="text-3xl font-extrabold tracking-tight flex items-center">'
    )

    # 3. Increase star image size
    # From class="h-5 w-auto object-contain mx-1.5 -mt-0.5 rounded-sm"
    # To class="h-8 w-auto object-contain mx-2 -mt-1 rounded-sm"
    content = content.replace(
        'class="h-5 w-auto object-contain mx-1.5 -mt-0.5 rounded-sm"',
        'class="h-8 w-auto object-contain mx-2 -mt-1 rounded-sm"'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated header in {filepath}")

update_header("index.html")
update_header("templates/landing.html")
