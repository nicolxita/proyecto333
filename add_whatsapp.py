import re

def add_whatsapp_button(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if whatsapp button already exists
    if 'wa.me/56979460119' in content:
        print(f"WhatsApp button already exists in {filepath}")
        return

    whatsapp_html = """
    <!-- WhatsApp Floating Button -->
    <a href="https://wa.me/56979460119" target="_blank" class="fixed bottom-6 right-6 z-50 bg-[#25D366] hover:bg-[#128C7E] text-white rounded-full p-3 shadow-2xl transition-transform hover:scale-110 flex items-center justify-center group" aria-label="Chat on WhatsApp">
        <svg class="w-8 h-8 fill-current" viewBox="0 0 24 24">
            <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.298.144.347.491 1.2.534 1.287.043.087.072.188.014.304-.058.116-.087.188-.173.289l-.26.304c-.087.086-.177.18-.076.354.101.174.449.741.964 1.201.662.591 1.221.774 1.394.86s.274.072.376-.043c.101-.116.433-.506.549-.68.116-.173.231-.145.39-.087s1.011.477 1.184.564.289.13.332.202c.045.072.045.419-.1.824zm-3.423-14.416c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm.029 18.88c-1.161 0-2.305-.292-3.318-.844l-3.677.964.984-3.595c-.607-1.052-.927-2.246-.926-3.468.001-5.824 4.74-10.563 10.567-10.563 5.824 0 10.563 4.739 10.564 10.563 0 5.824-4.74 10.563-10.564 10.563z"/>
        </svg>
    </a>
</body>"""

    content = content.replace("</body>", whatsapp_html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Added WhatsApp to {filepath}")

add_whatsapp_button("index.html")
add_whatsapp_button("templates/landing.html")
