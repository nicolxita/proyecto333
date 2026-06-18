import re

def update_hero(filepath, is_template=False):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the main image container
    # For template: <img src="{{ image_assets[0] }}" ...>
    # For index: <img src="file:///C:/Users/Option/Documents/proyecto333/generated_assets/humidificador_difuso_image_0.jpg" ...>
    
    if is_template:
        img_src_0 = '{{ image_assets[0] }}'
        img_src_1 = '{% if image_assets|length > 1 %}{{ image_assets[1] }}{% else %}{{ image_assets[0] }}{% endif %}'
        img_src_2 = 'assets/bg_banner.jpg'
    else:
        # Extract actual image path from index.html
        m = re.search(r'<img src="(file://.*?/humidificador_difuso_image_0\.jpg)"', content)
        img_src_0 = m.group(1) if m else 'assets/bg_banner.jpg'
        
        m2 = re.search(r'<img src="(file://.*?/humidificador_difuso_image_1\.jpg)"', content)
        img_src_1 = m2.group(1) if m2 else img_src_0
        
        img_src_2 = 'assets/bg_banner.jpg'

    # The old left column:
    # <div class="w-full h-auto aspect-[4/5] sm:aspect-square bg-gray-50 rounded-3xl flex items-center justify-center overflow-hidden border border-gray-100 shadow-sm">
    #     <img src="..." alt="..." class="w-full h-full object-cover">
    # </div>
    
    left_col_pattern = r'<div class="w-full h-auto aspect-\[4/5\] sm:aspect-square bg-gray-50 rounded-3xl flex items-center justify-center overflow-hidden border border-gray-100 shadow-sm">\s*<img src=".*?" alt=".*?" class="w-full h-full object-cover">\s*</div>'

    new_left_col = f"""<div class="flex gap-3 md:gap-4 w-full max-w-lg mx-auto">
                    <!-- Thumbnails -->
                    <div class="w-16 md:w-20 flex flex-col gap-3 md:gap-4 shrink-0">
                        <button onclick="document.getElementById('main-product-image').src='{img_src_0}'" class="w-full aspect-square rounded-xl overflow-hidden border-2 border-indigo-600 hover:opacity-80 transition-opacity">
                            <img src="{img_src_0}" class="w-full h-full object-cover">
                        </button>
                        <button onclick="document.getElementById('main-product-image').src='{img_src_1}'" class="w-full aspect-square rounded-xl overflow-hidden border border-gray-200 hover:opacity-80 transition-opacity">
                            <img src="{img_src_1}" class="w-full h-full object-cover">
                        </button>
                        <button onclick="document.getElementById('main-product-image').src='{img_src_2}'" class="w-full aspect-square rounded-xl overflow-hidden border border-gray-200 hover:opacity-80 transition-opacity">
                            <img src="{img_src_2}" class="w-full h-full object-cover">
                        </button>
                    </div>
                    <!-- Main Image -->
                    <div class="flex-1 h-auto aspect-[4/5] sm:aspect-square bg-gray-50 rounded-3xl overflow-hidden border border-gray-100 shadow-sm relative">
                        <img id="main-product-image" src="{img_src_0}" alt="Producto" class="w-full h-full object-cover">
                    </div>
                </div>"""

    content = re.sub(left_col_pattern, new_left_col, content, count=1)

    # Now add the tiktok videos below the form.
    # The form is wrapped in:
    # <div>
    #     <div class="bg-white rounded-3xl p-5 md:p-6 shadow-xl border border-gray-100 max-w-[420px] w-full mx-auto">
    #         ...
    #     </div>
    # </div>
    # We will find the end of the form card by looking for the checkoutModal button or the safe purchase badges, 
    # then appending the TikTok div inside the right column wrapper.

    # Wait, the form card closes right after:
    # <div class="flex justify-center items-center gap-3 text-[10px] font-medium text-gray-500"> ... </div>
    # </div>
    # </div>
    
    tiktok_html = f"""
                        <div class="mt-6 flex justify-center gap-3 w-full max-w-[420px] mx-auto">
                            <div class="flex-1 aspect-[9/16] bg-gray-900 rounded-2xl overflow-hidden relative shadow-md group cursor-pointer">
                                <img src="{img_src_0}" class="w-full h-full object-cover opacity-70 group-hover:opacity-90 transition-opacity">
                                <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                                    <div class="bg-white/20 backdrop-blur-sm rounded-full p-2">
                                        <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6z"/></svg>
                                    </div>
                                </div>
                                <div class="absolute bottom-2 left-2 text-[8px] text-white font-bold flex items-center gap-1">
                                    <svg class="w-3 h-3 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/></svg>
                                    Ver en TikTok
                                </div>
                            </div>
                            <div class="flex-1 aspect-[9/16] bg-gray-900 rounded-2xl overflow-hidden relative shadow-md group cursor-pointer">
                                <img src="{img_src_1}" class="w-full h-full object-cover opacity-70 group-hover:opacity-90 transition-opacity">
                                <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                                    <div class="bg-white/20 backdrop-blur-sm rounded-full p-2">
                                        <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6z"/></svg>
                                    </div>
                                </div>
                                <div class="absolute bottom-2 left-2 text-[8px] text-white font-bold flex items-center gap-1">
                                    <svg class="w-3 h-3 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/></svg>
                                    Reseña de Cliente
                                </div>
                            </div>
                            <div class="flex-1 aspect-[9/16] bg-gray-900 rounded-2xl overflow-hidden relative shadow-md group cursor-pointer">
                                <img src="{img_src_2}" class="w-full h-full object-cover opacity-70 group-hover:opacity-90 transition-opacity">
                                <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                                    <div class="bg-white/20 backdrop-blur-sm rounded-full p-2">
                                        <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6z"/></svg>
                                    </div>
                                </div>
                                <div class="absolute bottom-2 left-2 text-[8px] text-white font-bold flex items-center gap-1">
                                    <svg class="w-3 h-3 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/></svg>
                                    Unboxing
                                </div>
                            </div>
                        </div>"""

    # We need to insert this right after the closing </div> of the form card.
    # The form card ends exactly after the 100% Segura / Paga Contra Entrega block.
    search_pattern = r'<span class="flex items-center gap-1">\s*<svg.*?</svg>\s*Paga Contra Entrega\s*</span>\s*</div>\s*</div>'
    replacement = r'\g<0>' + tiktok_html

    content = re.sub(search_pattern, replacement, content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

update_hero("templates/landing.html", is_template=True)
update_hero("index.html", is_template=False)

print("Hero layout updated with thumbnails and TikTok videos!")
