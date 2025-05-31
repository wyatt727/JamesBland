#!/usr/bin/env python3
"""
Animation Asset Creator for James Bland: ACME Edition
Creates multi-frame animation sequences matching design specifications.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# Color palette from art style guide
ACME_RED = "#E53935"
ACME_YELLOW = "#FFEB3B"
ACME_BLUE = "#1E88E5"
OUTLINE_BLACK = "#000000"
CARTOON_WHITE = "#FFFFFF"
SILVER = "#C0C0C0"
DARK_GRAY = "#333333"
ORANGE = "#FF6600"
GREEN = "#4CAF50"

def ensure_directory(path):
    """Ensure directory exists."""
    os.makedirs(path, exist_ok=True)

def create_piano_drop_animation():
    """Create 12-frame Piano Drop Animation (64x64px)."""
    print("Creating Piano Drop Animation...")
    
    frames = []
    frame_count = 12
    
    for frame in range(frame_count):
        # Create 64x64 frame
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate piano position (falls from top to bottom)
        progress = frame / (frame_count - 1)
        piano_y = int(-20 + progress * 50)  # Falls from above screen to bottom
        
        # Add slight rotation during fall
        rotation = progress * 15  # Slight rotation
        
        # Piano body (black rectangle with white keys)
        piano_width = 40
        piano_height = 25
        piano_x = (64 - piano_width) // 2
        
        # Draw piano shadow first (gets larger as it falls)
        shadow_offset = int(progress * 3)
        shadow_y = piano_y + piano_height + shadow_offset
        if shadow_y < 64:
            shadow_alpha = int(100 * progress)
            shadow_color = (0, 0, 0, shadow_alpha)
            # Simple shadow ellipse
            draw.ellipse([piano_x - 2, shadow_y, piano_x + piano_width + 2, shadow_y + 5], 
                        fill=shadow_color)
        
        # Draw piano body
        if piano_y < 64:
            draw.rectangle([piano_x, piano_y, piano_x + piano_width, piano_y + piano_height], 
                          fill=OUTLINE_BLACK, outline=OUTLINE_BLACK, width=2)
            
            # White keys
            key_width = 4
            for i in range(8):
                key_x = piano_x + 4 + i * 4
                if key_x < piano_x + piano_width - 2:
                    draw.rectangle([key_x, piano_y + 3, key_x + key_width - 1, piano_y + piano_height - 3], 
                                  fill=CARTOON_WHITE)
        
        # Add impact effects in later frames
        if frame > 8:  # Last few frames show impact
            # Explosion clouds
            for i in range(3):
                cloud_x = 32 + (i - 1) * 15
                cloud_y = 50 + (i % 2) * 5
                cloud_size = 8 + i * 2
                draw.ellipse([cloud_x - cloud_size, cloud_y - cloud_size, 
                             cloud_x + cloud_size, cloud_y + cloud_size], 
                            fill=CARTOON_WHITE, outline=OUTLINE_BLACK, width=1)
            
            # Musical notes flying out
            note_positions = [(20, 30), (44, 25), (15, 45), (48, 40)]
            for i, (nx, ny) in enumerate(note_positions):
                if frame > 9 + i:
                    # Simple musical note
                    draw.ellipse([nx, ny, nx + 4, ny + 3], fill=OUTLINE_BLACK)
                    draw.line([(nx + 3, ny), (nx + 3, ny - 8)], fill=OUTLINE_BLACK, width=2)
        
        frames.append(img)
    
    # Save individual frames
    ensure_directory('assets/images/animations/piano_drop')
    for i, frame in enumerate(frames):
        frame.save(f'assets/images/animations/piano_drop/frame_{i:02d}.png')
    
    print(f"✓ Created {len(frames)} piano drop animation frames")
    return frames

def create_anvil_bounce_animation():
    """Create 10-frame Anvil Bounce Animation (64x64px)."""
    print("Creating Anvil Bounce Animation...")
    
    frames = []
    frame_count = 10
    
    for frame in range(frame_count):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Animation phases: compress spring (0-3), release (4-6), bounce (7-9)
        progress = frame / (frame_count - 1)
        
        # Spring compression/extension
        if frame <= 3:
            # Compression phase
            spring_compression = frame / 3.0
            spring_height = 20 - int(spring_compression * 8)  # Compress by 8 pixels
            anvil_y = 35 - int(spring_compression * 8)
        elif frame <= 6:
            # Release phase
            release_progress = (frame - 3) / 3.0
            spring_height = 12 + int(release_progress * 16)  # Extend beyond normal
            anvil_y = 27 - int(release_progress * 12)  # Anvil goes up
        else:
            # Settle phase
            settle_progress = (frame - 6) / 3.0
            spring_height = 28 - int(settle_progress * 8)  # Back to normal
            anvil_y = 15 + int(settle_progress * 12)  # Anvil settles down
        
        # Draw spring base
        spring_x = 26
        spring_base_y = 55
        spring_width = 12
        
        # Spring coils
        spring_color = ACME_YELLOW
        coil_count = max(3, spring_height // 4)
        for i in range(coil_count):
            coil_y = spring_base_y - (i + 1) * (spring_height // coil_count)
            draw.ellipse([spring_x, coil_y - 2, spring_x + spring_width, coil_y + 2], 
                        fill=spring_color, outline=OUTLINE_BLACK, width=2)
        
        # Draw anvil
        anvil_color = SILVER
        anvil_width = 20
        anvil_height = 15
        anvil_x = (64 - anvil_width) // 2
        
        # Anvil base
        draw.rectangle([anvil_x, anvil_y + 8, anvil_x + anvil_width, anvil_y + anvil_height], 
                      fill=anvil_color, outline=OUTLINE_BLACK, width=2)
        
        # Anvil horn
        draw.polygon([(anvil_x, anvil_y + 10), (anvil_x - 5, anvil_y + 12), (anvil_x, anvil_y + 14)], 
                    fill=anvil_color, outline=OUTLINE_BLACK, width=2)
        
        # Anvil face
        draw.rectangle([anvil_x + anvil_width, anvil_y + 9, anvil_x + anvil_width + 4, anvil_y + 14], 
                      fill=anvil_color, outline=OUTLINE_BLACK, width=2)
        
        # Anvil top
        draw.rectangle([anvil_x + 2, anvil_y, anvil_x + anvil_width - 2, anvil_y + 10], 
                      fill=anvil_color, outline=OUTLINE_BLACK, width=2)
        
        # Add motion lines during fast movement
        if 4 <= frame <= 6:
            # Speed lines during bounce
            for i in range(3):
                line_y = anvil_y + 5 + i * 4
                draw.line([(10, line_y), (15, line_y)], fill=OUTLINE_BLACK, width=1)
                draw.line([(49, line_y), (54, line_y)], fill=OUTLINE_BLACK, width=1)
        
        frames.append(img)
    
    # Save individual frames
    ensure_directory('assets/images/animations/anvil_bounce')
    for i, frame in enumerate(frames):
        frame.save(f'assets/images/animations/anvil_bounce/frame_{i:02d}.png')
    
    print(f"✓ Created {len(frames)} anvil bounce animation frames")
    return frames

def create_custard_pie_splash_animation():
    """Create 8-frame Custard Pie Splash Animation (64x64px)."""
    print("Creating Custard Pie Splash Animation...")
    
    frames = []
    frame_count = 8
    
    for frame in range(frame_count):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        progress = frame / (frame_count - 1)
        
        if frame < 3:
            # Pie approaching (frames 0-2)
            pie_x = int(10 + frame * 15)  # Moves from left to center
            pie_y = 25
            
            # Draw flying pie
            pie_color = ACME_YELLOW  # Custard color
            crust_color = "#8B4513"  # Brown crust
            
            # Pie crust
            draw.ellipse([pie_x, pie_y, pie_x + 15, pie_y + 12], 
                        fill=crust_color, outline=OUTLINE_BLACK, width=2)
            
            # Custard filling
            draw.ellipse([pie_x + 2, pie_y + 2, pie_x + 13, pie_y + 8], 
                        fill=pie_color, outline=OUTLINE_BLACK, width=1)
            
            # Motion lines
            for i in range(3):
                line_x = pie_x - 5 - i * 3
                line_y = pie_y + 4 + i
                draw.line([(line_x, line_y), (line_x + 8, line_y)], fill=OUTLINE_BLACK, width=1)
        
        else:
            # Impact and splash (frames 3-7)
            splash_frame = frame - 3
            splash_intensity = splash_frame / 4.0
            
            # Impact point
            impact_x, impact_y = 32, 30
            
            # Draw custard splatter
            custard_splats = [
                (impact_x, impact_y - 8, 6),      # Up
                (impact_x - 10, impact_y - 4, 5), # Left-up
                (impact_x + 10, impact_y - 4, 5), # Right-up
                (impact_x - 8, impact_y + 6, 4),  # Left-down
                (impact_x + 8, impact_y + 6, 4),  # Right-down
                (impact_x, impact_y + 10, 3),     # Down
            ]
            
            for i, (sx, sy, size) in enumerate(custard_splats):
                if splash_frame >= i * 0.5:  # Staggered appearance
                    splat_size = int(size * (1 + splash_intensity * 0.5))
                    draw.ellipse([sx - splat_size, sy - splat_size, 
                                 sx + splat_size, sy + splat_size], 
                                fill=ACME_YELLOW, outline=OUTLINE_BLACK, width=1)
            
            # Add pie crust fragments
            if splash_frame >= 1:
                crust_fragments = [
                    (impact_x - 6, impact_y - 6),
                    (impact_x + 6, impact_y - 8),
                    (impact_x - 4, impact_y + 8),
                    (impact_x + 8, impact_y + 6),
                ]
                
                for fx, fy in crust_fragments:
                    fragment_size = 3
                    draw.rectangle([fx, fy, fx + fragment_size, fy + fragment_size], 
                                  fill="#8B4513", outline=OUTLINE_BLACK, width=1)
            
            # Add impact stars
            if splash_frame >= 2:
                star_positions = [(impact_x - 12, impact_y), (impact_x + 12, impact_y), 
                                 (impact_x, impact_y - 12), (impact_x, impact_y + 12)]
                for star_x, star_y in star_positions:
                    # Simple 4-pointed star
                    draw.line([(star_x - 3, star_y), (star_x + 3, star_y)], 
                             fill=ACME_YELLOW, width=2)
                    draw.line([(star_x, star_y - 3), (star_x, star_y + 3)], 
                             fill=ACME_YELLOW, width=2)
        
        frames.append(img)
    
    # Save individual frames
    ensure_directory('assets/images/animations/custard_pie_splash')
    for i, frame in enumerate(frames):
        frame.save(f'assets/images/animations/custard_pie_splash/frame_{i:02d}.png')
    
    print(f"✓ Created {len(frames)} custard pie splash animation frames")
    return frames

def create_explosion_animation():
    """Create 10-frame Explosion Animation (64x64px)."""
    print("Creating Explosion Animation...")
    
    frames = []
    frame_count = 10
    
    for frame in range(frame_count):
        img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        progress = frame / (frame_count - 1)
        explosion_center = (32, 32)
        
        if frame < 3:
            # Initial flash and small explosion
            flash_size = 8 + frame * 4
            draw.ellipse([explosion_center[0] - flash_size, explosion_center[1] - flash_size,
                         explosion_center[0] + flash_size, explosion_center[1] + flash_size], 
                        fill=ACME_YELLOW, outline=ACME_RED, width=2)
        
        elif frame < 7:
            # Main explosion with expanding radius
            explosion_frame = frame - 3
            max_radius = 20
            radius = int(8 + explosion_frame * 3)
            
            # Multiple explosion rings
            colors = [ACME_RED, ORANGE, ACME_YELLOW, CARTOON_WHITE]
            for i, color in enumerate(colors):
                ring_radius = radius - i * 2
                if ring_radius > 0:
                    draw.ellipse([explosion_center[0] - ring_radius, explosion_center[1] - ring_radius,
                                 explosion_center[0] + ring_radius, explosion_center[1] + ring_radius], 
                                fill=color, outline=OUTLINE_BLACK, width=1)
            
            # Add radiating spikes
            spike_count = 8
            for i in range(spike_count):
                angle = (i * 360 / spike_count) * math.pi / 180
                spike_length = radius + 5
                spike_end_x = explosion_center[0] + math.cos(angle) * spike_length
                spike_end_y = explosion_center[1] + math.sin(angle) * spike_length
                
                # Thick spike line
                draw.line([explosion_center, (spike_end_x, spike_end_y)], 
                         fill=ACME_YELLOW, width=3)
                draw.line([explosion_center, (spike_end_x, spike_end_y)], 
                         fill=ACME_RED, width=1)
        
        else:
            # Smoke and dissipation
            smoke_frame = frame - 7
            smoke_alpha = max(100, 200 - smoke_frame * 50)
            
            # Smoke clouds
            smoke_positions = [
                (explosion_center[0] - 8, explosion_center[1] - 10),
                (explosion_center[0] + 6, explosion_center[1] - 8),
                (explosion_center[0] - 4, explosion_center[1] + 8),
                (explosion_center[0] + 10, explosion_center[1] + 6),
            ]
            
            for i, (smoke_x, smoke_y) in enumerate(smoke_positions):
                if smoke_frame >= i * 0.5:
                    cloud_size = 6 + smoke_frame * 2
                    # Gray smoke with transparency
                    smoke_color = DARK_GRAY
                    draw.ellipse([smoke_x - cloud_size, smoke_y - cloud_size,
                                 smoke_x + cloud_size, smoke_y + cloud_size], 
                                fill=smoke_color, outline=OUTLINE_BLACK, width=1)
        
        # Add "BOOM!" text in middle frames
        if 2 <= frame <= 5:
            try:
                # Try to use a bold font if available
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
            except:
                font = ImageFont.load_default()
            
            text = "BOOM!"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = (64 - text_width) // 2
            text_y = 45
            
            # Text with outline
            for adj in range(-1, 2):
                for adj2 in range(-1, 2):
                    if adj != 0 or adj2 != 0:
                        draw.text((text_x + adj, text_y + adj2), text, font=font, fill=OUTLINE_BLACK)
            draw.text((text_x, text_y), text, font=font, fill=CARTOON_WHITE)
        
        frames.append(img)
    
    # Save individual frames
    ensure_directory('assets/images/animations/explosion')
    for i, frame in enumerate(frames):
        frame.save(f'assets/images/animations/explosion/frame_{i:02d}.png')
    
    print(f"✓ Created {len(frames)} explosion animation frames")
    return frames

def create_css_animation_classes():
    """Create CSS file with animation keyframes for all animations."""
    print("Creating CSS animation classes...")
    
    css_content = '''/* =================================
   JAMES BLAND: ACME EDITION - ANIMATIONS
   Multi-frame animation sequences
   ================================= */

/* Piano Drop Animation */
@keyframes piano-drop {
    0% { background-image: url('../images/animations/piano_drop/frame_00.png'); }
    8.33% { background-image: url('../images/animations/piano_drop/frame_01.png'); }
    16.66% { background-image: url('../images/animations/piano_drop/frame_02.png'); }
    25% { background-image: url('../images/animations/piano_drop/frame_03.png'); }
    33.33% { background-image: url('../images/animations/piano_drop/frame_04.png'); }
    41.66% { background-image: url('../images/animations/piano_drop/frame_05.png'); }
    50% { background-image: url('../images/animations/piano_drop/frame_06.png'); }
    58.33% { background-image: url('../images/animations/piano_drop/frame_07.png'); }
    66.66% { background-image: url('../images/animations/piano_drop/frame_08.png'); }
    75% { background-image: url('../images/animations/piano_drop/frame_09.png'); }
    83.33% { background-image: url('../images/animations/piano_drop/frame_10.png'); }
    100% { background-image: url('../images/animations/piano_drop/frame_11.png'); }
}

.piano-drop-animation {
    width: 64px;
    height: 64px;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    animation: piano-drop 1s ease-in-out;
}

/* Anvil Bounce Animation */
@keyframes anvil-bounce {
    0% { background-image: url('../images/animations/anvil_bounce/frame_00.png'); }
    11.11% { background-image: url('../images/animations/anvil_bounce/frame_01.png'); }
    22.22% { background-image: url('../images/animations/anvil_bounce/frame_02.png'); }
    33.33% { background-image: url('../images/animations/anvil_bounce/frame_03.png'); }
    44.44% { background-image: url('../images/animations/anvil_bounce/frame_04.png'); }
    55.55% { background-image: url('../images/animations/anvil_bounce/frame_05.png'); }
    66.66% { background-image: url('../images/animations/anvil_bounce/frame_06.png'); }
    77.77% { background-image: url('../images/animations/anvil_bounce/frame_07.png'); }
    88.88% { background-image: url('../images/animations/anvil_bounce/frame_08.png'); }
    100% { background-image: url('../images/animations/anvil_bounce/frame_09.png'); }
}

.anvil-bounce-animation {
    width: 64px;
    height: 64px;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    animation: anvil-bounce 0.8s ease-out;
}

/* Custard Pie Splash Animation */
@keyframes custard-pie-splash {
    0% { background-image: url('../images/animations/custard_pie_splash/frame_00.png'); }
    14.28% { background-image: url('../images/animations/custard_pie_splash/frame_01.png'); }
    28.56% { background-image: url('../images/animations/custard_pie_splash/frame_02.png'); }
    42.84% { background-image: url('../images/animations/custard_pie_splash/frame_03.png'); }
    57.12% { background-image: url('../images/animations/custard_pie_splash/frame_04.png'); }
    71.4% { background-image: url('../images/animations/custard_pie_splash/frame_05.png'); }
    85.68% { background-image: url('../images/animations/custard_pie_splash/frame_06.png'); }
    100% { background-image: url('../images/animations/custard_pie_splash/frame_07.png'); }
}

.custard-pie-splash-animation {
    width: 64px;
    height: 64px;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    animation: custard-pie-splash 0.6s ease-in-out;
}

/* Explosion Animation */
@keyframes explosion {
    0% { background-image: url('../images/animations/explosion/frame_00.png'); }
    11.11% { background-image: url('../images/animations/explosion/frame_01.png'); }
    22.22% { background-image: url('../images/animations/explosion/frame_02.png'); }
    33.33% { background-image: url('../images/animations/explosion/frame_03.png'); }
    44.44% { background-image: url('../images/animations/explosion/frame_04.png'); }
    55.55% { background-image: url('../images/animations/explosion/frame_05.png'); }
    66.66% { background-image: url('../images/animations/explosion/frame_06.png'); }
    77.77% { background-image: url('../images/animations/explosion/frame_07.png'); }
    88.88% { background-image: url('../images/animations/explosion/frame_08.png'); }
    100% { background-image: url('../images/animations/explosion/frame_09.png'); }
}

.explosion-animation {
    width: 64px;
    height: 64px;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    animation: explosion 0.8s ease-out;
}

/* Utility Classes */
.animation-container {
    display: inline-block;
    position: relative;
}

.animation-once {
    animation-iteration-count: 1;
    animation-fill-mode: forwards;
}

.animation-loop {
    animation-iteration-count: infinite;
}

/* Animation trigger classes for JavaScript */
.trigger-piano-drop {
    animation-name: piano-drop;
}

.trigger-anvil-bounce {
    animation-name: anvil-bounce;
}

.trigger-custard-pie-splash {
    animation-name: custard-pie-splash;
}

.trigger-explosion {
    animation-name: explosion;
}
'''
    
    ensure_directory('assets/css')
    with open('assets/css/animations.css', 'w') as f:
        f.write(css_content)
    
    print("✓ Created animations.css with all animation keyframes")

def create_animation_manifest():
    """Create manifest file documenting all animations."""
    manifest_content = '''# Animation Assets Manifest - James Bland: ACME Edition

## Animation Specifications

### Piano Drop Animation
- **Frames**: 12
- **Dimensions**: 64×64px
- **Duration**: 1.0 seconds
- **Frame Rate**: 12 fps
- **CSS Class**: `.piano-drop-animation`
- **Trigger**: `.trigger-piano-drop`
- **Files**: `frame_00.png` through `frame_11.png`

### Anvil Bounce Animation  
- **Frames**: 10
- **Dimensions**: 64×64px
- **Duration**: 0.8 seconds
- **Frame Rate**: 12.5 fps
- **CSS Class**: `.anvil-bounce-animation`
- **Trigger**: `.trigger-anvil-bounce`
- **Files**: `frame_00.png` through `frame_09.png`

### Custard Pie Splash Animation
- **Frames**: 8
- **Dimensions**: 64×64px
- **Duration**: 0.6 seconds
- **Frame Rate**: 13.3 fps
- **CSS Class**: `.custard-pie-splash-animation`
- **Trigger**: `.trigger-custard-pie-splash`
- **Files**: `frame_00.png` through `frame_07.png`

### Explosion Animation
- **Frames**: 10  
- **Dimensions**: 64×64px
- **Duration**: 0.8 seconds
- **Frame Rate**: 12.5 fps
- **CSS Class**: `.explosion-animation`
- **Trigger**: `.trigger-explosion`
- **Files**: `frame_00.png` through `frame_09.png`

## Implementation Usage

### HTML Structure
```html
<div class="animation-container piano-drop-animation trigger-piano-drop"></div>
```

### JavaScript Trigger
```javascript
function playAnimation(element, animationType) {
    element.classList.add('trigger-' + animationType);
    element.addEventListener('animationend', function() {
        element.classList.remove('trigger-' + animationType);
    }, { once: true });
}
```

### CSS Import
```css
@import url('animations.css');
```

## File Structure
```
assets/images/animations/
├── piano_drop/
│   ├── frame_00.png through frame_11.png
├── anvil_bounce/
│   ├── frame_00.png through frame_09.png
├── custard_pie_splash/
│   ├── frame_00.png through frame_07.png
└── explosion/
    ├── frame_00.png through frame_09.png
```

## Integration Notes
- All animations use CSS keyframes with background-image switching
- Each frame is a separate PNG file with transparent background
- Animations can be triggered by adding CSS classes via JavaScript
- All assets follow ACME cartoon aesthetic with thick black outlines
- Frame dimensions optimized for mobile display
'''
    
    with open('assets/images/animations/ANIMATION_MANIFEST.md', 'w') as f:
        f.write(manifest_content)
    
    print("✓ Created animation manifest documentation")

def main():
    """Create all animation assets."""
    print("Creating Animation Assets for James Bland: ACME Edition")
    print("=" * 60)
    
    # Ensure base animation directory exists
    ensure_directory('assets/images/animations')
    
    # Create all animations
    create_piano_drop_animation()
    create_anvil_bounce_animation() 
    create_custard_pie_splash_animation()
    create_explosion_animation()
    
    # Create CSS and documentation
    create_css_animation_classes()
    create_animation_manifest()
    
    print("\n" + "=" * 60)
    print("✅ Animation Assets Creation Complete!")
    print("\nCreated Assets:")
    print("• Piano Drop Animation (12 frames)")
    print("• Anvil Bounce Animation (10 frames)")  
    print("• Custard Pie Splash Animation (8 frames)")
    print("• Explosion Animation (10 frames)")
    print("• CSS Animation Classes")
    print("• Animation Documentation")
    
    print("\nNext Steps:")
    print("1. Review generated animations in assets/images/animations/")
    print("2. Copy animations.css to static/css/ for web serving")
    print("3. Include animations.css in main stylesheet")
    print("4. Test animations in browser with JavaScript triggers")

if __name__ == "__main__":
    main() 