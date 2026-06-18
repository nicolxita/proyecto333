import re

def simplify_texts(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define old and new texts
    replacements = {
        # Problem
        'El estrés diario, la ansiedad y la dificultad para desconectar se han vuelto la norma. Tu hogar, que debería ser tu refugio, a menudo no logra ofrecer esa calma que tanto necesitas para recargar energías.': 'El estrés diario no te deja desconectar. Tu hogar debería ser tu refugio, un lugar para recargar energías de verdad.',
        
        # Solution
        'Presentamos nuestro Humidificador con Efecto Llama 3D. Una pieza de diseño que fusiona la aromaterapia terapéutica con un hipnótico efecto visual de llama, transformando cualquier espacio en un oasis de serenidad y bienestar.': 'Una pieza de diseño que fusiona aromaterapia con un hipnótico efecto de llama. Transforma cualquier espacio en tu oasis de calma.',
        
        # Benefits
        'Más que un humidificador, es una experiencia sensorial diseñada para elevar tu día a día.': 'Una experiencia diseñada para elevar tu bienestar diario.'
    }

    for old_text, new_text in replacements.items():
        content = content.replace(old_text, new_text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Simplified texts in {filepath}")

simplify_texts('index.html')
try:
    simplify_texts('templates/landing.html')
except Exception as e:
    print(e)
