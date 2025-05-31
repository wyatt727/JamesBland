# Animation Assets Manifest - James Bland: ACME Edition

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
