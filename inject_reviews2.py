import re

def inject_reviews(filepath, is_template=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if is_template:
        reviews_html = """
        <!-- Social Proof Section -->
        <section class="bg-[#F8F9FA] py-12 md:py-16">
            <div class="container mx-auto px-6 text-center">
                <h3 class="text-2xl md:text-3xl font-extrabold text-gray-900 mb-3 tracking-tighter">{{ social_proof_title | default('Lo que dicen quienes ya lo tienen') }}</h3>
                <p class="text-base text-gray-600 mb-10 max-w-2xl mx-auto">{{ social_proof_desc | default('Comentarios reales de personas reales.') }}</p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                    {% if reviews %}
                        {% for review in reviews %}
                        <div class="bg-white rounded-[20px] p-5 shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-gray-100 flex flex-col items-start text-left hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-all duration-300">
                            <div class="flex items-center w-full mb-3 space-x-3">
                                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-gray-200 to-gray-300 flex-shrink-0 flex items-center justify-center text-gray-600 font-bold text-lg">
                                    {{ review.author[0]|upper if review.author else 'U' }}
                                </div>
                                <div class="flex-1">
                                    <div class="flex items-center space-x-1">
                                        <span class="font-bold text-sm text-gray-900 tracking-tight">{{ review.author }}</span>
                                        <!-- Verification check -->
                                        <svg class="w-3 h-3 text-blue-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                                    </div>
                                    <div class="text-[11px] font-medium text-gray-400">{{ review.platform | default('TikTok') }}</div>
                                </div>
                                <!-- Rating Stars -->
                                <div class="flex text-yellow-400 space-x-0.5">
                                    {% for i in range(5) %}
                                    <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                                    {% endfor %}
                                </div>
                            </div>
                            <p class="text-gray-800 text-[15px] leading-relaxed mb-3 font-medium w-full">"{{ review.quote }}"</p>
                            <div class="mt-auto pt-3 border-t border-gray-50 w-full flex items-center justify-between text-gray-400 text-[11px] font-medium">
                                <div class="flex items-center space-x-4">
                                    <span class="flex items-center hover:text-red-500 cursor-pointer transition-colors"><svg class="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg> {{ loop.index * 41 + 17 }}</span>
                                    <span class="flex items-center hover:text-gray-600 cursor-pointer transition-colors"><svg class="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg> Responder</span>
                                </div>
                                <span>{{ review.location }}</span>
                            </div>
                        </div>
                        {% endfor %}
                    {% endif %}
                </div>
            </div>
        </section>
        """
    else:
        # Static mock data for index.html
        mock_reviews = [
            {"author": "@vale_ignacia", "platform": "TikTok", "quote": "Llegó super rápido a Providencia!! Las gotitas de lavanda huelen exquisito en toda mi pieza, recomendadísimo ✨", "location": "Providencia", "rating": 5},
            {"author": "Sebastián R.", "platform": "Amazon", "quote": "Al principio dudaba si realmente tiraba ese efecto de fuego, pero sí. Se ve increíble en el escritorio de noche y no mete nada de ruido.", "location": "Las Condes", "rating": 5},
            {"author": "@cata.lifestyle", "platform": "TikTok", "quote": "Lo compré hace 3 días y ya me solucionó los problemas de alergia por el aire seco. Amé q sea tan aesthetic 😍", "location": "Viña del Mar", "rating": 5},
            {"author": "Felipe M.", "platform": "X (Twitter)", "quote": "Confirmo que es el mejor setup upgrade que he hecho este año. El nivel del vapor es brutal y el rgb le da todo el toque.", "location": "Santiago", "rating": 5},
            {"author": "@dani_wellness", "platform": "TikTok", "quote": "Literalmente es como tener una chimenea en miniatura que no quema jaja. Lo dejo prendido toda la noche y me relaja al 100", "location": "Ñuñoa", "rating": 5}
        ]
        
        cards = ""
        for i, r in enumerate(mock_reviews):
            stars_svg = '<svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>'
            stars = stars_svg * r['rating']
            avatar_letter = r['author'][0].upper() if r['author'][0] != '@' else r['author'][1].upper()
            
            cards += f"""
                        <div class="bg-white rounded-[20px] p-5 shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-gray-100 flex flex-col items-start text-left hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-all duration-300">
                            <div class="flex items-center w-full mb-3 space-x-3">
                                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-gray-200 to-gray-300 flex-shrink-0 flex items-center justify-center text-gray-600 font-bold text-lg">
                                    {avatar_letter}
                                </div>
                                <div class="flex-1">
                                    <div class="flex items-center space-x-1">
                                        <span class="font-bold text-sm text-gray-900 tracking-tight">{r['author']}</span>
                                        <svg class="w-3 h-3 text-blue-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                                    </div>
                                    <div class="text-[11px] font-medium text-gray-400">{r['platform']}</div>
                                </div>
                                <div class="flex text-yellow-400 space-x-0.5">
                                    {stars}
                                </div>
                            </div>
                            <p class="text-gray-800 text-[15px] leading-relaxed mb-3 font-medium w-full">"{r['quote']}"</p>
                            <div class="mt-auto pt-3 border-t border-gray-50 w-full flex items-center justify-between text-gray-400 text-[11px] font-medium">
                                <div class="flex items-center space-x-4">
                                    <span class="flex items-center hover:text-red-500 cursor-pointer transition-colors"><svg class="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg> {(i+1) * 41 + 17}</span>
                                    <span class="flex items-center hover:text-gray-600 cursor-pointer transition-colors"><svg class="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg> Responder</span>
                                </div>
                                <span>{r['location']}</span>
                            </div>
                        </div>
            """

        reviews_html = f"""
        <!-- Social Proof Section -->
        <section class="bg-[#F8F9FA] py-12 md:py-16">
            <div class="container mx-auto px-6 text-center">
                <h3 class="text-2xl md:text-3xl font-extrabold text-gray-900 mb-3 tracking-tighter">Lo que dicen quienes ya lo tienen</h3>
                <p class="text-base text-gray-600 mb-10 max-w-2xl mx-auto">Comentarios 100% reales de personas que ya disfrutan de su Humidificador.</p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                    {cards}
                </div>
            </div>
        </section>
        """

    if '<!-- Social Proof Section -->' in content:
        print(f"Social Proof already in {filepath}, skipping.")
        return

    pattern = r'(</style>\s*</section>)'
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
