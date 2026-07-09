with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# The first instance is Beneficios
first_part = html[:len(html)//2]
second_part = html[len(html)//2:]

first_part = first_part.replace("assets/gifs/giforegano.gif", "assets/gifs/gif.gif")
second_part = second_part.replace("assets/gifs/giforegano.gif", "assets/gifs/13.webp")

html = first_part + second_part

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Update 14 complete")
