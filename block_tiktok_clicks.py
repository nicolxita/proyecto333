import re

def block_clicks(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the TikTok div wrapper
    # It looks like: <div class="snap-center shrink-0 w-[325px]">
    # We want to replace it with a relative wrapper and add overlays inside.
    
    # We can use regex to find:
    # <div class="snap-center shrink-0 w-\[325px\]">\s*<blockquote class="tiktok-embed"
    # And replace with the new structure.

    pattern = r'(<div class="snap-center shrink-0 w-\[325px\]">)(\s*<blockquote class="tiktok-embed")'
    
    # We add relative to the wrapper class
    replacement = r'<div class="snap-center shrink-0 w-[325px] relative">\n                        <!-- Overlays anti-fuga -->\n                        <div class="absolute top-0 left-0 w-full h-[70px] z-20 bg-transparent cursor-default"></div>\n                        <div class="absolute bottom-0 left-0 w-full h-[90px] z-20 bg-transparent cursor-default"></div>\2'
    
    new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Added click-blockers in {filepath}")
    else:
        print(f"Pattern not found in {filepath} or already applied.")

block_clicks('index.html')
block_clicks('templates/landing.html')
