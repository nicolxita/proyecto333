import re

def fix_script(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The exact script tag to look for
    script_tag = '<script async src="https://www.tiktok.com/embed.js"></script>'
    
    # Check if it exists
    count = content.count(script_tag)
    if count == 0:
        print(f"No scripts found in {filepath}, nothing to do.")
        return
        
    print(f"Found {count} script tags in {filepath}. Removing them and placing one at the end.")
    
    # Remove all occurrences
    content = content.replace(script_tag, '')
    
    # Also remove any empty lines left over, but not critical
    
    # Now add exactly one right before </body>
    if '</body>' in content:
        content = content.replace('</body>', f'    {script_tag}\n</body>')
    else:
        # Just append it if </body> isn't found (unlikely)
        content += f'\n{script_tag}\n'
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filepath}")

fix_script('index.html')
fix_script('templates/landing.html')
