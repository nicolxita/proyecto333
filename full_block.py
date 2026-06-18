import re

def full_block(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The current structure is:
    # <div class="snap-center shrink-0 w-[325px] relative">
    #     <!-- Overlays anti-fuga -->
    #     <div class="absolute top-0 left-0 w-full h-[70px] z-20 bg-transparent cursor-default"></div>
    #     <div class="absolute bottom-0 left-0 w-full h-[90px] z-20 bg-transparent cursor-default"></div>
    #     <blockquote class="tiktok-embed" ...
    
    # Let's replace the overlays with a single full overlay
    old_overlays = r'<!-- Overlays anti-fuga -->\s*<div class="absolute top-0 left-0 w-full h-\[70px\] z-20 bg-transparent cursor-default"></div>\s*<div class="absolute bottom-0 left-0 w-full h-\[90px\] z-20 bg-transparent cursor-default"></div>'
    
    new_overlay = r'<!-- Escudo Total Anti-Fuga -->\n                        <div class="absolute inset-0 w-full h-full z-50 bg-transparent cursor-default"></div>'
    
    # We also might want to add pointer-events-none to the iframe, but we can't because it's cross-origin generated. The div overlay is the way.
    # We will use absolute inset-0 z-50.
    
    new_content = re.sub(old_overlays, new_overlay, content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Applied full block in {filepath}")
    else:
        print(f"Failed to find overlays in {filepath}")

full_block('index.html')
full_block('templates/landing.html')
