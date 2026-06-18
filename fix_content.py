import re

def fix_content(filepath, is_template=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Shipping text
    if is_template:
        old_shipping = r'Envío Gratis asegurado: Recíbelo entre el <strong class="font-bold">\{\{ fecha_inicio \}\}</strong> y el <strong class="font-bold">\{\{ fecha_fin \}\}</strong>'
    else:
        old_shipping = r'Envío Gratis asegurado: Recíbelo entre el <strong class="font-bold">.*?</strong> y el <strong class="font-bold">.*?</strong>'
    
    new_shipping = r'Envío Gratis asegurado: Recíbelo en <strong class="font-bold">24 a 48 horas en RM</strong> y de <strong class="font-bold">3 a 5 días en regiones</strong>.'
    
    content = re.sub(old_shipping, new_shipping, content)

    # 2. Fix TikTok URLs
    # Since I don't want to use regex for the precise IDs, I'll just use string replace.
    replacements = {
        'cite="https://www.tiktok.com/@tiktok/video/7263192751708130602"': 'cite="https://www.tiktok.com/@diffuserpro2/video/7263192751708130602"',
        'cite="https://www.tiktok.com/@tiktok/video/7137111577060199686"': 'cite="https://www.tiktok.com/@eskahome/video/7137111577060199686"',
        'cite="https://www.tiktok.com/@tiktok/video/7434815922885512480"': 'cite="https://www.tiktok.com/@vaperwave/video/7434815922885512480"'
    }

    # For the template, the first part is a Jinja loop so we can't hardcode the cite in the loop.
    # Wait, in the loop: cite="https://www.tiktok.com/@tiktok/video/{{ video_id }}"
    # We should change it so that the agent provides the FULL URL or we just keep it as @tiktok in the loop, or better:
    # "cite="https://www.tiktok.com/video/{{ video_id }}"" (TikTok will redirect automatically to the correct creator if we omit the username or use a placeholder like @creator).
    # The user asked: "Cuando tu agente te consiga los 3 videos UGC perfectos del humidificador, recuerda reemplazar dos cosas en cada bloque:El enlace en el atributo cite="...". El número largo en el atributo data-video-id="..."
    # If the user is telling me what to do "when my agent gets them", the agent needs to return either the full URL or username.
    # Actually, the user says "reemplazar dos cosas en cada bloque". For now, they are hardcoded as fallbacks, so I'll replace the fallbacks in the template and the hardcoded ones in index.html.
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    # In templates/landing.html, the loop has: cite="https://www.tiktok.com/@tiktok/video/{{ video_id }}"
    # We can change it to cite="https://www.tiktok.com/@user/video/{{ video_id }}" so it's a generic placeholder that the embed.js will resolve.
    content = content.replace('cite="https://www.tiktok.com/@tiktok/video/{{ video_id }}"', 'cite="https://www.tiktok.com/@user/video/{{ video_id }}"')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed content in {filepath}")

fix_content('index.html', is_template=False)
fix_content('templates/landing.html', is_template=True)
