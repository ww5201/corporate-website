from PIL import Image
import os

src = Image.open(r'D:\tokai\app_icon_108x108.png')

sizes = {
    'mipmap-mdpi': 48,
    'mipmap-hdpi': 72,
    'mipmap-xhdpi': 96,
    'mipmap-xxhdpi': 144,
    'mipmap-xxxhdpi': 192,
}

base = r'D:\tokai\android-app\app\src\main\res'
for folder, dim in sizes.items():
    out_path = os.path.join(base, folder, 'ic_launcher.png')
    resized = src.resize((dim, dim), Image.LANCZOS)
    resized.save(out_path, 'PNG')
    print(f'OK {folder}: {dim}x{dim}')

# Also update the root icon.png
root_icon = os.path.join(base, '..', 'icon.png')
resized_root = src.resize((192, 192), Image.LANCZOS)
resized_root.save(root_icon, 'PNG')
print('OK icon.png: 192x192')

print('All Android icons updated!')
