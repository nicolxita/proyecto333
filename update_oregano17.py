with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace bg-emerald-300 with bg-[#adf5d7]
html = html.replace("bg-emerald-300", "bg-[#adf5d7]")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 17 complete")
