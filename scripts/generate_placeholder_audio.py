#!/usr/bin/env python3
"""
Placeholder Audio Generator for James Bland: ACME Edition
Generates basic audio assets matching game specifications for development use.
"""

import numpy as np
import os
from scipy.io.wavfile import write
import tempfile

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a sine wave at given frequency and duration."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def generate_descending_gliss(start_freq, end_freq, duration, sample_rate=44100, amplitude=0.3):
    """Generate a descending glissando (smooth frequency slide)."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Exponential frequency decay for more musical effect
    frequencies = start_freq * np.exp(np.log(end_freq / start_freq) * t / duration)
    wave = amplitude * np.sin(2 * np.pi * np.cumsum(frequencies) / sample_rate)
    return wave

def apply_envelope(wave, attack=0.1, decay=0.1, sustain=0.7, release=0.2):
    """Apply ADSR envelope to a wave."""
    length = len(wave)
    envelope = np.ones(length)
    
    # Attack
    attack_samples = int(attack * length)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    
    # Decay + Sustain
    decay_samples = int(decay * length)
    if decay_samples > 0:
        envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain, decay_samples)
    
    # Release
    release_samples = int(release * length)
    if release_samples > 0:
        envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)
    
    return wave * envelope

def save_as_mp3(wave_data, filename, sample_rate=44100):
    """Save wave data as MP3 file."""
    # First save as WAV, then convert to MP3
    wav_filename = filename.replace('.mp3', '.wav')
    
    # Convert to 16-bit PCM
    wave_int16 = np.int16(wave_data * 32767)
    write(wav_filename, sample_rate, wave_int16)
    
    try:
        # Try to convert to MP3 using ffmpeg (if available)
        import subprocess
        result = subprocess.run(['ffmpeg', '-i', wav_filename, '-acodec', 'mp3', 
                               '-ab', '128k', '-y', filename], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            os.remove(wav_filename)  # Remove temporary WAV file
            print(f"✓ Created {filename} (MP3)")
        else:
            # Keep as WAV if MP3 conversion fails
            print(f"✓ Created {wav_filename} (WAV - ffmpeg not available)")
    except FileNotFoundError:
        # ffmpeg not available, keep as WAV
        print(f"✓ Created {wav_filename} (WAV - ffmpeg not available)")

def create_anvil_drop():
    """Create cartoon anvil drop sound effect."""
    print("Creating anvil drop sound...")
    
    # Combine multiple elements for cartoon anvil sound
    sample_rate = 44100
    
    # Whoosh sound (high frequency sweep down)
    whoosh_duration = 0.3
    whoosh = generate_descending_gliss(800, 200, whoosh_duration, sample_rate, 0.2)
    
    # Impact sound (low frequency thud)
    impact_duration = 0.4
    impact_freq = 80
    impact = generate_sine_wave(impact_freq, impact_duration, sample_rate, 0.5)
    # Add some noise for metallic ring
    ring_freq = 320
    ring = generate_sine_wave(ring_freq, impact_duration, sample_rate, 0.1)
    impact = impact + ring
    
    # Apply envelope to impact
    impact = apply_envelope(impact, attack=0.01, decay=0.3, sustain=0.3, release=0.4)
    
    # Silence between whoosh and impact
    silence_duration = 0.1
    silence = np.zeros(int(silence_duration * sample_rate))
    
    # Combine all parts
    full_sound = np.concatenate([whoosh, silence, impact])
    
    # Add some final reverb-like decay
    decay_duration = 0.2
    decay = np.zeros(int(decay_duration * sample_rate))
    full_sound = np.concatenate([full_sound, decay])
    
    save_as_mp3(full_sound, 'assets/audio/sfx/anvil_drop.mp3', sample_rate)

def create_piano_launch():
    """Create piano launch with descending glissando."""
    print("Creating piano launch sound...")
    
    sample_rate = 44100
    
    # Launch whoosh (ascending then quick descent)
    launch_duration = 0.5
    launch = generate_descending_gliss(200, 600, launch_duration * 0.3, sample_rate, 0.3)
    
    # Piano glissando (descending chromatic-ish scale)
    gliss_duration = 1.0
    # Simulate piano notes by combining harmonics
    gliss = np.zeros(int(gliss_duration * sample_rate))
    
    # Create descending "piano" notes
    start_note = 880  # A5
    end_note = 220    # A3
    num_notes = 12    # Chromatic descent
    
    for i in range(num_notes):
        note_start = i * gliss_duration / num_notes
        note_duration = 0.15
        
        # Calculate note frequency
        progress = i / (num_notes - 1)
        note_freq = start_note * (end_note / start_note) ** progress
        
        # Generate note with harmonics (piano-like)
        fundamental = generate_sine_wave(note_freq, note_duration, sample_rate, 0.3)
        harmonic2 = generate_sine_wave(note_freq * 2, note_duration, sample_rate, 0.1)
        harmonic3 = generate_sine_wave(note_freq * 3, note_duration, sample_rate, 0.05)
        
        note = fundamental + harmonic2 + harmonic3
        note = apply_envelope(note, attack=0.01, decay=0.3, sustain=0.3, release=0.4)
        
        # Place note in timeline
        start_sample = int(note_start * sample_rate)
        end_sample = min(start_sample + len(note), len(gliss))
        note_len = end_sample - start_sample
        
        gliss[start_sample:end_sample] += note[:note_len]
    
    # Combine launch and glissando
    full_sound = np.concatenate([launch, gliss])
    
    save_as_mp3(full_sound, 'assets/audio/sfx/piano_launch.mp3', sample_rate)

def create_explosion_sizzle():
    """Create cartoon explosion sound."""
    print("Creating explosion sound...")
    
    sample_rate = 44100
    duration = 1.0
    
    # Generate noise-based explosion
    explosion_samples = int(duration * sample_rate)
    
    # White noise base
    noise = np.random.uniform(-1, 1, explosion_samples) * 0.4
    
    # Filter to create more explosion-like sound (emphasize lower frequencies)
    # Simple low-pass filter simulation
    filtered_noise = np.zeros_like(noise)
    for i in range(1, len(noise)):
        filtered_noise[i] = 0.7 * filtered_noise[i-1] + 0.3 * noise[i]
    
    # Add some tonal components for cartoon effect
    low_boom = generate_sine_wave(60, duration, sample_rate, 0.3)
    mid_crack = generate_sine_wave(200, duration * 0.5, sample_rate, 0.2)
    
    # Combine elements
    explosion = filtered_noise + low_boom
    explosion[:len(mid_crack)] += mid_crack
    
    # Apply explosive envelope (quick attack, long decay)
    explosion = apply_envelope(explosion, attack=0.01, decay=0.4, sustain=0.1, release=0.5)
    
    save_as_mp3(explosion, 'assets/audio/sfx/explosion_sizzle.mp3', sample_rate)

def create_suspense_loop():
    """Create suspense background music loop."""
    print("Creating suspense loop...")
    
    sample_rate = 44100
    duration = 30.0  # 30 second loop
    
    # Simple suspenseful chord progression
    # Use minor chords for tension
    base_freq = 110  # A2
    
    # Chord progression: Am - F - C - G (simplified)
    chord_duration = duration / 4
    
    music = np.zeros(int(duration * sample_rate))
    
    # Define chords (simplified as root + fifth + octave)
    chords = [
        [110, 165, 220],  # A minor
        [87, 131, 175],   # F major
        [131, 196, 262],  # C major
        [98, 147, 196]    # G major
    ]
    
    for i, chord in enumerate(chords):
        chord_start = i * chord_duration
        
        # Generate chord tones
        chord_sound = np.zeros(int(chord_duration * sample_rate))
        
        for freq in chord:
            tone = generate_sine_wave(freq, chord_duration, sample_rate, 0.15)
            # Add some tremolo for suspense
            tremolo = 1 + 0.1 * np.sin(2 * np.pi * 4 * np.linspace(0, chord_duration, len(tone)))
            tone = tone * tremolo
            chord_sound += tone
        
        # Apply envelope to chord
        chord_sound = apply_envelope(chord_sound, attack=0.1, decay=0.2, sustain=0.7, release=0.1)
        
        # Place in full music
        start_sample = int(chord_start * sample_rate)
        end_sample = min(start_sample + len(chord_sound), len(music))
        chord_len = end_sample - start_sample
        
        music[start_sample:end_sample] += chord_sound[:chord_len]
    
    save_as_mp3(music, 'assets/audio/music/suspense_loop.mp3', sample_rate)

def create_victory_fanfare():
    """Create victory celebration fanfare."""
    print("Creating victory fanfare...")
    
    sample_rate = 44100
    duration = 12.0
    
    # Classic victory fanfare progression
    # Triumphant ascending melody
    
    notes = [
        (262, 0.5),  # C4
        (294, 0.5),  # D4
        (330, 0.5),  # E4
        (349, 0.5),  # F4
        (392, 1.0),  # G4 (hold)
        (523, 0.5),  # C5
        (587, 0.5),  # D5
        (659, 1.5),  # E5 (hold longer)
        (523, 0.5),  # C5
        (392, 2.0),  # G4 (final hold)
    ]
    
    fanfare = np.zeros(int(duration * sample_rate))
    current_time = 0
    
    for freq, note_duration in notes:
        if current_time + note_duration > duration:
            note_duration = duration - current_time
        
        if note_duration <= 0:
            break
        
        # Generate note with harmonics for fanfare effect
        fundamental = generate_sine_wave(freq, note_duration, sample_rate, 0.4)
        harmonic2 = generate_sine_wave(freq * 2, note_duration, sample_rate, 0.1)
        harmonic3 = generate_sine_wave(freq * 3, note_duration, sample_rate, 0.05)
        
        note = fundamental + harmonic2 + harmonic3
        note = apply_envelope(note, attack=0.05, decay=0.1, sustain=0.8, release=0.05)
        
        # Place note in timeline
        start_sample = int(current_time * sample_rate)
        end_sample = min(start_sample + len(note), len(fanfare))
        note_len = end_sample - start_sample
        
        fanfare[start_sample:end_sample] += note[:note_len]
        
        current_time += note_duration
    
    save_as_mp3(fanfare, 'assets/audio/music/victory_fanfare.mp3', sample_rate)

def main():
    """Generate all placeholder audio assets."""
    print("Generating placeholder audio assets for James Bland: ACME Edition")
    print("=" * 70)
    
    # Ensure directories exist
    os.makedirs('assets/audio/sfx', exist_ok=True)
    os.makedirs('assets/audio/music', exist_ok=True)
    
    try:
        # Check for required dependencies
        try:
            import numpy as np
            import scipy.io.wavfile
        except ImportError:
            print("❌ Required dependencies missing. Please install:")
            print("   pip install numpy scipy")
            return
        
        create_anvil_drop()
        create_piano_launch()
        create_explosion_sizzle()
        create_suspense_loop()
        create_victory_fanfare()
        
        print("\n" + "=" * 70)
        print("✓ All placeholder audio assets generated successfully!")
        print("Audio files created in the assets/audio/ directory")
        print("\nNote: These are basic synthesized placeholders.")
        print("For production, consider using professional audio assets.")
        print("\nNext steps:")
        print("1. Test audio playback in browsers")
        print("2. Copy to static/ directory for web serving")
        print("3. Replace with professional audio if needed")
        
    except Exception as e:
        print(f"\n❌ Error generating audio assets: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 