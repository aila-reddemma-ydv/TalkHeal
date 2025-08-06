import streamlit as st
import time
from datetime import datetime, timedelta
import random
import pygame
import requests
import os
import threading

# Focus session configurations
FOCUS_DURATIONS = [
    {"name": "Quick Break", "minutes": 5, "description": "Perfect for a short mental reset"},
    {"name": "Pomodoro", "minutes": 25, "description": "Classic focus technique"},
    {"name": "Deep Work", "minutes": 50, "description": "Extended concentration session"},
    {"name": "Mindful Hour", "minutes": 60, "description": "Full hour of focused time"},
    {"name": "Custom Time", "minutes": None, "description": "Set your own duration"}
]

# Motivational quotes for during sessions
MOTIVATIONAL_QUOTES = [
    "Breathe in peace, exhale stress.",
    "You are stronger than you think.",
    "One moment at a time, one breath at a time.",
    "Your mind is a garden. Tend to it with care.",
    "Progress, not perfection.",
    "You've got this. Take it step by step.",
    "Every breath is a fresh start.",
    "You are capable of amazing things.",
    "Stay present, stay focused.",
    "Your well-being matters."
]

# Audio management
AUDIO_FILES_DIR = "audio_files"
if not os.path.exists(AUDIO_FILES_DIR):
    os.makedirs(AUDIO_FILES_DIR)

# Updated Audio URLs for 5 calming music types
AUDIO_URLS = {
    "gentle_piano": "https://www.soundjay.com/misc/sounds/piano-1.mp3",
    "forest_ambience": "https://www.soundjay.com/misc/sounds/forest-01.mp3", 
    "ocean_waves": "https://www.soundjay.com/misc/sounds/ocean-wave-1.mp3",
    "rain_sounds": "https://www.soundjay.com/misc/sounds/rain-01.mp3",
    "tibetan_bowls": "https://www.soundjay.com/misc/sounds/white-noise-1.mp3"
}

# Initialize pygame mixer
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
except:
    st.warning("Audio playback may not work properly. Please ensure pygame is installed.")

# Updated calming background options with 7 music types
BACKGROUND_OPTIONS = [
    {"name": "No Music", "description": "No background audio - pure focus", "audio_type": None},
    {"name": "Gentle Piano", "description": "Soft piano melodies for deep meditation", "audio_type": "gentle_piano"},
    {"name": "Forest Ambience", "description": "Nature sounds for grounding and peace", "audio_type": "forest_ambience"},
    {"name": "Ocean Waves", "description": "Calming wave sounds for relaxation", "audio_type": "ocean_waves"},
    {"name": "Rain Sounds", "description": "Gentle rain for focus and tranquility", "audio_type": "rain_sounds"},
    {"name": "Tibetan Bowls", "description": "Healing frequencies for deep calm", "audio_type": "tibetan_bowls"},
    {"name": "Silent Soft Music", "description": "Barely audible ambient tones for subtle focus", "audio_type": "silent_soft_music"}
]

def create_sample_audio_files():
    """Create sample audio files if they don't exist"""
    sample_files = {
        "gentle_piano.mp3": "Sample gentle piano meditation music",
        "forest_ambience.mp3": "Sample forest nature sounds", 
        "ocean_waves.mp3": "Sample ocean wave sounds",
        "rain_sounds.mp3": "Sample rain ambience",
        "tibetan_bowls.mp3": "Sample Tibetan singing bowl sounds"
    }
    
    for filename, description in sample_files.items():
        filepath = os.path.join(AUDIO_FILES_DIR, filename)
        if not os.path.exists(filepath):
            # Create a simple text file as placeholder
            with open(filepath, 'w') as f:
                f.write(f"# {description}\n")
                f.write("# This is a placeholder file for calming music\n")
                f.write("# In a real implementation, this would be an actual MP3 file\n")
            st.info(f"📁 Created placeholder for {filename}")

