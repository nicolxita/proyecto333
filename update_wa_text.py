import urllib.parse

def update_wa_text(filepath, product_name):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_href = 'href="https://wa.me/56979460119"'
    
    # Create the predefined text
    if '{{ product_name }}' in product_name:
        # In jinja template we just leave the variable
        text = "¡Hola! Vengo de la tienda y me interesa el producto: {{ product_name }}"
    else:
        text = f"¡Hola! Vengo de la tienda y me interesa el producto: {product_name}"
    
    # URL encode the text, but keep {{ and }} unencoded for Jinja if possible, 
    # actually Jinja works fine even if it's url encoded, but browsers parse it better if the whole string is encoded except we can't encode {{ product_name }} before Jinja evaluates it.
    # Wait, if we use {{ product_name|urlencode }}, it's safer.
    # For simplicity, let's just use regular URL encoding for the static part.
    
    if is_template:
        encoded_text = urllib.parse.quote("¡Hola! Vengo de la tienda y me interesa el producto: ") + "{{ product_name }}"
    else:
        encoded_text = urllib.parse.quote(text)

    new_href = f'href="https://wa.me/56979460119?text={encoded_text}"'
    
    content = content.replace(old_href, new_href)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

is_template = False
update_wa_text("index.html", "Humidificador Difusor Aromaterapia Llama 3D")
is_template = True
update_wa_text("templates/landing.html", "{{ product_name }}")
print("WhatsApp links updated!")
