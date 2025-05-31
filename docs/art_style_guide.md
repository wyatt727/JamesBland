# James Bland: ACME Edition - Art Style Guide

## 1. Overall Aesthetic

James Bland: ACME Edition embraces the classic **ACME cartoon aesthetic** popularized by Warner Bros. and similar animation studios. The visual style is deliberately exaggerated, colorful, and playful, emphasizing:

- **Bright primary colors** with high saturation
- **Thick black outlines** around all visual elements
- **Exaggerated proportions** and cartoonish forms
- **Minimal realistic shading** in favor of flat, bold colors
- **Slapstick visual humor** through expressive iconography

The entire game should feel like a living cartoon where every interaction could result in an anvil dropping from the sky or a piano exploding in a cloud of musical notes.

## 2. Color Palette

### 2.1 Primary Colors

**ACME Red** (`#E53935`)
- Used for: Action highlights, "Confirm" buttons, critical warnings, danger indicators
- Usage: Backgrounds for primary action buttons, alert text, destructive gadget effects
- Accessibility: Provides strong contrast against white text

**ACME Yellow** (`#FFEB3B`) 
- Used for: Caution highlights, hover states, gadget icons, warning indicators
- Usage: Button hover effects, selected state backgrounds, attention-grabbing elements
- Accessibility: Requires dark text overlay for readability

**ACME Blue** (`#1E88E5`)
- Used for: Neutral UI backgrounds, Safe House icons, informational elements
- Usage: Panel backgrounds, defensive action indicators, secondary buttons
- Accessibility: Works well with both light and dark text

### 2.2 Secondary Colors

**Outline Black** (`#000000`)
- Used for: Thick outlines around every visual element (2-3px minimum)
- Usage: Button borders, icon outlines, text shadows, panel borders
- Purpose: Creates the distinctive cartoon aesthetic and improves visual clarity

**Cartoon White** (`#FFFFFF`)
- Used for: Text on colored backgrounds, highlights, panel interiors
- Usage: Button text, popup backgrounds, contrast elements
- Purpose: Maximum contrast and readability

**Panel Gray** (`#F2F2F2`)
- Used for: Background panels, dropdown interiors, inactive states
- Usage: Main panel backgrounds, disabled button states, neutral areas
- Purpose: Subtle backgrounds that don't compete with primary colors

### 2.3 Status Colors

**Active Green** (`#4CAF50`)
- Used for: Active player status, successful actions, positive feedback
- Usage: Player status borders, success animations, positive IP changes

**Compromised Yellow** (`#FF9800`) 
- Used for: Compromised player status, warning states
- Usage: Player status borders, caution indicators

**Burned Orange** (`#FF5722`)
- Used for: Burned player status, moderate danger states
- Usage: Player status borders, warning animations

**Captured Red** (`#D32F2F`)
- Used for: Captured player status, high danger, errors
- Usage: Player status borders, error messages, negative feedback

**Eliminated Black** (`#424242`)
- Used for: Eliminated players, ghost mode indicators
- Usage: Grayed-out elements, ghost player indicators

## 3. Typography

### 3.1 Display Font

**Primary**: "Fredoka One" (Google Fonts) or similar cartoon-style font
- **Characteristics**: Bold, rounded letterforms with slight irregularity
- **Usage**: Headings, button labels, gadget names, player codenames
- **Styling**: Always uppercase for headings, thick letter spacing
- **Fallback**: "Comic Sans MS", "Arial Black", sans-serif

**CSS Implementation**:
```css
.display-text {
  font-family: 'Fredoka One', 'Comic Sans MS', 'Arial Black', sans-serif;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-shadow: 2px 2px 0px #000;
}
```

### 3.2 Body Font

**Primary**: "Open Sans" (Google Fonts) or system sans-serif
- **Characteristics**: Clean, highly legible, mobile-optimized
- **Usage**: Body text, tooltips, descriptions, chat messages
- **Weights**: Regular (400), Bold (600)
- **Fallback**: system-ui, -apple-system, sans-serif

**CSS Implementation**:
```css
.body-text {
  font-family: 'Open Sans', system-ui, -apple-system, sans-serif;
  font-weight: 400;
  line-height: 1.4;
}
```

### 3.3 Monospace Font

**Primary**: "Roboto Mono" (Google Fonts)
- **Usage**: Timer countdowns, IP counters, technical displays
- **Characteristics**: Fixed-width, clear number distinction
- **Fallback**: "Courier New", monospace

## 4. UI Components

### 4.1 Buttons

**Primary Action Buttons**
- **Minimum size**: 44×44px (touch-friendly)
- **Border radius**: 8px (rounded corners)
- **Border**: 3px solid black
- **Background**: Primary color (red for confirm, blue for neutral, yellow for special)
- **Text**: White, uppercase, bold with black text-shadow
- **Hover effect**: Slight scale transform (1.05x) and inner glow

**Secondary Buttons**
- **Background**: Panel gray with primary color border
- **Text**: Black, normal case
- **Hover effect**: Background shifts to light primary color

