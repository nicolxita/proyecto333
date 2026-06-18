import re

def fix_tiktok_size(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # We are looking for:
        # <div class="snap-center shrink-0 w-[220px] md:w-[240px]">
        #     <iframe src="https://www.tiktok.com/embed/v2/{{ video_id }}" style="width: 100%; height: 410px; border: none; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);" allowfullscreen></iframe>
        # </div>
        
        # In index.html, it's hardcoded IDs. In landing.html, it might have Jinja.
        # Let's just find all div wrappers of iframes containing tiktok.com.
        
        pattern = r'<div class="snap-center shrink-0 [^>]*">\s*<iframe src="(https://www\.tiktok\.com/embed/v2/[^"]+)" style="[^"]*" allowfullscreen></iframe>\s*</div>'
        
        def repl(match):
            src = match.group(1)
            return f"""<div class="snap-center shrink-0 w-[227px] h-[406px] relative overflow-hidden rounded-2xl" style="box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                                    <iframe src="{src}" style="width: 325px; height: 580px; border: none; transform: scale(0.7); transform-origin: top left; position: absolute; top: 0; left: 0;" allowfullscreen></iframe>
                                </div>"""

        content = re.sub(pattern, repl, content)
        
        # Handle the one inside Jinja {% if %} block in landing.html if I had one
        pattern_jinja = r'<div class="snap-center shrink-0 w-\[220px\] md:w-\[240px\]">\s*<iframe src="https://www.tiktok.com/embed/v2/\{\{ video_id \}\}" style="[^"]*" allowfullscreen></iframe>\s*</div>'
        
        def repl_jinja(match):
            return f"""<div class="snap-center shrink-0 w-[227px] h-[406px] relative overflow-hidden rounded-2xl" style="box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                                    <iframe src="https://www.tiktok.com/embed/v2/{{{{ video_id }}}}" style="width: 325px; height: 580px; border: none; transform: scale(0.7); transform-origin: top left; position: absolute; top: 0; left: 0;" allowfullscreen></iframe>
                                </div>"""

        content = re.sub(pattern_jinja, repl_jinja, content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed sizes in {filepath}")
    except Exception as e:
        print(f"Failed {filepath}: {e}")

fix_tiktok_size('index.html')
fix_tiktok_size('templates/landing.html')
