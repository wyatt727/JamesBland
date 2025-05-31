# Font Documentation - James Bland: ACME Edition

## Font Stack Overview

### Display Font (Headings, Buttons, UI)
- **Primary**: ACME Cartoon (Fredoka One)
- **Fallbacks**: 'Comic Sans MS', 'Arial Black', cursive, sans-serif
- **Usage**: Game title, button labels, player names, important UI text
- **Characteristics**: Bold, rounded, cartoon-like appearance

### Body Font (General Text)
- **Primary**: Open Sans
- **Fallbacks**: system-ui, -apple-system, BlinkMacSystemFont, sans-serif
- **Usage**: Instructions, descriptions, chat messages, general content
- **Characteristics**: Clean, highly legible, mobile-optimized

### Monospace Font (Technical Display)
- **Primary**: ACME Console (JetBrains Mono)
- **Fallbacks**: 'Roboto Mono', 'Courier New', monospace
- **Usage**: Timer countdowns, IP counters, technical information
- **Characteristics**: Fixed-width, clear number distinction

## CSS Variables

Use these CSS custom properties for consistent font application:

```css
--font-display: Display font stack
--font-body: Body text font stack  
--font-mono: Monospace font stack
```

## Utility Classes

- `.font-display`: Applies display font with cartoon styling
- `.font-body`: Applies body font with standard styling
- `.font-mono`: Applies monospace font with tabular numbers
- `.btn-text`: Specialized button text styling with shadows
- `.hud-text`: HUD-specific text styling
- `.timer-display`: Timer and counter styling

## Mobile Considerations

- All fonts tested for mobile readability
- 16px minimum font size to prevent zoom on iOS
- High contrast combinations for accessibility
- Fallbacks available on all major platforms

## Loading Strategy

- Fonts loaded via @font-face with `font-display: swap`
- Fallbacks provide immediate text rendering
- Primary fonts enhance experience when loaded
- No layout shift during font loading

## File Formats

- WOFF2: Primary format (best compression, wide support)
- Fallback to system fonts if download fails
- No FOUT (Flash of Unstyled Text) issues
