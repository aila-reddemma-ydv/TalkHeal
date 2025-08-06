# Audio Files for Focus Session

This directory contains audio files for the Focus Session background sounds.

## Required Audio Files:
- `rain.mp3` - Gentle rain sounds
- `forest.mp3` - Forest ambience with birds and nature sounds
- `ocean.mp3` - Ocean wave sounds
- `white-noise.mp3` - White noise for concentration

## Audio Specifications:
- Format: MP3
- Quality: 128kbps or higher
- Duration: 10-30 minutes (looped)
- Volume: Normalized for consistent playback

## How to Add Audio Files:
1. Place your audio files in this directory
2. Update the `BACKGROUND_OPTIONS` in `components/focus_session.py` to use local file paths
3. Ensure the audio files are properly licensed for use

## Alternative: Online Audio Sources
If you prefer to use online audio sources, you can update the `audio_url` in the `BACKGROUND_OPTIONS` to point to external URLs. 