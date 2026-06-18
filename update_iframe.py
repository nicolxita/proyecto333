import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The old HTML used for the TikTok embeds:
    old_embed_block = """<div class="snap-center shrink-0 w-[325px]">
                                    <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@daniel.ecommerceshopify/video/7649734220826381590" data-video-id="7649734220826381590" style="max-width: 325px; min-width: 325px; margin: 0;">
                                        <section> <a target="_blank" title="@daniel.ecommerceshopify" href="https://www.tiktok.com/@daniel.ecommerceshopify">@daniel.ecommerceshopify</a> </section>
                                    </blockquote>
                                </div>"""

    new_embed_block = """<div class="snap-center shrink-0 w-[260px] md:w-[280px]">
                                    <iframe src="https://www.tiktok.com/embed/v2/7649734220826381590" style="width: 100%; height: 480px; border: none; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);" allowfullscreen></iframe>
                                </div>"""

    # We have 3 of these blocks
    content = content.replace(old_embed_block, new_embed_block)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

update_file("index.html")
update_file("templates/landing.html")
