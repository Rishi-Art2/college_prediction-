import streamlit as st
from database import init_db, add_user, authenticate_user
from supabase import create_client, Client

# Page Configuration
st.set_page_config(
    page_title="Admit Sure",
    page_icon="Image.jpeg",
    layout="centered"
)


page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.freepik.com/premium-photo/paper-cut-abstract-background_277819-187.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
# Main page config ke paas hi add kar sakte hain
st.logo("Image.jpeg", icon_image="Image.jpeg")
# Supabase Configuration
SUPABASE_URL = "https://uchmareibvcqiajqlbl.supabase.co"
SUPABASE_KEY = "sb_publishable_vEEkVtKRnJ0zptT1CpprI9Q_7sq_gij-"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Database
init_db()

# Session State Initializations
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# ------------------ Login Form ------------------ #
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
            st.success(f"Welcome {user['username']}! 🎉")
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.markdown("---")

   
    if st.button("🌐 Login with Google", use_container_width=True):
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": "https://cutoff-prediction.streamlit.app"
            }
        })
        if response and hasattr(response, 'url'):
            st.link_button("Continue to Google", response.url, use_container_width=True)

    st.caption("Demo version • Google authentication can be enabled using Google OAuth.\nPasswords should be securely hashed (bcrypt) before storing in the database.")


# ------------------ Signup Form ------------------ #
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
    

# ------------------ MAIN APP CONTROLLER ------------------ #

if st.session_state.logged_in:

    # 1. Sidebar CSS Background Image Injection
    sidebar_bg_img = """
    <style>
    [data-testid="stSidebar"] {
        background-image: url("https://img.freepik.com/premium-photo/dark-blue-background-with-gold-accents-elegant-geometric-shapes_626475-10892.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """
    st.markdown(sidebar_bg_img, unsafe_allow_html=True)
    
    sidebar_bg_img = """
         <style>
            [data-testid="stSidebar"] {
                background-image: url("https://img.freepik.com/premium-photo/dark-blue-background-with-gold-accents-elegant-geometric-shapes_626475-10092.jpg");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            </style>
            """
    st.markdown(sidebar_bg_img, unsafe_allow_html=True)

    with st.sidebar:
        # Top Logo Display
        try:
            st.image("logo.png", width=110)
        except Exception:
            pass

        # User Info
        st.title(f"👤 {st.session_state.user['username']}")
        st.write("Navigation & Features")
        st.divider()

        # Navigation Options
        selected_page = st.radio(
            "Navigation",
            ["🎯 Predict College", "📜 My History", "📊 Admin Dashboard"],
            label_visibility="collapsed"
        )

        st.divider()

        # Logout Button (Properly inside sidebar)
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    # 3. MAIN DASHBOARD CONTENT AREA
    st.title(f"Welcome back, {st.session_state.user['username']}! 👋")
    st.caption("Here is an overview of college cutoff analytics & predictive admissions guide.")
    st.markdown("---")

    # Key Metrics Summary Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">500+</div>
                <div class="metric-label">Colleges Covered</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">98.5%</div>
                <div class="metric-label">Prediction Accuracy</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">2026</div>
                <div class="metric-label">Latest Data Model</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">Active 🟢</div>
                <div class="metric-label">System Status</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Dynamic Page View Based on Selection
    if selected_page == "🎯 Predict College":
        st.subheader("🎯 College Cutoff Predictor")
        # Yahan aapka Predict College wala form/inputs aayenge

    elif selected_page == "📜 My History":
        st.subheader("📜 Recent Search History")
        # Yahan history table ya list dikhadein

    elif selected_page == "📊 Admin Dashboard":
        st.subheader("📊 System Analytics & Controls")
        # Admin metrics
else:
    
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

  
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("🎓 Admit Sure")
        login_tab, signup_tab = st.tabs(["🔒 Login", "📝 Sign Up"])

        with login_tab:
            login_form()

        with signup_tab:
            signup_form()
