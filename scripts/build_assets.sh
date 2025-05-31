#!/bin/bash
# James Bland: ACME Edition - Asset Build Script
# Copies assets from source directories to static directories for web serving

echo "James Bland: ACME Edition - Building Assets"

# Create static directories if they don't exist
echo "Creating static directories..."
mkdir -p static/audio/sfx
mkdir -p static/audio/music
mkdir -p static/fonts
mkdir -p static/images/UI
mkdir -p static/images/board_tiles
mkdir -p static/images/gadgets

# Copy audio files if they exist
echo "Copying audio assets..."
if [ -d "assets/audio/sfx" ]; then
    cp assets/audio/sfx/*.mp3 static/audio/sfx/ 2>/dev/null || echo "No SFX files found"
fi

if [ -d "assets/audio/music" ]; then
    cp assets/audio/music/*.mp3 static/audio/music/ 2>/dev/null || echo "No music files found"
fi

# Copy font files if they exist
echo "Copying font assets..."
if [ -d "assets/fonts" ]; then
    cp assets/fonts/*.ttf static/fonts/ 2>/dev/null || echo "No TTF fonts found"
    cp assets/fonts/*.woff* static/fonts/ 2>/dev/null || echo "No WOFF fonts found"
fi

# Copy image files if they exist
echo "Copying image assets..."
if [ -d "assets/images/UI" ]; then
    cp assets/images/UI/*.png static/images/UI/ 2>/dev/null || echo "No UI images found"
fi

if [ -d "assets/images/board_tiles" ]; then
    cp assets/images/board_tiles/*.png static/images/board_tiles/ 2>/dev/null || echo "No board tile images found"
fi

if [ -d "assets/images/gadgets" ]; then
    cp assets/images/gadgets/*.png static/images/gadgets/ 2>/dev/null || echo "No gadget images found"
fi

echo "Asset build complete!"
echo "Run 'python server.py' to start the game server" 