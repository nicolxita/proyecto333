with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace pinks with pastel greens (emerald)
html = html.replace("bg-pink-300", "bg-emerald-300")
html = html.replace("bg-pink-100", "bg-emerald-100")
html = html.replace("text-pink-400", "text-emerald-500")
html = html.replace("bg-pink-400", "bg-emerald-500")
html = html.replace("hover:bg-pink-500", "hover:bg-emerald-600")
html = html.replace("shadow-pink-400/20", "shadow-emerald-500/20")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 16 complete")
