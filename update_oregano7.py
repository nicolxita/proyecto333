with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

replacements = {
    "Camila R.": "Camila Rojas",
    "Francisca L.": "Francisca López"
}

for old, new in replacements.items():
    html = html.replace(old, new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 7 complete")
