import re
import urllib.parse

def update_whatsapp(filepath, product_name):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. New text
    if '{{ product_name }}' in product_name:
        raw_text = "¡Hola MUNDO AURA! tengo dudas sobre... {{ product_name }}"
        encoded_text = urllib.parse.quote("¡Hola MUNDO AURA! tengo dudas sobre... ") + "{{ product_name }}"
    else:
        raw_text = f"¡Hola MUNDO AURA! tengo dudas sobre... {product_name}"
        encoded_text = urllib.parse.quote(raw_text)

    # 2. Extract the current WhatsApp a-tag block
    # We look for <a href="https://wa.me/... </a>
    pattern = r'<!-- WhatsApp Floating Button -->\s*<a href="https://wa\.me/56979460119.*?</a>'
    
    new_html = f"""<!-- WhatsApp Floating Button -->
    <a href="https://wa.me/56979460119?text={encoded_text}" target="_blank" class="fixed bottom-6 right-6 z-50 transition-transform hover:scale-110 drop-shadow-2xl" aria-label="Chat on WhatsApp">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" class="w-14 h-14 md:w-16 md:h-16">
    </a>"""
    
    content = re.sub(pattern, new_html, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_whatsapp("index.html", "Humidificador Difusor Aromaterapia Llama 3D")
update_whatsapp("templates/landing.html", "{{ product_name }}")
print("WhatsApp updated!")
