with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace review photos
html = html.replace('src="assets/reseñas/l.avif"', 'src="assets/reseñas/reseña.png"')
html = html.replace('src="assets/reseñas/l (2).avif"', 'src="assets/reseñas/reseña2.png"')
# Note: l (1).avif is still in the folder, so we leave it mapped to the second review.

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 15 complete")
