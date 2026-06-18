import re

with open("templates/landing.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Move the side banner to be absolute to body and adjust width
# We find the <div class="relative"> wrapper and the side banner
banner_pattern = r'<div class="relative">\s*<!-- Background side banner -->\s*<div class="absolute top-0 left-0 w-\[200px\] xl:w-\[250px\] h-\[800px\] hidden lg:block pointer-events-none z-0">\s*<img src="assets/bg_banner\.jpg" class="w-full h-full object-cover opacity-90" style="-webkit-mask-image: linear-gradient\(to right, rgba\(0,0,0,1\) 30%, rgba\(0,0,0,0\) 100%\); mask-image: linear-gradient\(to right, rgba\(0,0,0,1\) 30%, rgba\(0,0,0,0\) 100%\);">\s*</div>'

new_banner = """<!-- Background side banner -->
    <div class="absolute top-0 left-0 w-[120px] xl:w-[180px] h-[900px] hidden lg:block pointer-events-none z-0">
        <img src="assets/bg_banner.jpg" class="w-full h-full object-cover opacity-80" style="-webkit-mask-image: linear-gradient(to right, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 100%); mask-image: linear-gradient(to right, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 100%);">
    </div>"""

# Remove the old banner and the relative wrapper
content = re.sub(banner_pattern, '', content)

# Remove the closing </div> of the relative wrapper that was right before the footer
content = content.replace("</section>\n    </div>\n\n    <footer", "</section>\n\n    <footer")

# Add relative to body and insert the new banner right after body starts
body_tag = '<body class="bg-white text-gray-900">'
new_body = '<body class="bg-white text-gray-900 relative">\n    ' + new_banner
content = content.replace(body_tag, new_body)


# 2. Update Marquee margin
marquee_old = '<div class="bg-gray-50 border-b border-gray-200/50 overflow-hidden lg:ml-[200px] xl:ml-[250px] relative z-10">'
marquee_new = '<div class="bg-gray-50 border-b border-gray-200/50 overflow-hidden lg:ml-[120px] xl:ml-[180px] relative z-10">'
content = content.replace(marquee_old, marquee_new)


# 3. Constrain Hero Grid and Center Form
hero_grid_old = '<div class="grid md:grid-cols-2 gap-12 items-center">'
hero_grid_new = '<div class="grid md:grid-cols-2 gap-8 lg:gap-12 items-center max-w-5xl mx-auto">'
# Only replace the first instance (Hero)
content = content.replace(hero_grid_old, hero_grid_new, 1)

form_old = '<div class="bg-white rounded-3xl p-5 md:p-6 shadow-xl border border-gray-100 max-w-[400px] w-full mx-auto lg:mx-0">'
form_new = '<div class="bg-white rounded-3xl p-5 md:p-6 shadow-xl border border-gray-100 max-w-[420px] w-full mx-auto">'
content = content.replace(form_old, form_new)

image_container_old = '<div class="w-full h-auto aspect-square bg-gray-50 rounded-3xl flex items-center justify-center overflow-hidden border border-gray-100">'
image_container_new = '<div class="w-full h-auto aspect-[4/5] sm:aspect-square bg-gray-50 rounded-3xl flex items-center justify-center overflow-hidden border border-gray-100 shadow-sm">'
# We will replace all instances of this to affect Hero, Solution, and Highlights
content = content.replace(image_container_old, image_container_new)

# Constrain grids in Solution and Highlights
solution_grid_old = '<div class="grid md:grid-cols-2 gap-12 items-center">'
solution_grid_new = '<div class="grid md:grid-cols-2 gap-8 lg:gap-12 items-center max-w-5xl mx-auto">'
content = content.replace(solution_grid_old, solution_grid_new)


# 4. Change Objection bg from gray-900 to black
objection_old = '<div class="grid md:grid-cols-2 gap-12 items-center bg-gray-900 text-white p-8 md:p-12 rounded-3xl">'
objection_new = '<div class="grid md:grid-cols-2 gap-12 items-center bg-black text-white p-8 md:p-12 rounded-3xl shadow-xl">'
content = content.replace(objection_old, objection_new)


with open("templates/landing.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Template updated!")
