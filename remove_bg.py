from PIL import Image

def make_transparent(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        # Change all white (also shades of white) to transparent
        # We can use a threshold, e.g., if R, G, and B are all > 240
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Saved {output_path}")

if __name__ == "__main__":
    make_transparent("assets/estrella.jpg", "assets/estrella.png")
