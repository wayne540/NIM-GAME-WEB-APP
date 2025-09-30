from PIL import Image, ImageDraw
import os

# Path where favicon will be saved (frontend/public)
output_path = os.path.join("frontend", "public", "favicon.png")

# Create blank image
img = Image.new("RGB", (256, 256), color=(30, 30, 30))  # dark background
draw = ImageDraw.Draw(img)

# Circle positions
positions = [(128, 60), (80, 160), (176, 160)]
for x, y in positions:
    draw.ellipse((x-30, y-30, x+30, y+30), fill=(230, 230, 230))  # light counters

# Save image
os.makedirs(os.path.dirname(output_path), exist_ok=True)
img.save(output_path)
print(f"✅ Favicon saved at {output_path}")
