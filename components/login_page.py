import streamlit as st
from auth.auth_utils import register_user, authenticate_user

def show_login_page():
    """Renders the login/signup page with the modern dark theme."""
    st.markdown(
        """
        <style>
        /* --- Import Google Font --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

        /* --- Animation Keyframes --- */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* --- Sleek Dark Theme --- */
        html, body {
            height: 100%;
            min-height: 100vh;
            background-color: #121212;
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stSidebar"] { display: none; }
        [data-testid="stHeader"] { display: none; }

        .block-container {
            background-color: #1E1E1E;
            border-radius: 16px;
            max-width: 420px;
            margin: auto;
            margin-top: 60px;
            padding: 2.5rem 3rem;
            border: 1px solid #2D2D2D;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            animation: fadeIn 0.5s ease-out;
        }

        .auth-title {
            text-align: center;
            font-size: 2.25rem;
            font-weight: 800;
            color: #F5F5F5;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            text-align: center;
            font-size: 1rem;
            color: #8A8A8A;
            margin-bottom: 2.5rem;
        }

        .auth-input input {
            width: 100%;
            padding: 0.8rem 1rem;
            margin-bottom: 1.25rem;
            border-radius: 8px;
            border: 1px solid #333333;
            background-color: #252525;
            color: #E0E0E0;
            font-size: 1rem;
            transition: all 0.2s ease-in-out;
        }

        .auth-input input::placeholder {
            color: #6c6c6c;
        }

        .auth-input input:focus {
            outline: none;
            border-color: #10B981;
            background-color: #1E1E1E;
            box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
        }

        .auth-button {
            display: flex;
            justify-content: center;
            width: 100%;
        }

        .auth-button button {
            width: 100%;
            padding: 0.85rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            border: none;
            color: #121212;
            margin-top: 0.5rem;
            cursor: pointer;
            background-color: #10B981;
            transition: background-color 0.2s ease;
        }

        .auth-button button:hover {
            background-color: #14D396;
        }

        .switch-link {
            display: flex;
            justify-content: center;
            width: 100%;
            margin-top: 1.5rem;
        }

        .switch-link button {
            background: none;
            color: #8A8A8A;
            border: none;
            font-size: 0.95rem;
            text-decoration: none;
            cursor: pointer;
            transition: color 0.2s;
        }

        .switch-link button:hover {
            color: #10B981;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False

    is_signup = st.session_state.show_signup
    title = "Create Your Account" if is_signup else "Welcome Back"
    subtitle_text = "Join TalkHeal to get started" if is_signup else "Login to continue your journey"

    st.markdown(f'<div class="auth-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{subtitle_text}</div>', unsafe_allow_html=True)

    form_container = st.container()

    if is_signup:
        with form_container:
            name = st.text_input("Name", placeholder="Enter your full name", label_visibility="collapsed", key="signup_name")
            email = st.text_input("Email", placeholder="your.email@example.com", label_visibility="collapsed", key="signup_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed", key="signup_password")

            st.markdown('<div class="auth-button">', unsafe_allow_html=True)
            if st.button("Sign Up", key="signup_submit"):
                if not name or not email or not password:
                    st.warning("Please fill out all fields.")
                else:
                    success, message = register_user(name, email, password)
                    if success:
                        st.success("Account created! You can now login.")
                        st.session_state.show_signup = False
                        st.rerun()
                    else:
                        st.error(message)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="switch-link">', unsafe_allow_html=True)
            if st.button("Already have an account? Login", key="switch_to_login"):
                st.session_state.show_signup = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        with form_container:
            email = st.text_input("Email", placeholder="your.email@example.com", label_visibility="collapsed", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed", key="login_password")

            st.markdown('<div class="auth-button">', unsafe_allow_html=True)
            if st.button("Login", key="login_submit"):
                if not email or not password:
                    st.warning("Please enter your email and password.")
                else:
                    success, user = authenticate_user(email, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_name = user['name']
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="switch-link">', unsafe_allow_html=True)
            if st.button("Don't have an account? Sign up", key="switch_to_signup"):
                st.session_state.show_signup = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# Main app logic
if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    if not st.session_state.authenticated:
        show_login_page()
    else:
        st.title(f"🎉 Welcome, {st.session_state.user_name}!")
        st.success("You're logged in!")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_name = ""
            st.rerun()
