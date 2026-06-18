import re

def fix_tiktok(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    bad_ids = ['7162235921868311854', '7181077755839204613', '7294819402111394851']
    valid_id = '6718335390845095173'

    for bad_id in bad_ids:
        content = content.replace(bad_id, valid_id)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed TikToks in {filepath}")

fix_tiktok('index.html')
