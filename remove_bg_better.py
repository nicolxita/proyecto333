from PIL import Image

def remove_background(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    
    pixels = img.load()
    
    visited = set()
    # Start from all four corners
    queue = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
    
    def is_white(c):
        return c[0] > 230 and c[1] > 230 and c[2] > 230
        
    for q in queue:
        visited.add(q)
        
    while queue:
        x, y = queue.pop(0)
        c = pixels[x, y]
        if is_white(c) or c[3] == 0: # If it's already transparent, we can pass through it just in case
            pixels[x, y] = (255, 255, 255, 0)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

    img.save(output_path, "PNG")
    print(f"Saved {output_path}")

if __name__ == "__main__":
    remove_background("assets/estrella.jpg", "assets/estrella.png")
