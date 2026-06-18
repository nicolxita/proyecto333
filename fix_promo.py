import re

def fix_promo_selection(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace the labels block
    old_labels = """<div class="grid grid-cols-2 gap-2">
                            <label class="relative border-2 border-indigo-600 bg-indigo-50/30 rounded-xl p-2 cursor-pointer flex flex-col items-center justify-center text-center hover:border-indigo-500 transition-colors">
                                <input type="radio" name="promo" class="hidden" checked>
                                <span class="block text-xs font-bold text-gray-900 mb-0.5">Llevar 1 Unidad</span>
                                <span class="block text-[10px] text-gray-500 mb-1">Precio Unitario</span>
                                <span class="block font-extrabold text-emerald-600 text-base">{{ offer_price }}</span>
                            </label>
                            <label class="relative border-2 border-gray-100 rounded-xl p-2 cursor-pointer flex flex-col items-center justify-center text-center hover:border-indigo-400 transition-colors">
                                <input type="radio" name="promo" class="hidden">
                                <span class="block text-xs font-bold text-gray-600 mb-0.5">Llevar 2 Unidades</span>
                                <span class="block text-[10px] text-indigo-600 font-bold mb-1">Segunda al 50%</span>
                                <span class="block font-extrabold text-gray-900 text-base">{{ promo_2_price }}</span>
                            </label>
                            </div>"""

    new_labels = """<div class="grid grid-cols-2 gap-2" id="promo-selector">
                            <label onclick="selectPromo(1, '{{ offer_price }}')" id="label-promo-1" class="relative border-2 border-indigo-600 bg-indigo-50/30 rounded-xl p-2 cursor-pointer flex flex-col items-center justify-center text-center transition-colors">
                                <input type="radio" name="promo" value="1" class="hidden" checked>
                                <span class="block text-xs font-bold text-gray-900 mb-0.5">Llevar 1 Unidad</span>
                                <span class="block text-[10px] text-gray-500 mb-1">Precio Unitario</span>
                                <span class="block font-extrabold text-emerald-600 text-base">{{ offer_price }}</span>
                            </label>
                            <label onclick="selectPromo(2, '{{ promo_2_price }}')" id="label-promo-2" class="relative border-2 border-gray-100 rounded-xl p-2 cursor-pointer flex flex-col items-center justify-center text-center transition-colors hover:border-indigo-400">
                                <input type="radio" name="promo" value="2" class="hidden">
                                <span class="block text-xs font-bold text-gray-600 mb-0.5">Llevar 2 Unidades</span>
                                <span class="block text-[10px] text-indigo-600 font-bold mb-1">Segunda al 50%</span>
                                <span class="block font-extrabold text-gray-900 text-base">{{ promo_2_price }}</span>
                            </label>
                            </div>"""
    
    # Check if the content is exactly matched, or we can use regex if spaces differ
    content = content.replace(old_labels, new_labels)

    # In case of minor spacing differences, let's use a regex fallback
    if "selectPromo(" not in content:
        content = re.sub(
            r'<div class="grid grid-cols-2 gap-2">\s*<label class="relative border-2 border-indigo-600.*?</label>\s*<label class="relative border-2 border-gray-100.*?</label>\s*</div>',
            new_labels, content, flags=re.DOTALL
        )

    # Replace modal units and price ids
    old_modal_units = '<span class="block text-[10px] text-gray-500 mt-0.5">1 Unidad</span>'
    new_modal_units = '<span id="modal-units" class="block text-[10px] text-gray-500 mt-0.5">1 Unidad</span>'
    content = content.replace(old_modal_units, new_modal_units)

    old_modal_price = '<span class="block text-base font-bold text-emerald-600">{{ offer_price }}</span>'
    new_modal_price = '<span id="modal-price" class="block text-base font-bold text-emerald-600">{{ offer_price }}</span>'
    content = content.replace(old_modal_price, new_modal_price)

    # Add the JavaScript function before the existing submitCODOrder script
    script_insertion = """<script>
        let selectedUnits = '1 Unidad';
        let selectedPrice = '{{ offer_price }}';

        function selectPromo(units, price) {
            selectedUnits = units === 1 ? '1 Unidad' : '2 Unidades';
            selectedPrice = price;
            
            const label1 = document.getElementById('label-promo-1');
            const label2 = document.getElementById('label-promo-2');
            
            if (units === 1) {
                label1.className = 'relative border-2 border-indigo-600 bg-indigo-50/30 rounded-xl p-2 cursor-pointer flex flex-col items-center justify-center text-center transition-colors';
                label2.className = 'relative border-2 border-gray-100 rounded-xl p-2 cursor-pointer flex flex-col items-center justify-center text-center transition-colors hover:border-indigo-400';
            } else {
                label2.className = 'relative border-2 border-indigo-600 bg-indigo-50/30 rounded-xl p-2 cursor-pointer flex flex-col items-center justify-center text-center transition-colors';
                label1.className = 'relative border-2 border-gray-100 rounded-xl p-2 cursor-pointer flex flex-col items-center justify-center text-center transition-colors hover:border-indigo-400';
            }

            const modalUnits = document.getElementById('modal-units');
            const modalPrice = document.getElementById('modal-price');
            if (modalUnits) modalUnits.innerText = selectedUnits;
            if (modalPrice) modalPrice.innerText = selectedPrice;
        }

        function submitCODOrder(event) {"""
    
    content = content.replace("<script>\n        function submitCODOrder(event) {", script_insertion)

    # Note: index.html has concrete values for offer_price, but we should do regex replace for index.html if needed.
    # Ah, index.html has "$34.990" instead of "{{ offer_price }}" !!
    # So for index.html we must apply the changes with regex.
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

fix_promo_selection("templates/landing.html")

print("Templates updated!")
