import re

def update_tiktok(filepath, is_template=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    video1 = '7162235921868311854'
    video2 = '7181077755839204613'
    video3 = '7294819402111394851'

    # If the file has the dummy ID 7649734220826381590 repeated 3 times:
    if content.count('7649734220826381590') == 3:
        content = content.replace('7649734220826381590', video1, 1)
        content = content.replace('7649734220826381590', video2, 1)
        content = content.replace('7649734220826381590', video3, 1)

    if is_template:
        # For the template, we want to wrap the 3 divs in a Jinja {% if %} block
        # Find the start of the 3 TikTok divs
        # Let's find the container:
        # <div class="flex overflow-x-auto justify-start lg:justify-center gap-4 snap-x snap-mandatory pb-4 px-4" style="-ms-overflow-style: none; scrollbar-width: none;">
        
        container_start = content.find('style="-ms-overflow-style: none; scrollbar-width: none;">')
        if container_start != -1:
            # Step forward to the end of the line
            insert_point = content.find('\\n', container_start)
            if insert_point == -1:
                insert_point = container_start + len('style="-ms-overflow-style: none; scrollbar-width: none;">')
            else:
                insert_point += 1
            
            # The 3 divs end before:
            # </div>
            # </div>
            # </section>
            
            # Let's just do a regex replace on the entire block of 3 divs
            # It's easier
            pass
        
        # Let's use regex to find the 3 tiktok divs
        pattern = r'(<!-- TikTok 1 -->.*?</div>\s*<!-- TikTok 2 -->.*?</div>\s*<!-- TikTok 3 -->.*?</div>)'
        
        def replacement(match):
            original = match.group(1)
            return """{% if tiktok_videos %}
                                {% for video_id in tiktok_videos %}
                                <div class="snap-center shrink-0 w-[220px] md:w-[240px]">
                                    <iframe src="https://www.tiktok.com/embed/v2/{{ video_id }}" style="width: 100%; height: 410px; border: none; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);" allowfullscreen></iframe>
                                </div>
                                {% endfor %}
                                {% else %}
                                """ + original + """
                                {% endif %}"""
                                
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated TikToks in {filepath}")

update_tiktok('index.html', is_template=False)
try:
    update_tiktok('templates/landing.html', is_template=True)
except Exception as e:
    print(e)
