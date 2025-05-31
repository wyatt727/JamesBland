# James Bland: ACME Edition - Asset Specifications

This document tracks all required assets for the game, their specifications, and completion status.

## Audio Assets

### Sound Effects (`assets/audio/sfx/`)
- [ ] `anvil_drop.mp3` - Cartoon anvil "thud" sound (≤200 KB, ~1 sec)
- [ ] `piano_launch.mp3` - Piano whoosh + descending gliss (≤300 KB, ~1.5 sec)  
- [ ] `explosion_sizzle.mp3` - Cartoon explosion "boom" (≤250 KB, ~1 sec)

### Music (`assets/audio/music/`)
- [ ] `suspense_loop.mp3` - Planning phase background loop (30-60 sec, ≤1 MB)
- [ ] `victory_fanfare.mp3` - Victory celebration music (10-15 sec, ≤500 KB)

## Visual Assets

### UI Components (`assets/images/UI/`)
- [ ] `button_play.png` - 256×64px red button with "PLAY" text
- [ ] `button_settings.png` - 256×64px yellow button with gear icon + "SETTINGS"
- [ ] `panel_background.png` - 1024×768px tileable blueprint grid background

### Board Elements (`assets/images/board_tiles/`)
- [ ] `safe_house_icon.png` - 128×128px pastel blue fortress on springs
- [ ] `anvil_crate.png` - 128×128px wooden crate with silver anvil
- [ ] `spy_marker_default.png` - 64×64px spy silhouette with googly eyes

### Gadget Icons (`assets/images/gadgets/`)
- [ ] `spring_anvil.png` - 128×128px silver anvil on yellow spring
- [ ] `jetpack_skates.png` - 128×128px red skates with rocket flames
- [ ] `robo_duck.png` - 128×128px yellow duck with metal helmet
- [ ] `bug_detector.png` - 128×128px handheld radar device

## Typography (`assets/fonts/`)
- [ ] `acme_cartoon.ttf` - Bold cartoon display font
- [ ] `monospace_console.ttf` - Legible monospace font

## Color Palette Reference
- **ACME Red**: #E53935
- **ACME Yellow**: #FFEB3B  
- **ACME Blue**: #1E88E5
- **Outline Black**: #000000
- **Cartoon White**: #FFFFFF
- **Panel Gray**: #F2F2F2

## Asset Standards
- All PNGs should have transparent backgrounds
- All icons need thick black outlines (2-3px minimum)
- Touch targets must be ≥44×44px
- Audio files compressed for web delivery
- Mobile-optimized file sizes 