**CSS Example**:
```css
.primary-button {
  min-width: 44px;
  min-height: 44px;
  border: 3px solid #000;
  border-radius: 8px;
  background: #E53935;
  color: #fff;
  font-family: 'Fredoka One', sans-serif;
  text-transform: uppercase;
  text-shadow: 1px 1px 0px #000;
  cursor: pointer;
  transition: transform 0.1s ease;
}

.primary-button:hover {
  transform: scale(1.05);
  box-shadow: inset 0 0 10px rgba(255,255,255,0.3);
}
```

### 4.2 Panels and Containers

**Main Panels**
- **Background**: Panel gray (#F2F2F2) or white
- **Border**: 2px solid black
- **Border radius**: 8px
- **Drop shadow**: `box-shadow: 3px 3px 0px #000`
- **Padding**: Minimum 16px on mobile, 24px on larger screens

**Modal Dialogs**
- **Background**: White with 4px black border
- **Overlay**: Semi-transparent black (rgba(0,0,0,0.7))
- **Animation**: Scale in from center with slight bounce

### 4.3 Form Elements

**Dropdowns**
- **Background**: White with black border
- **Height**: 44px minimum
- **Font**: Body font, 16px (prevents zoom on iOS)
- **Selected state**: Yellow background
- **Border radius**: 4px

**Text Inputs**
- **Background**: White
- **Border**: 2px solid black, yellow when focused
- **Height**: 44px minimum
- **Padding**: 12px horizontal
- **Font**: Body font, 16px

**Sliders (for IP allocation)**
- **Track**: Gray background with black outline
- **Handle**: Yellow circle with black border
- **Active track**: Blue fill
- **Height**: 44px touch area

## 5. Iconography and Sprites

### 5.1 Icon Style Guidelines

**General Characteristics**
- **Size**: 128×128px base resolution (scalable)
- **Style**: Flat design with black outlines
- **Color**: Use primary palette, avoid gradients
- **Detail level**: Simple shapes, avoid fine details that don't scale well

**Gadget Icons**
- **Spring-Loaded Anvil**: Classic black anvil with yellow spring coil underneath
- **Jetpack Roller Skates**: Red roller skates with blue flame jets
- **Robo-Duck Patrol**: Yellow rubber duck with silver robotic antenna
- **Biplane**: Red vintage biplane with yellow propeller
- **Explosives Box**: Brown crate with "TNT" label and red warning symbols

**Action Icons**
- **Assassination**: Black gun with yellow muzzle flash
- **Sabotage**: Gray wrench with yellow sparks
- **Surveillance**: Blue magnifying glass with yellow lens
- **Defense**: Blue shield with white cross

### 5.2 Player Avatars

**Style**: Cartoon spy silhouettes with distinctive accessories
- **Basic Shape**: Simple head and shoulders silhouette
- **Size**: 64×64px in-game, 128×128px for lobby
- **Variations**: Different hat styles, glasses, bow ties for personalization
- **Colors**: Solid colors matching the primary palette
- **Border**: Always 2px black outline

**Avatar Options**:
1. **Classic Spy**: Black fedora, dark sunglasses
2. **Tech Specialist**: Round glasses, blue cap
3. **Femme Fatale**: Red beret, pearl necklace outline
4. **Gadget Expert**: Yellow hard hat, tool belt outline
5. **Master of Disguise**: Multiple overlapping hat silhouettes
6. **International Agent**: Various cultural hat styles

### 5.3 Board and Background Elements

**Background Patterns**
- **Blueprint style**: Light blue background with white grid lines
- **ACME logo**: Subtle watermark in corners
- **Border decorations**: Small cartoon bomb, anvil, and spring motifs

**Strategic Asset Icons**
- **ACME Bank**: Yellow building with dollar sign and black vault door
- **ACME Armory**: Gray building with red warning triangles
- **ACME Broadcast Station**: Blue tower with yellow lightning bolts
- **ACME Black Market**: Purple building with question mark
- **ACME Tunnel Hub**: Brown entrance with yellow "TUNNEL" sign

## 6. Animation Guidelines

### 6.1 UI Animations

**Timing**
- **Button interactions**: 100-150ms for immediate feedback
- **Panel transitions**: 200-300ms for smooth but snappy feel
- **Modal appearances**: 300-500ms with easing for dramatic effect

**Easing Functions**
- **Buttons**: `ease-out` for natural feel
- **Panels**: `ease-in-out` for smooth transitions
- **Modals**: `cubic-bezier(0.68, -0.55, 0.265, 1.55)` for bounce effect

**CSS Examples**:
```css
.button-press {
  animation: button-press 150ms ease-out;
}

@keyframes button-press {
  0% { transform: scale(1); }
  50% { transform: scale(0.95); }
  100% { transform: scale(1); }
}

.modal-enter {
  animation: modal-enter 400ms cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes modal-enter {
  0% { 
    transform: scale(0.3);
    opacity: 0;
  }
  100% { 
    transform: scale(1);
    opacity: 1;
  }
}
```

### 6.2 Game Animations

**Action Resolution**
- **Piano Drop**: Large piano sprite falls from top of screen with rotation
- **Anvil Bounce**: Anvil drops and bounces twice with squash-and-stretch
- **Explosion**: Burst of yellow and red particles with screen shake
- **Banner Plane**: Small biplane sprite moves across screen with trailing banner

**Status Changes**
- **Player Compromised**: Yellow warning triangle appears above avatar
- **Player Eliminated**: Avatar fades to grayscale with ghost overlay
- **IP Changes**: Floating numbers (+2 IP or -1 IP) with fade-out animation

### 6.3 Performance Considerations

**Mobile Optimization**
- **Prefer CSS animations** over JavaScript for better performance
- **Use transform and opacity** properties for hardware acceleration
- **Limit concurrent animations** to 3-4 maximum
- **Provide motion-reduced alternatives** for accessibility

**Reduced Motion**
```css
@media (prefers-reduced-motion: reduce) {
  .animated-element {
    animation: none;
    transition: none;
  }
}
```

## 7. Mobile-Specific Considerations

### 7.1 Touch Targets

**Minimum Sizes**
- **Primary buttons**: 44×44px minimum
- **Secondary actions**: 36×36px minimum
- **Text links**: 32px height minimum
- **Spacing**: 8px minimum between touch targets

### 7.2 Screen Scaling

**Breakpoints**
- **Small phones**: 320px width (scaling factor 0.8x)
- **Standard phones**: 375px width (scaling factor 1.0x)
- **Large phones/small tablets**: 768px width (scaling factor 1.2x)
- **Tablets**: 1024px+ width (scaling factor 1.5x)

**Responsive Elements**
- **Text sizes**: Scale proportionally with viewport
- **Icon sizes**: Use rem units for consistent scaling
- **Panel layouts**: Stack vertically on narrow screens

### 7.3 Performance on Mobile

**Image Optimization**
- **Format**: Use WebP with PNG fallback
- **Compression**: Optimize for file size while maintaining cartoon clarity
- **Loading**: Lazy load non-critical images
- **Caching**: Implement aggressive caching for repeated game assets

## 8. Accessibility

### 8.1 Color Contrast

**WCAG 2.1 AA Compliance**
- **Text on backgrounds**: Minimum 4.5:1 contrast ratio
- **Large text (18px+)**: Minimum 3:1 contrast ratio
- **Interactive elements**: Clear visual focus indicators

**High Contrast Mode**
- **Provide alternative color scheme** for accessibility settings
- **Maintain thick black outlines** for shape definition
- **Use patterns and textures** as color alternatives

### 8.2 Visual Indicators

**Status Communication**
- **Never rely on color alone** for status information
- **Use icons, shapes, and text** as additional indicators
- **Player status**: Combine color borders with icon overlays

### 8.3 Font Legibility

**Sizing**
- **Minimum body text**: 16px on mobile
- **Heading text**: 20px+ on mobile
- **Critical information**: 18px+ on mobile

**Line Height**
- **Body text**: 1.4-1.6 line height
- **Headings**: 1.2-1.3 line height
- **Buttons**: 1.0 line height (centered)

## 9. Implementation Notes

### 9.1 Asset Organization

**Directory Structure**
```
/static/assets/
├── icons/
│   ├── gadgets/
│   ├── actions/
│   └── ui/
├── avatars/
├── backgrounds/
└── animations/
```

**Naming Conventions**
- **Icons**: `icon-{category}-{name}.svg` (e.g., `icon-gadget-anvil.svg`)
- **Avatars**: `avatar-{style}.svg` (e.g., `avatar-fedora.svg`)
- **Backgrounds**: `bg-{location}.jpg` (e.g., `bg-blueprint.jpg`)

### 9.2 CSS Variables

**Color Variables**
```css
:root {
  --acme-red: #E53935;
  --acme-yellow: #FFEB3B;
  --acme-blue: #1E88E5;
  --outline-black: #000000;
  --cartoon-white: #FFFFFF;
  --panel-gray: #F2F2F2;
  
  --status-active: #4CAF50;
  --status-compromised: #FF9800;
  --status-burned: #FF5722;
  --status-captured: #D32F2F;
  --status-eliminated: #424242;
}
```

**Typography Variables**
```css
:root {
  --font-display: 'Fredoka One', 'Comic Sans MS', sans-serif;
  --font-body: 'Open Sans', system-ui, sans-serif;
  --font-mono: 'Roboto Mono', 'Courier New', monospace;
  
  --text-shadow-heavy: 2px 2px 0px var(--outline-black);
  --text-shadow-light: 1px 1px 0px var(--outline-black);
}
```

### 9.3 Component Library

**Reusable Components**
- **Button variants**: Primary, secondary, danger, success
- **Panel types**: Game panel, modal, tooltip
- **Status indicators**: Player status, IP display, timer
- **Form elements**: Dropdown, slider, text input

This style guide ensures visual consistency across all game elements while maintaining the playful, cartoon aesthetic that makes James Bland: ACME Edition distinctive and engaging. 