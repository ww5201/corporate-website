"""
Generate app icons for "Whole House Design Customization" (全屋设计定制)
v2 - Modern geometric design with warm gradient
Creates 28x28 (mobile) and 108x108 (app store) PNG icons
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

def create_app_icon(size):
    """Create a modern geometric app icon - warm orange/gold theme."""
    
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Warm orange-gold color scheme
    primary_color = (255, 87, 34)       # Deep orange #FF5722
    secondary_color = (255, 152, 0)     # Amber #FF9800
    accent_color = (255, 193, 7)        # Gold #FFC107
    dark_color = (230, 81, 0)           # Darker orange
    white = (255, 255, 255, 255)
    cream = (255, 248, 240)
    
    margin = int(size * 0.08)
    center = size // 2
    
    # Draw rounded square background with gradient-like effect
    radius = int(size * 0.22)
    
    # Main background - deep warm gradient feel
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=primary_color
    )
    
    # Bottom-right highlight area (lighter)
    hl_margin = int(size * 0.12)
    draw.rounded_rectangle(
        [hl_margin + int(size*0.15), hl_margin + int(size*0.15),
         size - hl_margin, size - hl_margin],
        radius=int(radius * 0.7),
        fill=secondary_color
    )
    
    # Top-left darker area for depth
    draw.rounded_rectangle(
        [margin + 2, margin + 2,
         size - margin - int(size*0.25), size - margin - int(size*0.25)],
        radius=int(radius * 0.6),
        fill=(230, 74, 0)
    )
    
    # === Central design: Stylized geometric house + design tools ===
    inner_margin = int(size * 0.18)
    inner_size = size - 2 * inner_margin
    inner_center = center
    inner_top = inner_margin
    inner_bottom = size - inner_margin
    
    # --- Abstract house shape made of geometric elements ---
    
    # Roof: elegant triangle using lines
    roof_peak = (inner_center, inner_top + int(inner_size * 0.05))
    roof_left = (inner_margin + int(size * 0.04), inner_top + int(inner_size * 0.38))
    roof_right = (size - inner_margin - int(size * 0.04), inner_top + int(inner_size * 0.38))
    
    # Roof fill (slightly lighter than bg)
    draw.polygon([roof_peak, roof_left, roof_right], fill=accent_color)
    
    # House body area
    body_top = inner_top + int(inner_size * 0.36)
    body_bottom = inner_bottom - int(size * 0.03)
    body_left = inner_margin + int(size * 0.1)
    body_right = size - inner_margin - int(size * 0.1)
    
    # Body rectangle with rounded top corners effect
    body_radius = int(size * 0.04)
    draw.rounded_rectangle(
        [body_left, body_top, body_right, body_bottom],
        radius=body_radius,
        fill=cream
    )
    
    # Door - centered arch door
    door_width = int(inner_size * 0.22)
    door_height = int(inner_size * 0.32)
    door_left = inner_center - door_width // 2
    door_right = inner_center + door_width // 2
    door_top = body_bottom - door_height
    door_arch_r = door_width // 2
    
    # Door body (rectangle part)
    draw.rectangle(
        [door_left, door_top + door_arch_r, door_right, body_bottom],
        fill=primary_color
    )
    
    # Door arch (top half circle)
    arch_bbox = [door_left, door_top, door_right, door_top + 2 * door_arch_r]
    draw.pieslice(arch_bbox, 180, 0, fill=primary_color)
    
    # Door handle
    handle_r = max(1, int(size * 0.018))
    handle_x = door_right - int(door_width * 0.22)
    handle_y = door_top + door_height - int(door_height * 0.35)
    draw.ellipse([handle_x - handle_r, handle_y - handle_r,
                  handle_x + handle_r, handle_y + handle_r],
                 fill=white)
    
    # Windows - round windows for a more modern look
    win_radius = int(inner_size * 0.1)
    win_y = body_top + int(inner_size * 0.15)
    win_spacing = int(inner_size * 0.35)
    
    # Left window
    win_lx = body_left + int(inner_size * 0.18)
    draw.ellipse([win_lx - win_radius, win_y - win_radius,
                  win_lx + win_radius, win_y + win_radius],
                 fill=primary_color)
    # Window shine
    shine_r = max(1, win_radius // 3)
    draw.ellipse([win_lx - win_radius + shine_r, win_y - win_radius + shine_r,
                  win_lx - win_radius + shine_r*2 + 1, win_y - win_radius + shine_r*2 + 1],
                 fill=white)
    
    # Right window
    win_rx = body_right - int(inner_size * 0.18)
    draw.ellipse([win_rx - win_radius, win_y - win_radius,
                  win_rx + win_radius, win_y + win_radius],
                 fill=primary_color)
    draw.ellipse([win_rx - win_radius + shine_r, win_y - win_radius + shine_r,
                  win_rx - win_radius + shine_r*2 + 1, win_y - win_radius + shine_r*2 + 1],
                 fill=white)
    
    # --- Design tool element: Compass/ruler indicator ---
    if size >= 48:
        # Small decorative angle bracket in top-right corner of the house
        brace_cx = body_right - int(inner_size * 0.08)
        brace_cy = body_top + int(inner_size * 0.1)
        brace_len = int(size * 0.1)
        brace_w = max(2, int(size * 0.025))
        
        # L-shaped design ruler mark
        draw.line([(brace_cx - brace_len, brace_cy), (brace_cx, brace_cy)],
                  fill=dark_color, width=brace_w)
        draw.line([(brace_cx, brace_cy), (brace_cx, brace_cy + brace_len)],
                  fill=dark_color, width=brace_w)
        
        # Small dot at corner
        dot_r = max(1, int(size * 0.02))
        draw.ellipse([brace_cx - dot_r, brace_cy - dot_r,
                      brace_cx + dot_r, brace_cy + dot_r],
                     fill=dark_color)
    
    return img


def main():
    output_dir = r'D:\tokai'
    
    sizes = {
        'app_icon_28x28.png': 28,
        'app_icon_108x108.png': 108,
    }
    
    for filename, size in sizes.items():
        print(f'Generating {filename} ({size}x{size})...')
        img = create_app_icon(size)
        
        filepath = os.path.join(output_dir, filename)
        img.save(filepath, 'PNG')
        
        file_size_kb = os.path.getsize(filepath) / 1024
        status = 'OK' if file_size_kb <= 300 else 'WARN'
        print(f'[{status}] Saved: {filepath} ({file_size_kb:.1f} KB)')
    
    print('\nDone! Icons generated successfully.')
    return list(sizes.keys())


if __name__ == '__main__':
    main()
