import re

def resize_tiktok(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change wrapper width
    content = content.replace('w-[260px] md:w-[280px]', 'w-[220px] md:w-[240px]')
    
    # Change iframe height
    content = content.replace('height: 480px;', 'height: 410px;')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Resized TikToks in {filepath}")

resize_tiktok('index.html')
resize_tiktok('templates/landing.html')
