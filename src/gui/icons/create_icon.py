"""
Icon Generator for Simple Media Player
Creates a professional film reel icon with play button overlay
"""

from PIL import Image, ImageDraw
import os


def create_app_icon():
    """
    Create application icon at multiple resolutions
    Design: Film reel with Netflix red play button
    """
    sizes = [16, 32, 48, 64, 128, 256, 512]
    
    # Colors (Netflix theme)
    NETFLIX_RED = (229, 9, 20)
    DARK_GRAY = (20, 20, 20)
    WHITE = (255, 255, 255)
    
    for size in sizes:
        # Create image with transparency
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate dimensions
        center = size // 2
        outer_radius = size // 2 - 2
        inner_radius = int(outer_radius * 0.6)
        
        # Draw outer circle (film reel border) - dark gray
        draw.ellipse(
            [2, 2, size-2, size-2],
            fill=DARK_GRAY,
            outline=WHITE,
            width=max(1, size // 64)
        )
        
        # Draw inner circle (transparent center)
        draw.ellipse(
            [center - inner_radius, center - inner_radius,
             center + inner_radius, center + inner_radius],
            fill=(0, 0, 0, 0)
        )
        
        # Draw film reel holes (4 small circles around the edge)
        hole_radius = max(2, size // 20)
        hole_distance = int(outer_radius * 0.8)
        
        for angle in [45, 135, 225, 315]:
            import math
            rad = math.radians(angle)
            x = center + int(hole_distance * math.cos(rad))
            y = center + int(hole_distance * math.sin(rad))
            draw.ellipse(
                [x - hole_radius, y - hole_radius,
                 x + hole_radius, y + hole_radius],
                fill=(0, 0, 0, 0),
                outline=WHITE,
                width=max(1, size // 128)
            )
        
        # Draw Netflix red circle background for play button
        play_bg_radius = int(inner_radius * 0.7)
        draw.ellipse(
            [center - play_bg_radius, center - play_bg_radius,
             center + play_bg_radius, center + play_bg_radius],
            fill=NETFLIX_RED
        )
        
        # Draw white play triangle
        play_size = int(play_bg_radius * 0.6)
        play_offset = play_size // 4
        
        triangle = [
            (center - play_offset, center - play_size),  # Top
            (center - play_offset, center + play_size),  # Bottom
            (center + play_size, center)  # Right point
        ]
        draw.polygon(triangle, fill=WHITE)
        
        # Save PNG
        img.save(f'icon_{size}x{size}.png', 'PNG')
        print(f"Created icon_{size}x{size}.png")
    
    # Create ICO file for Windows (combining multiple sizes)
    ico_sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
    icons = []
    for width, height in ico_sizes:
        icons.append(Image.open(f'icon_{width}x{height}.png'))
    
    icons[0].save(
        'app_icon.ico',
        format='ICO',
        sizes=ico_sizes
    )
    print("Created app_icon.ico")
    
    print("\nIcon generation complete!")
    print("Files created:")
    print("  - icon_*.png (various sizes)")
    print("  - app_icon.ico (Windows)")


if __name__ == '__main__':
    # Ensure we're in the icons directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    create_app_icon()
