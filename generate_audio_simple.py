import numpy as np
import scipy.io.wavfile as wav
import os

def create_gentle_piano():
    """Create gentle piano-like tones"""
    sample_rate = 44100
    duration = 10  # 10 seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a sequence of soft sine waves at piano frequencies
    frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]  # C major scale
    audio = np.zeros_like(t)
    
    for i, freq in enumerate(frequencies):
        start_time = i * (duration / len(frequencies))
        end_time = (i + 1) * (duration / len(frequencies))
        mask = (t >= start_time) & (t < end_time)
        audio[mask] += 0.1 * np.sin(2 * np.pi * freq * t[mask])
    
    return audio, sample_rate

def create_forest_ambience():
    """Create forest-like ambient sounds"""
    sample_rate = 44100
    duration = 10
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create white noise for wind
    wind = 0.05 * np.random.randn(len(t))
    
    # Add bird chirps
    bird_chirps = np.zeros_like(t)
    for _ in range(5):
        start_time = np.random.uniform(0, duration - 1)
        chirp_duration = 0.5
        chirp_mask = (t >= start_time) & (t < start_time + chirp_duration)
        freq = 800 + np.random.randint(0, 400)
        bird_chirps[chirp_mask] += 0.08 * np.sin(2 * np.pi * freq * t[chirp_mask])
    
    return wind + bird_chirps, sample_rate

def create_ocean_waves():
    """Create ocean wave sounds"""
    sample_rate = 44100
    duration = 10
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    waves = np.zeros_like(t)
    for i in range(8):
        start_time = i * (duration / 8)
        wave_duration = 2
        wave_mask = (t >= start_time) & (t < start_time + wave_duration)
        # Create wave-like sound with varying frequency
        freq = 100 + 50 * np.sin(2 * np.pi * 0.5 * t[wave_mask])
        waves[wave_mask] += 0.1 * np.sin(2 * np.pi * freq * t[wave_mask])
    
    return waves, sample_rate

def create_rain_sounds():
    """Create rain sound effects"""
    sample_rate = 44100
    duration = 10
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a base rain sound with more consistent drops
    rain = np.zeros_like(t)
    
    # Create multiple layers of rain drops
    for _ in range(50):  # More drops
        start_time = np.random.uniform(0, duration - 0.2)
        drop_duration = np.random.uniform(0.05, 0.2)  # Varying drop durations
        drop_mask = (t >= start_time) & (t < start_time + drop_duration)
        
        if np.any(drop_mask):
            # Create a more realistic rain drop sound
            drop_samples = int(sample_rate * drop_duration)
            drop_sound = np.random.randn(drop_samples) * 0.1  # Louder drops
            
            # Add some frequency content to make it more realistic
            freq = np.random.uniform(200, 800)
            drop_tone = 0.05 * np.sin(2 * np.pi * freq * np.linspace(0, drop_duration, drop_samples))
            drop_sound += drop_tone
            
            # Apply to the main audio
            if len(drop_sound) <= len(rain[drop_mask]):
                rain[drop_mask][:len(drop_sound)] += drop_sound
    
    # Add some background rain ambience
    background_rain = 0.02 * np.random.randn(len(t))
    rain += background_rain
    
    return rain, sample_rate

def create_tibetan_bowls():
    """Create Tibetan bowl-like sounds"""
    sample_rate = 44100
    duration = 10
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create resonant tones similar to singing bowls
    frequencies = [147, 196, 220, 294, 330]  # Lower frequencies for bowls
    audio = np.zeros_like(t)
    
    for i, freq in enumerate(frequencies):
        start_time = i * (duration / len(frequencies))
        tone_duration = 3
        tone_mask = (t >= start_time) & (t < start_time + tone_duration)
        # Add some harmonics for bowl-like sound
        fundamental = np.sin(2 * np.pi * freq * t[tone_mask])
        harmonic1 = 0.5 * np.sin(2 * np.pi * freq * 2 * t[tone_mask])
        harmonic2 = 0.25 * np.sin(2 * np.pi * freq * 3 * t[tone_mask])
        audio[tone_mask] += 0.15 * (fundamental + harmonic1 + harmonic2)
    
    return audio, sample_rate

def create_silent_soft_music():
    """Create very gentle, barely audible background music"""
    sample_rate = 44100
    duration = 10
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create very soft, ambient tones
    audio = np.zeros_like(t)
    
    # Very low frequency, barely audible tones
    frequencies = [55, 110, 165]  # Very low frequencies
    for i, freq in enumerate(frequencies):
        # Create very soft sine waves
        tone = 0.005 * np.sin(2 * np.pi * freq * t)  # Extremely quiet
        audio += tone
    
    # Add very subtle white noise for ambient feel
    ambient_noise = 0.002 * np.random.randn(len(t))  # Very quiet noise
    audio += ambient_noise
    
    return audio, sample_rate

def save_audio(audio, sample_rate, filename):
    """Save audio as WAV file and convert to MP3"""
    # Check if audio has content
    max_val = np.max(np.abs(audio))
    if max_val == 0:
        print(f"⚠️ Warning: {filename} has no audio content")
        return
    
    # Normalize audio with safety check
    if max_val > 0:
        audio = audio / max_val
    
    # Convert to 16-bit integers
    audio_int = (audio * 32767).astype(np.int16)
    
    # Save as WAV first
    wav_filename = filename.replace('.mp3', '.wav')
    wav.write(wav_filename, sample_rate, audio_int)
    
    # Try to convert to MP3 using pydub if available
    try:
        from pydub import AudioSegment
        audio_segment = AudioSegment.from_wav(wav_filename)
        audio_segment.export(filename, format="mp3")
        os.remove(wav_filename)  # Remove the WAV file
        print(f"✅ Created {filename}")
    except:
        # If MP3 conversion fails, keep the WAV file
        os.rename(wav_filename, filename.replace('.mp3', '.wav'))
        print(f"✅ Created {filename.replace('.mp3', '.wav')} (WAV format)")

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
        "tibetan_bowls.mp3": create_tibetan_bowls,
        "silent_soft_music.mp3": create_silent_soft_music
    }
    
    for filename, generator_func in audio_files.items():
        print(f"Creating {filename}...")
        audio, sample_rate = generator_func()
        filepath = os.path.join("audio_files", filename)
        save_audio(audio, sample_rate, filepath)
    
    print("🎉 All calming audio files generated successfully!")

if __name__ == "__main__":
    main() 