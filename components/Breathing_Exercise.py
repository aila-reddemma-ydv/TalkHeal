import streamlit as st
import time

def breathing_exercise():
    st.markdown("<h2 style='text-align: center; color: teal;'>🧘 Breathing Exercise</h2>", unsafe_allow_html=True)

    st.markdown("### 👇 Follow the animation to breathe in and out")
    st.write("Use this simple breathing exercise to relax. Follow the circle expanding and contracting.")

    circle_animation = """
    <style>
    @keyframes breathe {
      0% { transform: scale(1); }
      25% { transform: scale(1.5); }
      50% { transform: scale(1); }
      75% { transform: scale(0.75); }
      100% { transform: scale(1); }
    }

    .breathing-circle {
      margin: auto;
      margin-top: 50px;
      height: 150px;
      width: 150px;
      border-radius: 50%;
      background-color: #90e0ef;
      animation: breathe 8s ease-in-out infinite;
    }
    </style>

    <div class="breathing-circle"></div>
    """
    st.markdown(circle_animation, unsafe_allow_html=True)

    breath_text = st.empty()

    if st.button("🌀 Start Breathing"):
        for _ in range(3):
            breath_text.markdown("## 🌬️ Breathe In...")
            time.sleep(4)
            breath_text.markdown("## ✋ Hold...")
            time.sleep(2)
            breath_text.markdown("## 😮‍💨 Breathe Out...")
            time.sleep(4)
        breath_text.markdown("### ✅ Done! Feel better?")

    with st.expander("🕒 Need a Timer?"):
        minutes = st.slider("How many minutes do you want to do this?", 1, 10, 2)
        if st.button("Start Timer"):
            st.success("Relax and follow the animation...")
            timer_placeholder = st.empty()
            for i in range(minutes * 60, 0, -1):
                mins, secs = divmod(i, 60)
                timer_text = f"{mins:02d}:{secs:02d}"
                timer_placeholder.markdown(f"## ⏳ {timer_text}")
                time.sleep(1)
            timer_placeholder.markdown("### ✅ Timer complete!")

if __name__ == "__main__":
    breathing_exercise()
