import re

# Update index.html
def update_index_faq(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_q = '<span class="font-medium text-gray-900">¿Ofrecen pago contra entrega?</span>'
    new_q = '<span class="font-medium text-gray-900">¿Qué significa que sea pago contra entrega?</span>'
    
    old_a = '<p class="text-gray-600 mt-3 text-sm leading-relaxed">Sí, para tu comodidad y seguridad, ofrecemos la opción de pago contra entrega en la Región Metropolitana. Pagas al recibir tu producto en la puerta de tu casa.</p>'
    new_a = '<p class="text-gray-600 mt-3 text-sm leading-relaxed">Significa que tu compra es 100% libre de riesgos. Haces tu pedido ahora sin pagar nada por adelantado, y solo pagas en efectivo o transferencia cuando el repartidor te entrega el producto en tus manos.</p>'

    content = content.replace(old_q, new_q)
    content = content.replace(old_a, new_a)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated index FAQ in {filepath}")

# Update agents/devops.py prompt
def update_devops_prompt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_prompt = '8. FAQs: 5-8 frequently asked questions. MUST include one about "Pago Contra Entrega" and shipping times.'
    new_prompt = '8. FAQs: 5-8 frequently asked questions. MUST include one exactly with the question: "¿Qué significa que sea pago contra entrega?" and the answer MUST briefly explain that they order now without paying, and only pay (cash/transfer) when they receive the product in their hands.'
    
    content = content.replace(old_prompt, new_prompt)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated devops prompt in {filepath}")

update_index_faq('index.html')
try:
    update_devops_prompt('agents/devops.py')
except Exception as e:
    print(e)
