#!/usr/bin/env python3
"""
Placeholder Asset Generator for James Bland: ACME Edition
Generates basic visual assets matching design specifications for development use.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Color palette from art style guide
ACME_RED = "#E53935"
ACME_YELLOW = "#FFEB3B"
ACME_BLUE = "#1E88E5"
OUTLINE_BLACK = "#000000"
CARTOON_WHITE = "#FFFFFF"
PANEL_GRAY = "#F2F2F2"

def create_ui_components():
    """Create UI component assets."""
    print("Creating UI Components...")
    
    # Play button - 256x64px red button with "PLAY" text
    img = Image.new('RGBA', (256, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Main button body with rounded corners (simulated with rectangle)
    draw.rectangle([2, 2, 254, 62], fill=ACME_RED, outline=OUTLINE_BLACK, width=3)
    
    # Add "PLAY" text (simplified - using default font)
    try:
        # Try to use a larger font
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text = "PLAY"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (256 - text_width) // 2
    text_y = (64 - text_height) // 2
    
    # Text with outline effect
    for adj in range(-2, 3):
        for adj2 in range(-2, 3):
            if adj != 0 or adj2 != 0:
                draw.text((text_x + adj, text_y + adj2), text, font=font, fill=OUTLINE_BLACK)
    draw.text((text_x, text_y), text, font=font, fill=CARTOON_WHITE)
    
    img.save('assets/images/UI/button_play.png')
    print("✓ Created button_play.png")
    
    # Settings button - 256x64px yellow button with gear icon + "SETTINGS"
    img = Image.new('RGBA', (256, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Main button body
    draw.rectangle([2, 2, 254, 62], fill=ACME_YELLOW, outline=OUTLINE_BLACK, width=3)
    
    # Simple gear icon (circle with teeth)
    gear_center = (40, 32)
    gear_radius = 12
    draw.ellipse([gear_center[0]-gear_radius, gear_center[1]-gear_radius, 
                  gear_center[0]+gear_radius, gear_center[1]+gear_radius], 
                 fill=OUTLINE_BLACK, outline=OUTLINE_BLACK, width=2)
    draw.ellipse([gear_center[0]-6, gear_center[1]-6, 
                  gear_center[0]+6, gear_center[1]+6], 
                 fill=ACME_YELLOW, outline=OUTLINE_BLACK, width=1)
    
    # "SETTINGS" text
    text = "SETTINGS"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = 80 + (176 - text_width) // 2  # Start after gear
    text_y = (64 - text_height) // 2
    
    # Text with outline
    for adj in range(-2, 3):
        for adj2 in range(-2, 3):
            if adj != 0 or adj2 != 0:
                draw.text((text_x + adj, text_y + adj2), text, font=font, fill=OUTLINE_BLACK)
    draw.text((text_x, text_y), text, font=font, fill=CARTOON_WHITE)
    
    img.save('assets/images/UI/button_settings.png')
    print("✓ Created button_settings.png")
    
    # Panel background - 1024x768px tileable blueprint grid
    img = Image.new('RGBA', (1024, 768), PANEL_GRAY)
    draw = ImageDraw.Draw(img)
    
    # Create blueprint grid pattern
    grid_size = 32
    line_color = "#E0E0E0"
    
    # Vertical lines
    for x in range(0, 1024, grid_size):
        draw.line([(x, 0), (x, 768)], fill=line_color, width=1)
    
    # Horizontal lines
    for y in range(0, 768, grid_size):
        draw.line([(0, y), (1024, y)], fill=line_color, width=1)
    
    # Add some blueprint-style accent lines
    accent_color = "#D0D0D0"
    for x in range(0, 1024, grid_size * 4):
        draw.line([(x, 0), (x, 768)], fill=accent_color, width=2)
    for y in range(0, 768, grid_size * 4):
        draw.line([(0, y), (1024, y)], fill=accent_color, width=2)
    
    img.save('assets/images/UI/panel_background.png')
    print("✓ Created panel_background.png")

def create_board_tiles():
    """Create board tile assets."""
    print("Creating Board Tiles...")
    
    # Safe house icon - 128x128px pastel blue fortress on springs
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Springs at bottom
    spring_color = "#F0F0F0"
    for x in range(20, 108, 20):
        # Zigzag spring pattern
        points = [(x, 100), (x+5, 95), (x+10, 105), (x+15, 90), (x+20, 100)]
        draw.polygon(points, fill=spring_color, outline=OUTLINE_BLACK, width=2)
    
    # Fortress main body
    fortress_color = "#ADD8E6"  # Light blue
    draw.rectangle([30, 40, 98, 95], fill=fortress_color, outline=OUTLINE_BLACK, width=3)
    
    # Castle towers
    draw.rectangle([25, 20, 45, 60], fill=fortress_color, outline=OUTLINE_BLACK, width=3)
    draw.rectangle([83, 20, 103, 60], fill=fortress_color, outline=OUTLINE_BLACK, width=3)
    
    # Crenellations
    for x in range(30, 45, 5):
        draw.rectangle([x, 15, x+3, 25], fill=fortress_color, outline=OUTLINE_BLACK, width=2)
    for x in range(88, 103, 5):
        draw.rectangle([x, 15, x+3, 25], fill=fortress_color, outline=OUTLINE_BLACK, width=2)
    
    # Door
    draw.rectangle([55, 65, 73, 95], fill=OUTLINE_BLACK, outline=OUTLINE_BLACK, width=2)
    
    img.save('assets/images/board_tiles/safe_house_icon.png')
    print("✓ Created safe_house_icon.png")
    
    # Anvil crate - 128x128px wooden crate with silver anvil
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Wooden crate
    crate_color = "#8B4513"  # Saddle brown
    draw.rectangle([20, 60, 108, 110], fill=crate_color, outline=OUTLINE_BLACK, width=3)
    
    # Wood grain lines
    grain_color = "#654321"
    for y in range(65, 105, 8):
        draw.line([(25, y), (103, y)], fill=grain_color, width=1)
    
    # Crate bands
    band_color = "#333333"
    draw.rectangle([15, 65, 25, 105], fill=band_color, outline=OUTLINE_BLACK, width=2)
    draw.rectangle([103, 65, 113, 105], fill=band_color, outline=OUTLINE_BLACK, width=2)
    
    # Silver anvil popping out
    anvil_color = "#C0C0C0"  # Silver
    
    # Anvil base
    draw.rectangle([45, 30, 83, 70], fill=anvil_color, outline=OUTLINE_BLACK, width=3)
    
    # Anvil horn
    draw.polygon([(45, 40), (35, 50), (45, 60)], fill=anvil_color, outline=OUTLINE_BLACK, width=3)
    
    # Anvil face
    draw.rectangle([83, 35, 93, 65], fill=anvil_color, outline=OUTLINE_BLACK, width=3)
    
    img.save('assets/images/board_tiles/anvil_crate.png')
    print("✓ Created anvil_crate.png")
    
    # Spy marker - 64x64px spy silhouette with googly eyes
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Hat silhouette
    draw.ellipse([10, 15, 54, 35], fill=OUTLINE_BLACK, outline=OUTLINE_BLACK, width=2)  # Hat brim
    draw.rectangle([20, 10, 44, 25], fill=OUTLINE_BLACK, outline=OUTLINE_BLACK, width=2)  # Hat crown
    
    # Head silhouette
    draw.ellipse([18, 25, 46, 53], fill=OUTLINE_BLACK, outline=OUTLINE_BLACK, width=2)
    
    # Googly eyes
    eye_color = CARTOON_WHITE
    pupil_color = OUTLINE_BLACK
    
    # Left eye
    draw.ellipse([22, 30, 32, 40], fill=eye_color, outline=OUTLINE_BLACK, width=2)
    draw.ellipse([25, 33, 29, 37], fill=pupil_color)
    
    # Right eye
    draw.ellipse([32, 30, 42, 40], fill=eye_color, outline=OUTLINE_BLACK, width=2)
    draw.ellipse([35, 33, 39, 37], fill=pupil_color)
    
    img.save('assets/images/board_tiles/spy_marker_default.png')
    print("✓ Created spy_marker_default.png")

def create_gadget_icons():
    """Create gadget icon assets."""
    print("Creating Gadget Icons...")
    
    # Spring anvil - 128x128px silver anvil on yellow spring
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Yellow spring
    spring_color = ACME_YELLOW
    spring_width = 20
    spring_height = 50
    spring_x = (128 - spring_width) // 2
    spring_bottom = 115
    
    # Spring coils
    for i in range(5):
        y = spring_bottom - i * 10
        draw.ellipse([spring_x, y-5, spring_x+spring_width, y+5], 
                    fill=spring_color, outline=OUTLINE_BLACK, width=2)
    
    # Silver anvil on top
    anvil_color = "#C0C0C0"
    anvil_y = 25
    
    # Anvil base
    draw.rectangle([35, anvil_y+20, 93, anvil_y+40], fill=anvil_color, outline=OUTLINE_BLACK, width=3)
    
    # Anvil horn
    draw.polygon([(35, anvil_y+25), (25, anvil_y+30), (35, anvil_y+35)], 
                fill=anvil_color, outline=OUTLINE_BLACK, width=3)
    
    # Anvil face
    draw.rectangle([93, anvil_y+22, 103, anvil_y+38], fill=anvil_color, outline=OUTLINE_BLACK, width=3)
    
    # Anvil top
    draw.rectangle([40, anvil_y+10, 88, anvil_y+25], fill=anvil_color, outline=OUTLINE_BLACK, width=3)
    
    img.save('assets/images/gadgets/spring_anvil.png')
    print("✓ Created spring_anvil.png")
    
    # Jetpack skates - 128x128px red skates with rocket flames
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Skate boots (red)
    boot_color = ACME_RED
    draw.ellipse([20, 40, 108, 80], fill=boot_color, outline=OUTLINE_BLACK, width=3)
    
    # Skate blade
    blade_color = "#C0C0C0"
    draw.rectangle([25, 80, 103, 88], fill=blade_color, outline=OUTLINE_BLACK, width=2)
    
    # Rocket thrusters
    thruster_color = "#666666"
    draw.ellipse([15, 50, 25, 70], fill=thruster_color, outline=OUTLINE_BLACK, width=2)
    draw.ellipse([103, 50, 113, 70], fill=thruster_color, outline=OUTLINE_BLACK, width=2)
    
    # Flames
    flame_colors = ["#FF6600", "#FF9900", "#FFCC00"]
    for i, color in enumerate(flame_colors):
        flame_size = 8 - i * 2
        # Left flame
        draw.ellipse([5-i*2, 55+i, 15-i*2, 65+i], fill=color, outline=OUTLINE_BLACK, width=1)
        # Right flame  
        draw.ellipse([113+i*2, 55+i, 123+i*2, 65+i], fill=color, outline=OUTLINE_BLACK, width=1)
    
    img.save('assets/images/gadgets/jetpack_skates.png')
    print("✓ Created jetpack_skates.png")
    
    # Robo duck - 128x128px yellow duck with metal helmet
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Duck body (yellow)
    duck_color = ACME_YELLOW
    draw.ellipse([30, 50, 98, 100], fill=duck_color, outline=OUTLINE_BLACK, width=3)
    
    # Duck head
    draw.ellipse([45, 25, 83, 65], fill=duck_color, outline=OUTLINE_BLACK, width=3)
    
    # Beak
    beak_color = "#FFA500"  # Orange
    draw.polygon([(45, 40), (30, 45), (45, 50)], fill=beak_color, outline=OUTLINE_BLACK, width=2)
    
    # Metal helmet
    helmet_color = "#808080"  # Gray
    draw.ellipse([40, 15, 88, 45], fill=helmet_color, outline=OUTLINE_BLACK, width=3)
    
    # Helmet antenna
    draw.line([(64, 15), (64, 5)], fill=OUTLINE_BLACK, width=3)
    draw.ellipse([62, 3, 66, 7], fill=ACME_RED, outline=OUTLINE_BLACK, width=2)
    
    # Googly eyes
    eye_color = CARTOON_WHITE
    pupil_color = OUTLINE_BLACK
    
    # Left eye
    draw.ellipse([50, 35, 60, 45], fill=eye_color, outline=OUTLINE_BLACK, width=2)
    draw.ellipse([53, 38, 57, 42], fill=pupil_color)
    
    # Right eye
    draw.ellipse([68, 35, 78, 45], fill=eye_color, outline=OUTLINE_BLACK, width=2)
    draw.ellipse([71, 38, 75, 42], fill=pupil_color)
    
    img.save('assets/images/gadgets/robo_duck.png')
    print("✓ Created robo_duck.png")
    
    # Bug detector - 128x128px handheld radar device
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Device body
    device_color = "#808080"  # Gray
    draw.rectangle([40, 30, 88, 100], fill=device_color, outline=OUTLINE_BLACK, width=3)
    
    # Screen
    screen_color = "#003300"  # Dark green
    draw.rectangle([45, 35, 83, 60], fill=screen_color, outline=OUTLINE_BLACK, width=2)
    
    # Radar sweep (green lines)
    sweep_color = "#00FF00"  # Bright green
    center_x, center_y = 64, 47
    draw.line([(center_x, center_y), (center_x+15, center_y-10)], fill=sweep_color, width=2)
    draw.line([(center_x, center_y), (center_x-10, center_y+12)], fill=sweep_color, width=1)
    
    # Radar dots
    draw.ellipse([70, 42, 74, 46], fill=sweep_color)
    draw.ellipse([58, 52, 62, 56], fill=sweep_color)
    
    # LED indicator
    led_color = ACME_RED
    draw.ellipse([75, 65, 83, 73], fill=led_color, outline=OUTLINE_BLACK, width=2)
    
    # Handle
    handle_color = "#404040"  # Dark gray
    draw.rectangle([55, 100, 73, 115], fill=handle_color, outline=OUTLINE_BLACK, width=2)
    
    # Antenna
    draw.line([(50, 30), (45, 15)], fill=OUTLINE_BLACK, width=3)
    draw.line([(78, 30), (83, 15)], fill=OUTLINE_BLACK, width=3)
    
    img.save('assets/images/gadgets/bug_detector.png')
    print("✓ Created bug_detector.png")

def main():
    """Generate all placeholder assets."""
    print("Generating placeholder assets for James Bland: ACME Edition")
    print("=" * 60)
    
    # Ensure directories exist
    os.makedirs('assets/images/UI', exist_ok=True)
    os.makedirs('assets/images/board_tiles', exist_ok=True)
    os.makedirs('assets/images/gadgets', exist_ok=True)
    
    try:
        create_ui_components()
        create_board_tiles()
        create_gadget_icons()
        
        print("\n" + "=" * 60)
        print("✓ All placeholder assets generated successfully!")
        print("Assets created in the assets/images/ directory")
        print("\nNext steps:")
        print("1. Review assets for visual accuracy")
        print("2. Copy to static/ directory for web serving")
        print("3. Replace with professionally designed assets if needed")
        
    except Exception as e:
        print(f"\n❌ Error generating assets: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 