def download_audio_file(audio_type):
    """Get audio file path - check for local files first"""
    if not audio_type:
        return None
    
    # Check for WAV files first (our generated files)
    wav_filename = f"{audio_type}.wav"
    wav_filepath = os.path.join(AUDIO_FILES_DIR, wav_filename)
    
    if os.path.exists(wav_filepath):
        return wav_filepath
    
    # Check for MP3 files
    mp3_filename = f"{audio_type}.mp3"
    mp3_filepath = os.path.join(AUDIO_FILES_DIR, mp3_filename)
    
    if os.path.exists(mp3_filepath):
        return mp3_filepath
    
    # If no local file exists, try to download
    if audio_type in AUDIO_URLS:
        try:
            response = requests.get(AUDIO_URLS[audio_type], stream=True, timeout=10)
            response.raise_for_status()
            
            with open(mp3_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            st.success(f"✅ Downloaded {audio_type} audio file")
            return mp3_filepath
        except Exception as e:
            st.warning(f"⚠️ Could not download {audio_type} audio: {str(e)}")
            return None
    
    return None

def play_audio(audio_type):
    """Play audio using pygame"""
    if not audio_type:
        return
    
    filepath = download_audio_file(audio_type)
    if not filepath:
        st.info(f"🎵 {audio_type.replace('_', ' ').title()} music would play here")
        st.session_state.audio_playing = True
        return
    
    try:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        st.session_state.audio_playing = True
        st.success(f"🎵 Now playing: {audio_type.replace('_', ' ').title()} background music")
    except Exception as e:
        st.warning(f"⚠️ Could not play audio: {str(e)}")
        st.info(f"🎵 {audio_type.replace('_', ' ').title()} music would play here")
        st.session_state.audio_playing = True

def stop_audio():
    """Stop audio playback"""
    try:
        pygame.mixer.music.stop()
        st.session_state.audio_playing = False
        st.info("🔇 Audio stopped")
    except Exception as e:
        st.session_state.audio_playing = False
        st.info("🔇 Audio stopped")

def pause_audio():
    """Pause audio playback"""
    try:
        pygame.mixer.music.pause()
        st.session_state.audio_playing = False
        st.info("⏸️ Audio paused")
    except Exception as e:
        st.session_state.audio_playing = False
        st.info("⏸️ Audio paused")

def unpause_audio():
    """Unpause audio playback"""
    try:
        pygame.mixer.music.unpause()
        st.session_state.audio_playing = True
        st.success("▶️ Audio resumed")
    except Exception as e:
        st.session_state.audio_playing = True
        st.success("▶️ Audio resumed")

def initialize_focus_state():
    """Initialize focus session state variables"""
    if "focus_session_active" not in st.session_state:
        st.session_state.focus_session_active = False
    if "focus_start_time" not in st.session_state:
        st.session_state.focus_start_time = None
    if "focus_duration" not in st.session_state:
        st.session_state.focus_duration = None
    if "focus_paused" not in st.session_state:
        st.session_state.focus_paused = False
    if "focus_pause_start" not in st.session_state:
        st.session_state.focus_pause_start = None
    if "focus_sessions_completed" not in st.session_state:
        st.session_state.focus_sessions_completed = 0
    if "focus_session_logs" not in st.session_state:
        st.session_state.focus_session_logs = []
    if "selected_background" not in st.session_state:
        st.session_state.selected_background = None
    if "audio_playing" not in st.session_state:
        st.session_state.audio_playing = False
    if "show_custom_time_input" not in st.session_state:
        st.session_state.show_custom_time_input = False
    if "selected_duration_type" not in st.session_state:
        st.session_state.selected_duration_type = None
    if "audio_auto_played" not in st.session_state:
        st.session_state.audio_auto_played = False
    if "audio_was_playing_before_pause" not in st.session_state:
        st.session_state.audio_was_playing_before_pause = False
    if "timer_start" not in st.session_state:
        st.session_state.timer_start = datetime.now()
    if "last_timer_update" not in st.session_state:
        st.session_state.last_timer_update = datetime.now()
    if "auto_refresh_counter" not in st.session_state:
        st.session_state.auto_refresh_counter = 0
    if "last_update" not in st.session_state:
        st.session_state.last_update = datetime.now()
    if "focus_session_completed" not in st.session_state:
        st.session_state.focus_session_completed = False

def format_time(seconds):
    """Format seconds into MM:SS display"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def get_breathing_animation():
    """Return breathing animation HTML"""
    return """
    <div class="breathing-animation">
        <div class="breathing-circle"></div>
        <p class="breathing-text">Breathe in...</p>
    </div>
    <style>
    .breathing-animation {
        text-align: center;
        margin: 20px 0;
    }
    .breathing-circle {
        width: 100px;
        height: 100px;
        border: 3px solid #40A578;
        border-radius: 50%;
        margin: 0 auto 10px;
        animation: breathe 4s ease-in-out infinite;
    }
    .breathing-text {
        color: #40A578;
        font-size: 18px;
        font-weight: 500;
        margin: 0;
    }
    @keyframes breathe {
        0%, 100% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.2); opacity: 1; }
    }
    </style>
    """

def render_audio_controls(audio_type, auto_play=False):
    """Render audio controls using Streamlit buttons"""
    st.markdown("**🎵 Background Audio Controls**")
    
    # Handle no music option
    if not audio_type:
        st.info("🔇 **No Music Selected** - Pure focus without any background audio")
        st.markdown("""
        <div style="background: rgba(59, 130, 246, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #3b82f6;">
            <p style="margin: 0; font-size: 14px; color: #1e40af;">
                💡 <strong>No Music Benefits:</strong>
                <br>🎯 Maximum concentration without any distractions
                <br>🧠 Better for deep thinking and problem-solving
                <br>🫁 Perfect for breathing exercises and meditation
                <br>⚡ Ideal for high-focus tasks and study sessions
                <br>🔇 Complete silence for pure mindfulness
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Auto-play when session starts
    if auto_play and not st.session_state.get("audio_auto_played", False):
        play_audio(audio_type)
        st.session_state.audio_auto_played = True
        st.rerun()
    
    # Audio control buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔊 Play", use_container_width=True, type="primary"):
            play_audio(audio_type)
            st.rerun()
    
    with col2:
        if st.button("⏸️ Pause", use_container_width=True, type="secondary"):
            pause_audio()
            st.rerun()
    
    with col3:
        if st.button("▶️ Resume", use_container_width=True, type="secondary"):
            unpause_audio()
            st.rerun()
    
    with col4:
        if st.button("🔇 Stop", use_container_width=True, type="secondary"):
            stop_audio()
            st.rerun()
    
    # Show current audio status (only if audio is playing)
    if st.session_state.get("audio_playing", False):
        st.success("🎵 Background music is currently playing")

