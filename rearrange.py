import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Delete garbage TikTok code
    # We will find "<!-- TikTok 2 -->" and the closest "<!-- 8. Objection Handling Section -->"
    # and clear the garbage between them.
    garbage_marker = "<!-- TikTok 2 -->"
    objection_marker = "<!-- 8. Objection Handling Section -->"
    
    start_garbage = content.find(garbage_marker)
    if start_garbage != -1:
        # Step back to find the stray </blockquote></div> that precedes it
        step_back = content.rfind("</blockquote>", 0, start_garbage)
        if step_back != -1:
            step_back = content.rfind("</div>", 0, step_back) # It was inside a <div class="mt-8...
            
            # Wait, let's just use regex to delete from </blockquote>\n </div> to </section> before Objection Handling
            
    # Better approach for the garbage:
    # We know the exact garbage block from view_file:
    # Starts around line 321 with:
    #                         </blockquote>
    #                     </div>
    #                     <!-- TikTok 2 -->
    
    # We can just search for the specific TikTok script and blockquotes and delete them.
    # Actually, let's regex remove any blockquote with class="tiktok-embed" completely.
    content = re.sub(r'<blockquote class="tiktok-embed".*?</blockquote>', '', content, flags=re.DOTALL)
    # Remove the TikTok script
    content = re.sub(r'<!-- TikTok Script -->\s*<script async src="https://www\.tiktok\.com/embed\.js"></script>', '', content)
    # Remove the extra wrappers that were left over. 
    # e.g. <div class="bg-white/5 rounded-3xl p-4 backdrop-blur-sm border border-white/10 flex justify-center shadow-2xl md:transform md:-translate-y-4">\s*</div>
    content = re.sub(r'<div class="bg-white/5[^>]*>\s*</div>', '', content, flags=re.DOTALL)
    
    # And there's a stray </blockquote> and </div> around line 322
    content = re.sub(r'</blockquote>\s*</div>\s*<!-- TikTok 2 -->', '', content, flags=re.DOTALL)
    content = content.replace("<!-- TikTok 2 -->", "")
    content = content.replace("<!-- TikTok 3 -->", "")
    # Remove empty sections that might be left
    content = re.sub(r'<div class="container mx-auto px-6">\s*<div class="grid md:grid-cols-1 lg:grid-cols-3 gap-8">\s*</div>\s*</div>\s*</section>', '', content, flags=re.DOTALL)

    # 2. Extract and Move UGC Carousel
    # It starts with: <div class="mt-8 w-full max-w-[420px] mx-auto text-center">
    # And ends with: </style>
    start_ugc = content.find('<div class="mt-8 w-full max-w-[420px] mx-auto text-center">')
    if start_ugc != -1:
        end_ugc = content.find('</style>', start_ugc) + len('</style>')
        
        ugc_block = content[start_ugc:end_ugc]
        
        # Remove it from the current position
        content = content[:start_ugc] + content[end_ugc:]
        
        # Modify the ugc_block
        # Remove the "Se volvió viral" text
        ugc_block = re.sub(r'<span class="text-pink-400[^>]*>Se volvió viral 🔥</span>', '', ugc_block)
        
        # Change max-w-[420px] to max-w-5xl and add top margin
        ugc_block = ugc_block.replace('<div class="mt-8 w-full max-w-[420px] mx-auto text-center">', '<div class="mt-16 w-full max-w-5xl mx-auto text-center">')
        
        # Change flex classes to center on desktop: justify-start lg:justify-center
        ugc_block = ugc_block.replace('<div class="flex overflow-x-auto gap-4 snap-x snap-mandatory pb-4"', '<div class="flex overflow-x-auto justify-start lg:justify-center gap-4 snap-x snap-mandatory pb-4 px-4"')
        
        # Now find where to insert it. We want it right after the grid closes in the Hero section.
        # The grid closes before </section>
        # Let's find "<!-- 2. Problem Section -->" and step back to the </section> of the hero.
        problem_idx = content.find('<!-- 2. Problem Section -->')
        if problem_idx != -1:
            hero_end_section_idx = content.rfind('</section>', 0, problem_idx)
            if hero_end_section_idx != -1:
                # Insert right before the </section>
                content = content[:hero_end_section_idx] + "\n" + ugc_block + "\n        " + content[hero_end_section_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Rearranged {filepath}")

fix_file('index.html')
fix_file('templates/landing.html')
