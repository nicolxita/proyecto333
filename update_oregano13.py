with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Images
html = html.replace('src="assets/1.webp"', 'src="assets/fotos producto/1.png"')
html = html.replace('src="assets/2.webp"', 'src="assets/fotos producto/2.png"')
html = html.replace('src="assets/fotos producto/oreagno.png"', 'src="assets/fotos producto/3.png"')
html = html.replace('src="assets/fotos producto/descarga (1).png"', 'src="assets/fotos producto/4.png"')

# Main image (which was oreagno.png before, now let's set it to 1.png)
html = html.replace('id="main-product-image" src="assets/fotos producto/oreagno.png"', 'id="main-product-image" src="assets/fotos producto/1.png"')
# In case it's already set to 3.png because of previous replace
html = html.replace('id="main-product-image" src="assets/fotos producto/3.png"', 'id="main-product-image" src="assets/fotos producto/1.png"')

# 2. Update Discount %
html = html.replace("-50% OFF", "-25% OFF")

# 3. Update Promo 2 Price
html = html.replace("'$35.985'", "'$32.990'")
html = html.replace(">$35.985<", ">$32.990<")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 13 complete")
