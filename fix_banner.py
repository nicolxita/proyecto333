import re

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the banner block
    banner_pattern = r'<!-- Background side banner -->\s*<div class="absolute top-0 left-0 w-\[120px\] xl:w-\[180px\] h-\[900px\] hidden lg:block pointer-events-none z-0">\s*<img src="assets/bg_banner\.jpg" class="w-full h-full object-cover opacity-80" style="-webkit-mask-image: linear-gradient\(to right, rgba\(0,0,0,1\) 0%, rgba\(0,0,0,0\) 100%\); mask-image: linear-gradient\(to right, rgba\(0,0,0,1\) 0%, rgba\(0,0,0,0\) 100%\);">\s*</div>'
    
    new_banner = """<!-- Background side banner -->
    <div class="absolute top-0 left-0 w-[120px] xl:w-[180px] h-[900px] hidden lg:block pointer-events-none z-50" style="-webkit-mask-image: linear-gradient(to right, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 100%); mask-image: linear-gradient(to right, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 100%);">
        <img src="assets/bg_banner.jpg" class="w-full h-full object-cover opacity-80">
        <!-- Vertical fade out to white at the bottom -->
        <div class="absolute bottom-0 left-0 w-full h-[300px] bg-gradient-to-t from-white to-transparent"></div>
    </div>"""

    content = re.sub(banner_pattern, new_banner, content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

fix_file("index.html")
fix_file("templates/landing.html")

print("Banner fixed in both files!")
