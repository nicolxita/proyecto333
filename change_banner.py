def change_banner(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace("assets/bg_banner.jpg", "assets/blue_water_banner.png")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

change_banner("index.html")
change_banner("templates/landing.html")
print("Banner changed successfully!")
