import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove the large UGC section at the bottom
    start_str = "<!-- UGC / TikTok Section -->"
    end_str = "</section>"
    
    start_idx = content.find(start_str)
    if start_idx != -1:
        end_idx = content.find(end_str, start_idx)
        if end_idx != -1:
            end_idx += len(end_str)
            content = content[:start_idx] + content[end_idx:]

    # 2. Replace the fake thumbnails with the horizontal TikTok scroll
    # Fake thumbnails start at: <div class="mt-6 flex justify-center gap-3 w-full max-w-[420px] mx-auto">
    # And end at the </div> before the closing tag of lg:col-span-5
    
    fake_thumb_start = '<div class="mt-6 flex justify-center gap-3 w-full max-w-[420px] mx-auto">'
    start_thumb_idx = content.find(fake_thumb_start)
    
    if start_thumb_idx != -1:
        # The block is 37 lines long, ending with </div> </div> </section>
        # Let's find the end of the fake thumbnails div.
        # It ends right before "</div>\n                </div>\n            </div>\n        </section>"
        
        # We can find the next "</div>\n                </div>"
        end_thumb_idx = content.find('</div>\n                </div>\n            </div>\n        </section>', start_thumb_idx)
        
        if end_thumb_idx != -1:
            ugc_carousel = """<div class="mt-8 w-full max-w-[420px] mx-auto text-center">
                            <span class="text-pink-400 font-extrabold tracking-widest uppercase text-[10px] mb-1 block">Se volvió viral 🔥</span>
                            <h3 class="text-lg md:text-xl font-extrabold text-gray-900 mb-4 tracking-tight">Lo que todos dicen en TikTok</h3>
                            <div class="flex overflow-x-auto gap-4 snap-x snap-mandatory pb-4" style="-ms-overflow-style: none; scrollbar-width: none;">
                                <!-- TikTok 1 -->
                                <div class="snap-center shrink-0 w-[325px]">
                                    <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@daniel.ecommerceshopify/video/7649734220826381590" data-video-id="7649734220826381590" style="max-width: 325px; min-width: 325px; margin: 0;">
                                        <section> <a target="_blank" title="@daniel.ecommerceshopify" href="https://www.tiktok.com/@daniel.ecommerceshopify">@daniel.ecommerceshopify</a> </section>
                                    </blockquote>
                                </div>
                                <!-- TikTok 2 -->
                                <div class="snap-center shrink-0 w-[325px]">
                                    <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@daniel.ecommerceshopify/video/7649734220826381590" data-video-id="7649734220826381590" style="max-width: 325px; min-width: 325px; margin: 0;">
                                        <section> <a target="_blank" title="@daniel.ecommerceshopify" href="https://www.tiktok.com/@daniel.ecommerceshopify">@daniel.ecommerceshopify</a> </section>
                                    </blockquote>
                                </div>
                                <!-- TikTok 3 -->
                                <div class="snap-center shrink-0 w-[325px]">
                                    <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@daniel.ecommerceshopify/video/7649734220826381590" data-video-id="7649734220826381590" style="max-width: 325px; min-width: 325px; margin: 0;">
                                        <section> <a target="_blank" title="@daniel.ecommerceshopify" href="https://www.tiktok.com/@daniel.ecommerceshopify">@daniel.ecommerceshopify</a> </section>
                                    </blockquote>
                                </div>
                            </div>
                        </div>
                        <style>
                            .mt-8 .flex::-webkit-scrollbar { display: none; }
                        </style>"""
            
            content = content[:start_thumb_idx] + ugc_carousel + "\n                        " + content[end_thumb_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed {filepath}")

process_file('index.html')
process_file('templates/landing.html')
