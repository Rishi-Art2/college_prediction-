import streamlit as st
from database import init_db, add_user, authenticate_user
from supabase import create_client, Client

# ---------------- Page Config ---------------- #
st.set_page_config(
    page_title="Admit Sure",
    page_icon="🎓",
    layout="centered"
)

init_db()

# ---------------- Session ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- Login ---------------- #
def login_form():
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    remember = st.checkbox("Remember Me")

    if st.button("Login", use_container_width=True, type="primary"):

        if username == "" or password == "":
            st.warning("Please enter username and password.")
            return

        user = authenticate_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.user = user

            st.success(f"Welcome {user['username']} 🎉")
            st.rerun()

        else:
            st.error("Invalid username or password.")

    st.markdown("---")
    from supabase import create_client

SUPABASE_URL = "https://uchmareibvcqiajcqlbl.supabase.co"
SUPABASE_KEY = "sb_publishable_veEkVtKRnJOzpT1CpprI9Q_7sq_gij-"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

if st.button("🔵 Continue with Google"):
    response = supabase.auth.sign_in_with_oauth(
        {
            "provider": "google",
            "options": {
                "redirect_to": "https://cutoff-prediction.streamlit.app"
            }
        }
    )

# ---------------- Signup ---------------- #
def signup_form():
    st.subheader("📝 Create Account")

    username = st.text_input("Username", key="su_user")
    email = st.text_input("Email", key="su_email")
    password = st.text_input("Password", type="password", key="su_pass")
    confirm = st.text_input("Confirm Password", type="password", key="su_confirm")

    agree = st.checkbox("I agree to Terms & Conditions")

    if st.button("Create Account", use_container_width=True, type="primary"):

        if not username or not email or not password or not confirm:
            st.warning("Please fill all fields.")
            return

        if password != confirm:
            st.error("Passwords do not match.")
            return

        if len(password) < 6:
            st.error("Password must contain at least 6 characters.")
            return

        if not agree:
            st.warning("Please accept Terms & Conditions.")
            return

        success, message = add_user(username, email, password)

        if success:
            st.success(message)
        else:
            st.error(message)

    st.markdown("---")
    st.button("🔵 Sign up with Google", use_container_width=True)

# ---------------- Main ---------------- #
st.title("🎓 Admit Sure")
st.caption("Predict colleges based on your entrance exam percentile.")

if st.session_state.logged_in:

    st.success(f"Welcome **{st.session_state.user['username']}**")

    st.info("Use the sidebar to access Predict College and History.")

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

else:

    login_tab, signup_tab = st.tabs(["🔐 Login", "📝 Sign Up"])

    with login_tab:
        login_form()

    with signup_tab:
        signup_form()

st.divider()

st.caption(
    "Demo version • Google authentication can be enabled using Google OAuth. "
    "Passwords should be securely hashed (bcrypt) before storing in the database."
)