def render_focus_setup():
    """Render the focus session setup screen"""
    # Back button
    if st.button("← Back to Chat", type="primary"):
        st.session_state.show_focus_session = False
        st.rerun()
    
    st.markdown("""
    <div class="main-header">
        <h1>🧘 Focus Session</h1>
        <p>Take a mindful break to reduce stress and improve focus</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Duration selection
    st.subheader("⏱️ Choose Your Session Duration")
    duration_cols = st.columns(2)
    
    selected_duration = None
    for i, duration in enumerate(FOCUS_DURATIONS):
        with duration_cols[i % 2]:
            if st.button(
                f"**{duration['name']}**\n{duration['minutes'] if duration['minutes'] else 'Custom'} minutes\n*{duration['description']}*",
                key=f"duration_{i}",
                use_container_width=True,
                type="primary"
            ):
                if duration['name'] == "Custom Time":
                    st.session_state.show_custom_time_input = True
                    st.session_state.selected_duration_type = duration
                else:
                    selected_duration = duration
                    st.session_state.focus_duration = duration
                    st.session_state.focus_session_active = True
                    st.session_state.focus_start_time = datetime.now()
                    st.rerun()
    
    # Custom time input
    if st.session_state.get("show_custom_time_input", False):
        st.markdown("---")
        st.subheader("⏰ Set Custom Duration")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            custom_hours = st.number_input("Hours", min_value=0, max_value=12, value=0, key="custom_hours")
        with col2:
            custom_minutes = st.number_input("Minutes", min_value=0, max_value=59, value=15, key="custom_minutes")
        with col3:
            custom_seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, key="custom_seconds")
        
        total_custom_seconds = custom_hours * 3600 + custom_minutes * 60 + custom_seconds
        total_custom_minutes = total_custom_seconds / 60
        
        if total_custom_seconds > 0:
            # Format display time
            display_hours = int(total_custom_seconds // 3600)
            display_minutes = int((total_custom_seconds % 3600) // 60)
            display_seconds = int(total_custom_seconds % 60)
            
            if display_hours > 0:
                time_display = f"{display_hours}h {display_minutes}m {display_seconds}s"
            elif display_minutes > 0:
                time_display = f"{display_minutes}m {display_seconds}s"
            else:
                time_display = f"{display_seconds}s"
            
            st.info(f"📅 Total Duration: {time_display} ({total_custom_seconds} seconds)")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Start Custom Session", use_container_width=True, type="primary"):
                    custom_duration = {
                        "name": f"Custom ({time_display})",
                        "minutes": total_custom_minutes,
                        "seconds": total_custom_seconds,
                        "description": "Your personalized focus session"
                    }
                    st.session_state.focus_duration = custom_duration
                    st.session_state.focus_session_active = True
                    st.session_state.focus_start_time = datetime.now()
                    st.session_state.show_custom_time_input = False
                    st.rerun()
            
            with col2:
                if st.button("❌ Cancel", use_container_width=True, type="secondary"):
                    st.session_state.show_custom_time_input = False
                    st.rerun()
    
    # Background selection
    st.subheader("🎵 Choose Your Background Music (Optional)")
    background_option = st.selectbox(
        "Select calming background:",
        options=BACKGROUND_OPTIONS,
        format_func=lambda x: f"{x['name']} - {x['description']}",
        index=4,  # Default to silence
        key="background_selector"
    )
    
    # Store selected background
    st.session_state.selected_background = background_option
    
    # Music preview
    if background_option and background_option['audio_type']:
        
        # Preview audio controls
        render_audio_controls(background_option['audio_type'])
        
        st.info("💡 **Tip**: Use the controls above to preview the background music. This will help you choose the perfect sound for your focus session.")
    
    # Session statistics
    if st.session_state.focus_sessions_completed > 0:
        st.markdown("---")
        st.subheader("📊 Your Focus Journey")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sessions Completed", st.session_state.focus_sessions_completed)
        with col2:
            total_minutes = sum(log['duration'] for log in st.session_state.focus_session_logs)
            st.metric("Total Focus Time", f"{total_minutes} min")
        with col3:
            if st.session_state.focus_session_logs:
                avg_duration = total_minutes / len(st.session_state.focus_session_logs)
                st.metric("Average Session", f"{avg_duration:.1f} min")

def render_active_session():
    """Render the active focus session"""
    if not st.session_state.focus_session_active:
        return
    
    # Simple timer display
    if not st.session_state.focus_paused:
        # Show session is active
        st.info("⏰ Focus Session Active")
    
    # Calculate remaining time
    now = datetime.now()
    if st.session_state.focus_paused:
        elapsed = (st.session_state.focus_pause_start - st.session_state.focus_start_time).total_seconds()
    else:
        elapsed = (now - st.session_state.focus_start_time).total_seconds()
    
    # Use seconds field if available, otherwise calculate from minutes
    if 'seconds' in st.session_state.focus_duration:
        total_seconds = st.session_state.focus_duration['seconds']
    else:
        total_seconds = st.session_state.focus_duration['minutes'] * 60
    
    remaining_seconds = max(0, total_seconds - elapsed)
    
    # Check if session is complete
    if remaining_seconds <= 0:
        complete_session()
        st.rerun()  # Force page refresh to show completion screen
        return
    
    # Session header
    duration_display = st.session_state.focus_duration['name']
    if 'seconds' in st.session_state.focus_duration:
        # For custom sessions, the name already includes the formatted time
        duration_display = st.session_state.focus_duration['name']
    else:
        # For predefined sessions, show minutes
        duration_display = f"{st.session_state.focus_duration['name']} ({st.session_state.focus_duration['minutes']} minutes)"
    
    st.markdown(f"""
    <div class="main-header">
        <h1>🧘 Focus Session in Progress</h1>
        <p>Duration: {duration_display}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Timer display - Simple and clean
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="focus-session-timer">
            <h2>{format_time(int(remaining_seconds))}</h2>
            <p>Time Remaining</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar - Simple and clean
    progress = max(0.0, min(1.0, 1 - (remaining_seconds / total_seconds)))
    st.progress(progress)
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏸️ Pause" if not st.session_state.focus_paused else "▶️ Resume", 
                    use_container_width=True, type="secondary"):
            if st.session_state.focus_paused:
                # Resume
                pause_duration = (now - st.session_state.focus_pause_start).total_seconds()
                st.session_state.focus_start_time += timedelta(seconds=pause_duration)
                st.session_state.focus_paused = False
                st.session_state.focus_pause_start = None
                # Resume audio if it was playing before pause
                if st.session_state.audio_was_playing_before_pause and st.session_state.selected_background and st.session_state.selected_background['audio_type']:
                    unpause_audio()
                    st.session_state.audio_was_playing_before_pause = False
            else:
                # Pause
                st.session_state.focus_paused = True
                st.session_state.focus_pause_start = now
                # Track if audio was playing before pause
                st.session_state.audio_was_playing_before_pause = st.session_state.get("audio_playing", False)
                # Pause audio if it's playing
                if st.session_state.get("audio_playing", False):
                    pause_audio()
            st.rerun()
    
    with col2:
        if st.button("⏹️ End Session", use_container_width=True, type="primary"):
            # Stop any playing audio
            stop_audio()
            # Reset audio state
            st.session_state.audio_playing = False
            st.session_state.audio_auto_played = False
            st.session_state.audio_was_playing_before_pause = False
            st.session_state.focus_session_active = False
            st.rerun()
    
    with col3:
        if st.button("🔄 Restart", use_container_width=True, type="secondary"):
            # Stop current audio and reset audio state
            stop_audio()
            st.session_state.audio_playing = False
            st.session_state.audio_auto_played = False
            st.session_state.audio_was_playing_before_pause = False
            # Reset session state
            st.session_state.focus_start_time = datetime.now()
            st.session_state.focus_paused = False
            st.session_state.focus_pause_start = None
            st.rerun()
    
    # Handle background audio or silence
    if st.session_state.selected_background:
        if st.session_state.selected_background['audio_type']:
            # Auto-play background music when session starts
            if not st.session_state.get("audio_auto_played", False):
                play_audio(st.session_state.selected_background['audio_type'])
                st.session_state.audio_auto_played = True
                st.rerun()
            
            # Show simple audio status and stop button
            if st.session_state.get("audio_playing", False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    music_name = st.session_state.selected_background['name']
                    st.success(f"🎵 {music_name} is playing")
                with col2:
                    if st.button("🔇 Stop Music", use_container_width=True, type="secondary"):
                        stop_audio()
                        st.rerun()
        else:
            # No music mode
            st.info("🔇 **No Music Mode** - Enjoy pure focus without any background audio")
    
    # Breathing animation and motivational content
    st.markdown("---")
    
    # Breathing animation
    st.markdown(get_breathing_animation(), unsafe_allow_html=True)
    
    # Motivational quote
    quote = random.choice(MOTIVATIONAL_QUOTES)
    st.markdown(f"""
    <div class="focus-quote-box">
        <p style="color: #1e3a8a; font-size: 24px; font-weight: bold; text-align: center; margin: 20px 0;">"{quote}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Session tips
    with st.expander("💡 Focus Tips", expanded=False):
        st.markdown("""
        <div style="color: black; line-height: 1.8; font-size: 16px;">
        <p style="margin: 8px 0; color: black;"><strong>🫁 Breathe deeply</strong> - Follow the animation above</p>
        <p style="margin: 8px 0; color: black;"><strong>🎯 Stay present</strong> - Focus on one task at a time</p>
        <p style="margin: 8px 0; color: black;"><strong>💝 Be kind to yourself</strong> - It's okay if your mind wanders</p>
        <p style="margin: 8px 0; color: black;"><strong>⏸️ Take breaks</strong> - Listen to your body's needs</p>
        </div>
        """, unsafe_allow_html=True)
    


def complete_session():
    """Handle session completion"""
    st.session_state.focus_session_active = False
    st.session_state.focus_session_completed = True  # Add completion flag
    
    # Stop any playing audio and reset audio state
    stop_audio()
    st.session_state.audio_playing = False
    st.session_state.audio_auto_played = False
    st.session_state.audio_was_playing_before_pause = False
    
    # Log the session
    if 'seconds' in st.session_state.focus_duration:
        # For custom sessions, log the total seconds
        logged_duration = st.session_state.focus_duration['seconds']
    else:
        # For predefined sessions, log the minutes
        logged_duration = st.session_state.focus_duration['minutes']
    
    session_log = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'duration': logged_duration,
        'completed': True
    }
    st.session_state.focus_session_logs.append(session_log)
    st.session_state.focus_sessions_completed += 1

def render_completion_screen():
    """Render the session completion screen"""
    # Completion message
    st.markdown("""
    <div class="main-header">
        <h1>🎉 Focus Session Complete!</h1>
        <p>Great job taking time for yourself</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show completion status with more prominence
    st.success(f"✅ **Session Complete!** You've successfully completed your {st.session_state.focus_duration['name']} focus session!")
    
    # Add a visual separator
    st.markdown("---")
    
    # Show session summary
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📅 **Session Duration**: {st.session_state.focus_duration['name']}")
    with col2:
        st.info(f"🎵 **Background**: {st.session_state.selected_background['name'] if st.session_state.selected_background else 'No Music'}")
    
    # Post-session mood check
    st.subheader("💭 How are you feeling now?")
    post_mood = st.radio(
        "Rate your current mood:",
        options=["😔 Stressed", "😐 Neutral", "😊 Calm", "😄 Refreshed", "🌟 Energized"],
        horizontal=True,
        key="post_focus_mood"
    )
    
    # Follow-up suggestions
    st.subheader("🔄 What would you like to do next?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Journal My Thoughts", use_container_width=True):
            st.session_state.pre_filled_chat_input = f"Just completed a {st.session_state.focus_duration['name']} focus session. Feeling {post_mood}. "
            st.session_state.send_chat_message = True
            st.rerun()
    
    with col2:
        if st.button("🧘 Another Session", use_container_width=True):
            st.session_state.focus_session_completed = False
            st.rerun()
    
    with col3:
        if st.button("🏠 Back to Chat", use_container_width=True):
            st.session_state.focus_session_completed = False
            st.session_state.show_focus_session = False
            st.rerun()
    
    # Breathing exercise reminder
    st.info("💡 **Tip**: Take a few deep breaths to carry this calm feeling forward into your day.")

def render_focus_session():
    """Main function to render the focus session feature"""
    initialize_focus_state()
    
    if st.session_state.get("focus_session_completed", False):
        render_completion_screen()
    elif st.session_state.focus_session_active:
        render_active_session()
    else:
        render_focus_setup() 