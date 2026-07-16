# Update rating to 4.9/5.0, bought count to 931+ han comprado, and banner to show -25% OFERTA solo por hoy (in rose-600) & PAGALO EN TU CASA
import re

def update_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Define old and new sections for replacement
    
    # 1. Update index.html style ratings block (pre-update version)
    old_index_a = """                        <a href="#reviews"
                            class="flex items-center gap-2 mb-5 text-xs text-gray-600 hover:text-indigo-600 transition-colors cursor-pointer w-fit group flex-wrap">
                            <div class="flex text-amber-400 text-base">★★★★★</div>
                            <span
                                class="font-medium underline decoration-gray-300 underline-offset-2 group-hover:decoration-indigo-400 transition-colors">(184
                                valoraciones)</span>
                            <span class="text-gray-300 font-light">|</span>
                            <span class="flex items-center gap-1 text-gray-500 no-underline font-medium">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                                <span><strong class="text-gray-700">932</strong> personas han comprado</span>
                            </span>
                        </a>"""

    new_index_a = """                        <a href="#reviews"
                            class="flex items-center gap-2 mb-5 text-xs text-gray-600 hover:text-indigo-600 transition-colors cursor-pointer w-fit group flex-wrap">
                            <div class="flex text-amber-400 text-base">★★★★★</div>
                            <span class="font-semibold text-gray-800">4.9/5.0</span>
                            <span
                                class="font-medium underline decoration-gray-300 underline-offset-2 group-hover:decoration-indigo-400 transition-colors">(184
                                valoraciones)</span>
                            <span class="text-gray-300 font-light">|</span>
                            <span class="flex items-center gap-1 text-gray-500 no-underline font-medium">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                                <span><strong class="text-gray-700">931+</strong> han comprado</span>
                            </span>
                        </a>"""

    # 2. Update landing.html style ratings block (pre-update version)
    old_landing_a = """                        <a href="#reviews" class="flex items-center gap-2 mb-5 text-xs text-gray-600 hover:text-indigo-600 transition-colors cursor-pointer w-fit group">
                            <div class="flex text-amber-400 text-base">★★★★★</div>
                            <span class="font-medium underline decoration-gray-300 underline-offset-2 group-hover:decoration-indigo-400 transition-colors">(184 valoraciones)</span>
                        </a>"""

    new_landing_a = """                        <a href="#reviews" class="flex items-center gap-2 mb-5 text-xs text-gray-600 hover:text-indigo-600 transition-colors cursor-pointer w-fit group flex-wrap">
                            <div class="flex text-amber-400 text-base">★★★★★</div>
                            <span class="font-semibold text-gray-800">4.9/5.0</span>
                            <span class="font-medium underline decoration-gray-300 underline-offset-2 group-hover:decoration-indigo-400 transition-colors">(184 valoraciones)</span>
                            <span class="text-gray-300 font-light">|</span>
                            <span class="flex items-center gap-1 text-gray-500 no-underline font-medium">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                                <span><strong class="text-gray-700">931+</strong> han comprado</span>
                            </span>
                        </a>"""

    # Replace rating blocks
    if old_index_a in html:
        html = html.replace(old_index_a, new_index_a)
        print(f"Updated index rating block in {filepath}")
    elif old_landing_a in html:
        html = html.replace(old_landing_a, new_landing_a)
        print(f"Updated landing rating block in {filepath}")
    else:
        print(f"No match found for rating blocks in {filepath} (potentially already updated)")

    # 3. Replace marquee banner block using regular expression for absolute safety
    banner_pattern = r'(<!-- Moving Banner \(Now Above Header\) -->\s*<div class="bg-gray-50 border-b border-gray-200/50 overflow-hidden relative z-50 w-full">\s*<div class="marquee-content whitespace-nowrap py-1">).*?(<\/div>\s*<\/div>)'
    
    new_marquee_inner = """
            <p class="text-[11px] font-medium text-gray-900/50 px-6 tracking-widest"><span class="text-rose-600 font-bold">-25% OFERTA SOLO POR HOY</span> ✦ ENVÍO GRATIS A TODO CHILE ✦ PÁGALO EN TU CASA ✦</p>
            <p class="text-[11px] font-medium text-gray-900/50 px-6 tracking-widest"><span class="text-rose-600 font-bold">-25% OFERTA SOLO POR HOY</span> ✦ ENVÍO GRATIS A TODO CHILE ✦ PÁGALO EN TU CASA ✦</p>
            <p class="text-[11px] font-medium text-gray-900/50 px-6 tracking-widest"><span class="text-rose-600 font-bold">-25% OFERTA SOLO POR HOY</span> ✦ ENVÍO GRATIS A TODO CHILE ✦ PÁGALO EN TU CASA ✦</p>
            <p class="text-[11px] font-medium text-gray-900/50 px-6 tracking-widest"><span class="text-rose-600 font-bold">-25% OFERTA SOLO POR HOY</span> ✦ ENVÍO GRATIS A TODO CHILE ✦ PÁGALO EN TU CASA ✦</p>
        """
    
    html = re.sub(banner_pattern, rf'\g<1>{new_marquee_inner}\g<2>', html, flags=re.DOTALL)
    print(f"Substituted marquee banner block in {filepath}")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

update_file("index.html")
update_file("templates/landing.html")
print("Update 19 complete")
