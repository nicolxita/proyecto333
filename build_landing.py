import json
import os
import sys

def build_landing(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        
    with open("templates/landing.html", "r", encoding="utf-8") as f:
        template = f.read()
        
    for key, value in config.items():
        template = template.replace(f"{{{{ {key} }}}}", value)
        
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(template)
        
    print(f"✅ index.html generated successfully for {config.get('short_name')}!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        build_landing(sys.argv[1])
    else:
        print("Usage: python build_landing.py <config.json>")
