import re

def apply_real_tiktoks(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_ids = ['7263192751708130602', '7137111577060199686', '7434815922885512480']
    
    # We replaced them with 6718335390845095173 earlier
    # Let's replace them sequentially
    for new_id in new_ids:
        content = content.replace('6718335390845095173', new_id, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Applied real TikToks in {filepath}")

apply_real_tiktoks('index.html')
