from PIL import Image, ImageDraw
import os

# Paths
output_large = os.path.join("frontend", "public", "favicon.png")
output_small = os.path.join("frontend", "public", "favicon-32.png")

def create_favicon(size, path):
    img = Image.new("RGB", (size, size), color=(30, 30, 30))  # dark background
    draw = ImageDraw.Draw(img)

    # Scale circle positions and radius based on size
    scale = size / 256
    positions = [(128, 60), (80, 160), (176, 160)]
    radius = int(30 * scale)
    for x, y in positions:
        x_scaled = int(x * scale)
        y_scaled = int(y * scale)
        draw.ellipse((x_scaled-radius, y_scaled-radius, x_scaled+radius, y_scaled+radius), fill=(230, 230, 230))

    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    print(f"✅ Favicon saved at {path}")

# Generate both sizes
create_favicon(256, output_large)
create_favicon(32, output_small)
