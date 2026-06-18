import re

def remove_highlights(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of the Feature Highlights section
    start_str = "<!-- 6. Feature Highlights -->"
    start_idx = content.find(start_str)
    
    if start_idx != -1:
        # Find the next section comment, e.g., <!-- 8. Objection Handling Section -->
        # or just find the closing </section> of this section.
        # But wait, there might be other </section> tags inside if we're not careful.
        # Actually, in the HTML, the section is a single <section> tag containing <divs>.
        # So finding the next "<!-- " is safer.
        next_section_idx = content.find("<!--", start_idx + len(start_str))
        
        if next_section_idx != -1:
            content = content[:start_idx] + content[next_section_idx:]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Removed Highlights from {filepath}")
        else:
            print(f"Could not find end of section in {filepath}")
    else:
        # Maybe the user already removed the comment or it's named differently.
        # Let's search for the jinja block if it's templates/landing.html
        if "{% if highlights and highlights|length >= 2 %}" in content:
            # We can use regex to remove the entire section containing it
            content = re.sub(r'<!-- 6\. Feature Highlights -->.*?<!--', '<!--', content, flags=re.DOTALL)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Removed Highlights Jinja block from {filepath}")
        else:
            print(f"Highlights section not found in {filepath}")

remove_highlights('index.html')
try:
    remove_highlights('templates/landing.html')
except Exception as e:
    print(e)
