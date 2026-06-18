import re

def move_tiktok(filepath, is_template=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Delete the old TikTok div block
    if is_template:
        old_pattern = r'<div class="mt-16 w-full max-w-5xl mx-auto text-center">.*?<style>\s*\.mt-8 \.flex::.*?display: none; \}\s*</style>'
    else:
        old_pattern = r'<div class="mt-16 w-full max-w-5xl mx-auto text-center">.*?<style>\s*\.mt-8 \.flex::.*?display: none; \}\s*</style>'

    # Also need to remove the embed.js if it's there
    content = re.sub(old_pattern, '', content, flags=re.DOTALL)
    # the embed.js might be matched or maybe not? Wait, the regex includes it if it's between div and style.
    
    # Let's use a simpler pattern to just nuke the old div exactly.
    # The div starts with <div class="mt-16 w-full max-w-5xl mx-auto text-center">
    # and we want to remove everything up to right before </section>
    
    content = re.sub(r'<div class="mt-16 w-full max-w-5xl mx-auto text-center">.*?(?=</section>)', '', content, flags=re.DOTALL)

    # 2. Add the new TikTok section right after the Social Proof section
    if is_template:
        new_section = """
        <!-- NUEVA SECCIÓN DE VIDEOS TIKTOK -->
        <section class="py-12 md:py-16 bg-white">
            <div class="container mx-auto px-6 text-center max-w-5xl">
                <h3 class="text-2xl md:text-3xl font-extrabold text-gray-900 mb-3 tracking-tighter">Lo que todos dicen en TikTok</h3>
                <p class="text-base text-gray-600 mb-10 max-w-2xl mx-auto">Videos reales de nuestra comunidad probando el efecto llama 3D.</p>
                
                <div class="flex overflow-x-auto justify-start lg:justify-center gap-6 snap-x snap-mandatory pb-6 px-4" style="-ms-overflow-style: none; scrollbar-width: none;">
                    {% if tiktok_videos %}
                        {% for video_id in tiktok_videos %}
                        <div class="snap-center shrink-0 w-[325px]">
                            <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@tiktok/video/{{ video_id }}" data-video-id="{{ video_id }}" style="max-width: 100%; min-width: 325px; margin: 0; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                                <section></section>
                            </blockquote>
                        </div>
                        {% endfor %}
                    {% else %}
                        <!-- Fallback TikToks -->
                        <div class="snap-center shrink-0 w-[325px]">
                            <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@tiktok/video/7263192751708130602" data-video-id="7263192751708130602" style="max-width: 100%; min-width: 325px; margin: 0; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                                <section></section>
                            </blockquote>
                        </div>
                        <div class="snap-center shrink-0 w-[325px]">
                            <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@tiktok/video/7137111577060199686" data-video-id="7137111577060199686" style="max-width: 100%; min-width: 325px; margin: 0; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                                <section></section>
                            </blockquote>
                        </div>
                        <div class="snap-center shrink-0 w-[325px]">
                            <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@tiktok/video/7434815922885512480" data-video-id="7434815922885512480" style="max-width: 100%; min-width: 325px; margin: 0; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                                <section></section>
                            </blockquote>
                        </div>
                    {% endif %}
                </div>
            </div>
            <script async src="https://www.tiktok.com/embed.js"></script>
        </section>
"""
    else:
        new_section = """
        <!-- NUEVA SECCIÓN DE VIDEOS TIKTOK -->
        <section class="py-12 md:py-16 bg-white">
            <div class="container mx-auto px-6 text-center max-w-5xl">
                <h3 class="text-2xl md:text-3xl font-extrabold text-gray-900 mb-3 tracking-tighter">Lo que todos dicen en TikTok</h3>
                <p class="text-base text-gray-600 mb-10 max-w-2xl mx-auto">Videos reales de nuestra comunidad probando el efecto llama 3D.</p>
                
                <div class="flex overflow-x-auto justify-start lg:justify-center gap-6 snap-x snap-mandatory pb-6 px-4" style="-ms-overflow-style: none; scrollbar-width: none;">
                    <!-- TikTok 1 -->
                    <div class="snap-center shrink-0 w-[325px]">
                        <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@tiktok/video/7263192751708130602" data-video-id="7263192751708130602" style="max-width: 100%; min-width: 325px; margin: 0; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                            <section></section>
                        </blockquote>
                    </div>
                    <!-- TikTok 2 -->
                    <div class="snap-center shrink-0 w-[325px]">
                        <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@tiktok/video/7137111577060199686" data-video-id="7137111577060199686" style="max-width: 100%; min-width: 325px; margin: 0; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                            <section></section>
                        </blockquote>
                    </div>
                    <!-- TikTok 3 -->
                    <div class="snap-center shrink-0 w-[325px]">
                        <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@tiktok/video/7434815922885512480" data-video-id="7434815922885512480" style="max-width: 100%; min-width: 325px; margin: 0; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                            <section></section>
                        </blockquote>
                    </div>
                </div>
            </div>
            <script async src="https://www.tiktok.com/embed.js"></script>
        </section>
"""

    if "<!-- NUEVA SECCIÓN DE VIDEOS TIKTOK -->" in content:
        print(f"Already moved in {filepath}")
        return

    # Find where social proof ends:
    # "<!-- 2. Problem Section -->" or "<!-- Social Proof Section --> ... </section>"
    # Let's just insert before "<!-- 2. Problem Section -->"
    pattern2 = r'(\s*<!-- 2\. Problem Section -->)'
    content = re.sub(pattern2, '\n' + new_section + r'\1', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Moved tiktok in {filepath}")

move_tiktok('index.html', is_template=False)
move_tiktok('templates/landing.html', is_template=True)
