import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update image paths
    # Replace absolute generated_assets paths
    content = re.sub(r"file:///C:/Users/Option/Documents/proyecto333/generated_assets/humidificador_difuso_image_0\.jpg", "assets/real_humidifier_1.png", content)
    content = re.sub(r"file:///C:/Users/Option/Documents/proyecto333/generated_assets/humidificador_difuso_image_1\.jpg", "assets/real_humidifier_2.png", content)
    content = re.sub(r"assets/bg_banner\.jpg", "assets/real_humidifier_3.png", content)

    # Replace generated_assets if they appear without file:///
    content = re.sub(r"generated_assets/humidificador_difuso_image_0\.jpg", "assets/real_humidifier_1.png", content)
    content = re.sub(r"generated_assets/humidificador_difuso_image_1\.jpg", "assets/real_humidifier_2.png", content)

    # 2. Add UGC Section
    # Find Social Proof section and replace it
    ugc_section = """        <!-- UGC / TikTok Section -->
        <section class="bg-gray-900 py-16 md:py-24 text-white relative">
            <div class="container mx-auto px-6 relative z-10">
                <div class="text-center mb-12">
                    <span class="text-pink-400 font-bold tracking-wider uppercase text-sm mb-2 block">Se volvió viral 🔥</span>
                    <h2 class="text-3xl md:text-4xl font-extrabold tracking-tighter mb-4">Lo que todos dicen en TikTok</h2>
                    <p class="text-gray-300 max-w-2xl mx-auto">Únete a las miles de personas que ya están transformando sus habitaciones en un oasis de calma.</p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
                    <!-- TikTok 1 -->
                    <div class="bg-white/5 rounded-3xl p-4 backdrop-blur-sm border border-white/10 flex justify-center shadow-2xl">
                        <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@daniel.ecommerceshopify/video/7649734220826381590" data-video-id="7649734220826381590" style="max-width: 325px; min-width: 325px;">
                            <section> <a target="_blank" title="@daniel.ecommerceshopify" href="https://www.tiktok.com/@daniel.ecommerceshopify">@daniel.ecommerceshopify</a> </section>
                        </blockquote>
                    </div>
                    <!-- TikTok 2 -->
                    <div class="bg-white/5 rounded-3xl p-4 backdrop-blur-sm border border-white/10 flex justify-center shadow-2xl md:transform md:-translate-y-4">
                        <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@daniel.ecommerceshopify/video/7649734220826381590" data-video-id="7649734220826381590" style="max-width: 325px; min-width: 325px;">
                            <section> <a target="_blank" title="@daniel.ecommerceshopify" href="https://www.tiktok.com/@daniel.ecommerceshopify">@daniel.ecommerceshopify</a> </section>
                        </blockquote>
                    </div>
                    <!-- TikTok 3 -->
                    <div class="bg-white/5 rounded-3xl p-4 backdrop-blur-sm border border-white/10 flex justify-center shadow-2xl">
                        <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@daniel.ecommerceshopify/video/7649734220826381590" data-video-id="7649734220826381590" style="max-width: 325px; min-width: 325px;">
                            <section> <a target="_blank" title="@daniel.ecommerceshopify" href="https://www.tiktok.com/@daniel.ecommerceshopify">@daniel.ecommerceshopify</a> </section>
                        </blockquote>
                    </div>
                </div>
            </div>
            <!-- TikTok Script -->
            <script async src="https://www.tiktok.com/embed.js"></script>
        </section>"""

    # We want to replace the whole "7. Social Proof" section.
    # It starts at "<!-- 7. Social Proof -->" and ends at "</section>" before "</main>"
    
    # Let's find "<!-- 7. Social Proof -->"
    start_idx = content.find("<!-- 7. Social Proof -->")
    if start_idx != -1:
        # Find the end of the section (the next </section> after start_idx)
        end_idx = content.find("</section>", start_idx)
        if end_idx != -1:
            end_idx += len("</section>")
            content = content[:start_idx] + ugc_section + "\n" + content[end_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

update_file("index.html")
update_file("templates/landing.html")
