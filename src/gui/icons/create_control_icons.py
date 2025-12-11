"""
Control Icon Generator for Simple Media Player
Creates professional SVG icons for playback controls with Netflix-inspired design
"""

import os


def create_play_icon():
    """Create modern rounded triangle play icon"""
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <g>
    <!-- Circular background (optional, can be styled via CSS) -->
    <circle cx="24" cy="24" r="22" fill="none" stroke="currentColor" stroke-width="2" opacity="0.2"/>
    
    <!-- Rounded play triangle -->
    <path d="M18 12 L18 36 L36 24 Z" 
          fill="currentColor" 
          stroke="currentColor" 
          stroke-width="1.5" 
          stroke-linejoin="round" 
          stroke-linecap="round"/>
  </g>
</svg>"""
    return svg


def create_pause_icon():
    """Create modern rounded bars pause icon"""
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <g>
    <!-- Circular background (optional) -->
    <circle cx="24" cy="24" r="22" fill="none" stroke="currentColor" stroke-width="2" opacity="0.2"/>
    
    <!-- Left pause bar with rounded corners -->
    <rect x="16" y="13" width="6" height="22" rx="2" ry="2" fill="currentColor"/>
    
    <!-- Right pause bar with rounded corners -->
    <rect x="26" y="13" width="6" height="22" rx="2" ry="2" fill="currentColor"/>
  </g>
</svg>"""
    return svg


def create_stop_icon():
    """Create modern rounded square stop icon"""
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <g>
    <!-- Circular background (optional) -->
    <circle cx="24" cy="24" r="22" fill="none" stroke="currentColor" stroke-width="2" opacity="0.2"/>
    
    <!-- Rounded square -->
    <rect x="14" y="14" width="20" height="20" rx="3" ry="3" fill="currentColor"/>
  </g>
</svg>"""
    return svg


def create_fullscreen_icon():
    """Create modern expand arrows fullscreen icon"""
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <g stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- Top-left corner -->
    <polyline points="10,18 10,10 18,10"/>
    
    <!-- Top-right corner -->
    <polyline points="30,10 38,10 38,18"/>
    
    <!-- Bottom-right corner -->
    <polyline points="38,30 38,38 30,38"/>
    
    <!-- Bottom-left corner -->
    <polyline points="18,38 10,38 10,30"/>
  </g>
</svg>"""
    return svg


def create_exit_fullscreen_icon():
    """Create modern collapse arrows exit fullscreen icon"""
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <g stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- Top-left corner (inward) -->
    <polyline points="18,10 18,18 10,18"/>
    
    <!-- Top-right corner (inward) -->
    <polyline points="30,18 38,18 38,10"/>
    
    <!-- Bottom-right corner (inward) -->
    <polyline points="38,30 30,30 30,38"/>
    
    <!-- Bottom-left corner (inward) -->
    <polyline points="10,30 18,30 18,38"/>
  </g>
</svg>"""
    return svg


def create_forward_icon():
    """Create forward/skip icon"""
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <g fill="currentColor">
    <!-- First triangle -->
    <path d="M12 12 L12 36 L26 24 Z"/>
    
    <!-- Second triangle -->
    <path d="M24 12 L24 36 L38 24 Z"/>
  </g>
</svg>"""
    return svg


def create_backward_icon():
    """Create backward/rewind icon"""
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <g fill="currentColor">
    <!-- First triangle -->
    <path d="M36 12 L36 36 L22 24 Z"/>
    
    <!-- Second triangle -->
    <path d="M24 12 L24 36 L10 24 Z"/>
  </g>
</svg>"""
    return svg


def create_speed_icon():
    """Create speedometer icon for speed control"""
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <g stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round">
    <!-- Speedometer arc -->
    <path d="M10 30 A 14 14 0 0 1 38 30"/>
    
    <!-- Needle pointing to right (1x speed) -->
    <line x1="24" y1="30" x2="32" y2="22" stroke-width="3"/>
    
    <!-- Center dot -->
    <circle cx="24" cy="30" r="2" fill="currentColor"/>
  </g>
</svg>"""
    return svg


def create_theme_moon_icon():
    """Create moon icon for dark theme toggle"""
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <path d="M24 4 A 16 16 0 0 0 24 44 A 14 14 0 0 1 24 4 Z" 
        fill="currentColor" 
        stroke="currentColor" 
        stroke-width="1"/>
</svg>"""
    return svg


def create_theme_sun_icon():
    """Create sun icon for light theme toggle"""
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <g stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round">
    <!-- Center circle -->
    <circle cx="24" cy="24" r="8" fill="currentColor"/>
    
    <!-- Sun rays -->
    <line x1="24" y1="4" x2="24" y2="10"/>
    <line x1="24" y1="38" x2="24" y2="44"/>
    <line x1="4" y1="24" x2="10" y2="24"/>
    <line x1="38" y1="24" x2="44" y2="24"/>
    <line x1="10" y1="10" x2="14" y2="14"/>
    <line x1="34" y1="34" x2="38" y2="38"/>
    <line x1="10" y1="38" x2="14" y2="34"/>
    <line x1="34" y1="14" x2="38" y2="10"/>
  </g>
</svg>"""
    return svg


def save_icon(filename, svg_content):
    """Save SVG icon to file"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Created {filename}")


def main():
    """Generate all control icons"""
    print("Generating control icons...")
    
    icons = {
        'play.svg': create_play_icon(),
        'pause.svg': create_pause_icon(),
        'stop.svg': create_stop_icon(),
        'fullscreen.svg': create_fullscreen_icon(),
        'exit_fullscreen.svg': create_exit_fullscreen_icon(),
        'forward.svg': create_forward_icon(),
        'backward.svg': create_backward_icon(),
        'speed.svg': create_speed_icon(),
        'theme_moon.svg': create_theme_moon_icon(),
        'theme_sun.svg': create_theme_sun_icon(),
    }
    
    for filename, content in icons.items():
        save_icon(filename, content)
    
    print(f"\n✅ Generated {len(icons)} SVG icons successfully!")
    print("\nThese icons use 'currentColor' which means they will")
    print("automatically adapt to the theme's text color.")


if __name__ == '__main__':
    main()
