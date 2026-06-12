from PIL import Image
import os

# Source image
src = r"D:\tokai\android-app\app\src\main\res\icon.png"
base_dir = r"D:\tokai\android-app\app\src\main\res"

# Android icon sizes for each density
sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

img = Image.open(src)
print(f"Original image: {img.size}")

for folder, size in sizes.items():
    dir_path = os.path.join(base_dir, folder)
    os.makedirs(dir_path, exist_ok=True)
    
    # Resize with high quality
    resized = img.resize((size, size), Image.LANCZOS)
    
    # Save as ic_launcher.png
    out_path = os.path.join(dir_path, "ic_launcher.png")
    resized.save(out_path, "PNG")
    print(f"Created: {out_path} ({size}x{size})")

print("\nDone! All icon sizes created.")
