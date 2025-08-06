import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise
import os

def create_gentle_piano():
    """Create gentle piano-like tones"""
    # Create a sequence of soft sine waves at piano frequencies
    frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]  # C major scale
    audio = AudioSegment.empty()
    
    for freq in frequencies:
        tone = Sine(freq).to_audio_segment(duration=2000)  # 2 seconds each
        tone = tone - 20  # Reduce volume
        audio += tone
    
    # Loop to make it longer
    audio = audio * 3  # Repeat 3 times
    return audio

def create_forest_ambience():
    """Create forest-like ambient sounds"""
    # Create white noise with some filtering to simulate wind
    noise = WhiteNoise().to_audio_segment(duration=10000)  # 10 seconds
    noise = noise - 30  # Reduce volume significantly
    
    # Add some bird-like chirps (high frequency tones)
    bird_chirps = AudioSegment.empty()
    for _ in range(5):
        chirp = Sine(800 + np.random.randint(0, 400)).to_audio_segment(duration=500)
        chirp = chirp - 25
        bird_chirps += chirp + AudioSegment.silent(duration=1500)
    
    return noise + bird_chirps

def create_ocean_waves():
    """Create ocean wave sounds"""
    # Create wave-like sounds using filtered noise
    waves = AudioSegment.empty()
    
    for _ in range(8):
        # Create a wave sound
        wave = WhiteNoise().to_audio_segment(duration=2000)
        wave = wave - 25  # Reduce volume
        waves += wave + AudioSegment.silent(duration=1000)
    
    return waves

def create_rain_sounds():
    """Create rain sound effects"""
    # Create rain drops using short noise bursts
    rain = AudioSegment.empty()
    
    for _ in range(20):
        drop = WhiteNoise().to_audio_segment(duration=100)
        drop = drop - 35  # Very quiet
        rain += drop + AudioSegment.silent(duration=np.random.randint(200, 800))
    
    return rain

def create_tibetan_bowls():
    """Create Tibetan bowl-like sounds"""
    # Create resonant tones similar to singing bowls
    frequencies = [147, 196, 220, 294, 330]  # Lower frequencies for bowls
    audio = AudioSegment.empty()
    
    for freq in frequencies:
        tone = Sine(freq).to_audio_segment(duration=3000)
        tone = tone - 15  # Moderate volume
        audio += tone + AudioSegment.silent(duration=1000)
    
    return audio

def main():
    """Generate all calming audio files"""
    print("🎵 Generating calming audio files...")
    
    # Ensure audio_files directory exists
    if not os.path.exists("audio_files"):
        os.makedirs("audio_files")
    
    # Generate each audio file
    audio_files = {
        "gentle_piano.mp3": create_gentle_piano,
        "forest_ambience.mp3": create_forest_ambience,
        "ocean_waves.mp3": create_ocean_waves,
        "rain_sounds.mp3": create_rain_sounds,
        "tibetan_bowls.mp3": create_tibetan_bowls
    }
    
    for filename, generator_func in audio_files.items():
        print(f"Creating {filename}...")
        audio = generator_func()
        filepath = os.path.join("audio_files", filename)
        audio.export(filepath, format="mp3")
        print(f"✅ Created {filename}")
    
    print("🎉 All calming audio files generated successfully!")

if __name__ == "__main__":
    main() 