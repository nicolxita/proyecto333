import re

def inject_reviews(filepath, is_template=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where to inject. The TikTok section ends with:
    # <script async src="https://www.tiktok.com/embed.js"></script>
    #         </section>
    # 
    #         <!-- 2. Problem Section -->
    
    if is_template:
        reviews_html = """
        <!-- Social Proof Section -->
        <section class="container mx-auto px-6 pb-12 md:pb-16 text-center">
            <h3 class="text-2xl md:text-3xl font-extrabold text-gray-900 mb-3 tracking-tighter">{{ social_proof_title | default('Lo que dicen quienes ya lo tienen') }}</h3>
            <p class="text-base text-gray-600 mb-10 max-w-2xl mx-auto">{{ social_proof_desc | default('Comentarios reales de personas reales.') }}</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-w-5xl mx-auto">
                {% if reviews %}
                    {% for review in reviews %}
                    <div class="bg-white rounded-2xl p-5 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07)] border border-gray-100 flex items-start space-x-3 text-left hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-shadow duration-300">
                        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-gray-200 to-gray-300 flex-shrink-0 flex items-center justify-center text-gray-500 font-bold text-lg">
                            {{ review.author[0]|upper if review.author else 'U' }}
                        </div>
                        <div class="flex-1">
                            <div class="flex justify-between items-center mb-1">
                                <span class="font-bold text-sm text-gray-900 tracking-tight">{{ review.author }}</span>
                                <span class="text-[10px] uppercase font-bold tracking-wider text-gray-400 bg-gray-50 px-2 py-0.5 rounded-full">{{ review.platform | default('TikTok') }}</span>
                            </div>
                            <p class="text-gray-800 text-[15px] leading-snug mb-2 font-medium">"{{ review.quote }}"</p>
                            <div class="mt-2 flex items-center text-gray-400 text-xs space-x-3 font-semibold">
                                <span class="flex items-center"><svg class="w-4 h-4 mr-1 text-red-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"></path></svg> {{ loop.index * 42 + 13 }}</span>
                                <span class="text-gray-400 cursor-pointer hover:text-gray-600">Responder</span>
                                <span class="text-gray-300">·</span>
                                <span class="text-gray-400">{{ review.location }}</span>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                {% endif %}
            </div>
        </section>
        """
    else:
        # Static mock data for index.html
        mock_reviews = [
            {"author": "@vale_ignacia", "platform": "TikTok", "quote": "Llegó super rápido a Providencia!! Las gotitas de lavanda huelen exquisito en toda mi pieza, recomendadísimo ✨", "location": "Providencia"},
            {"author": "Sebastián R.", "platform": "Amazon", "quote": "Al principio dudaba si realmente tiraba ese efecto de fuego, pero sí. Se ve increíble en el escritorio de noche y no mete nada de ruido.", "location": "Las Condes"},
            {"author": "@cata.lifestyle", "platform": "TikTok", "quote": "Lo compré hace 3 días y ya me solucionó los problemas de alergia por el aire seco. Amé q sea tan aesthetic 😍", "location": "Viña del Mar"},
            {"author": "Felipe M.", "platform": "Twitter", "quote": "Confirmo que es el mejor setup upgrade que he hecho este año. El nivel del vapor es brutal y el rgb le da todo el toque.", "location": "Santiago"},
            {"author": "@dani_wellness", "platform": "TikTok", "quote": "Literalmente es como tener una chimenea en miniatura que no quema jaja. Lo dejo prendido toda la noche y me relaja al 100", "location": "Ñuñoa"}
        ]
        
        cards = ""
        for i, r in enumerate(mock_reviews):
            cards += f"""
                    <div class="bg-white rounded-2xl p-5 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07)] border border-gray-100 flex items-start space-x-3 text-left hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-shadow duration-300">
                        <div class="w-10 h-10 rounded-full bg-gradient-to-br from-gray-200 to-gray-300 flex-shrink-0 flex items-center justify-center text-gray-500 font-bold text-lg">
                            {r['author'][0].upper() if r['author'][0] != '@' else r['author'][1].upper()}
                        </div>
                        <div class="flex-1">
                            <div class="flex justify-between items-center mb-1">
                                <span class="font-bold text-sm text-gray-900 tracking-tight">{r['author']}</span>
                                <span class="text-[10px] uppercase font-bold tracking-wider text-gray-400 bg-gray-50 px-2 py-0.5 rounded-full">{r['platform']}</span>
                            </div>
                            <p class="text-gray-800 text-[15px] leading-snug mb-2 font-medium">"{r['quote']}"</p>
                            <div class="mt-2 flex items-center text-gray-400 text-xs space-x-3 font-semibold">
                                <span class="flex items-center"><svg class="w-4 h-4 mr-1 text-red-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"></path></svg> {(i+1) * 42 + 13}</span>
                                <span class="text-gray-400 cursor-pointer hover:text-gray-600">Responder</span>
                                <span class="text-gray-300">·</span>
                                <span class="text-gray-400">{r['location']}</span>
                            </div>
                        </div>
                    </div>
            """

        reviews_html = f"""
        <!-- Social Proof Section -->
        <section class="container mx-auto px-6 pb-12 md:pb-16 text-center">
            <h3 class="text-2xl md:text-3xl font-extrabold text-gray-900 mb-3 tracking-tighter">Lo que dicen quienes ya lo tienen</h3>
            <p class="text-base text-gray-600 mb-10 max-w-2xl mx-auto">Comentarios 100% reales de personas que ya disfrutan de su Humidificador.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-w-5xl mx-auto">
                {cards}
            </div>
        </section>
        """

    # Inject into content
    if '<!-- Social Proof Section -->' in content:
        print(f"Social Proof already in {filepath}, skipping.")
        return

    pattern = r'(<script async src="https://www\.tiktok\.com/embed\.js"></script>\s*</section>)'
    replacement = r'\1\n' + reviews_html

    new_content = re.sub(pattern, replacement, content)
    if new_content == content:
        print(f"Could not find insertion point in {filepath}.")
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Injected reviews in {filepath}")

inject_reviews('index.html', is_template=False)
inject_reviews('templates/landing.html', is_template=True)
