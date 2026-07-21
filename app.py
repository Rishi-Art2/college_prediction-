
# import streamlit as st
# from database import init_db, add_user, authenticate_user

# st.set_page_config(
#     page_title="Admit Sure",
#     page_icon="🎓",
#     layout="centered",
# )


# init_db()

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "user" not in st.session_state:
#     st.session_state.user = None


# def login_form():
#     st.subheader("Login to your account")
#     username = st.text_input("Username", key="login_username")
#     password = st.text_input("Password", type="password", key="login_password")

#     if st.button("Login", use_container_width=True, type="primary"):
#         if not username or not password:
#             st.warning("Please fill in both fields.")
#         else:
#             user = authenticate_user(username, password)
#             if user:
#                 st.session_state.logged_in = True
#                 st.session_state.user = user
#                 st.success(f"Welcome back, {user['username']}! Redirecting...")
#                 st.rerun()
#             else:
#                 st.error("Invalid username or password.")


# def signup_form():
#     st.subheader("Create a new account")
#     username = st.text_input("Choose a username", key="signup_username")
#     email = st.text_input("Email address", key="signup_email")
#     password = st.text_input("Choose a password", type="password", key="signup_password")
#     confirm = st.text_input("Confirm password", type="password", key="signup_confirm")

#     if st.button("Sign Up", use_container_width=True, type="primary"):
#         if not (username and email and password and confirm):
#             st.warning("Please fill in every field.")
#         elif password != confirm:
#             st.error("Passwords do not match.")
#         elif len(password) < 4:
#             st.error("Password should be at least 4 characters long.")
#         else:
#             success, message = add_user(username, email, password)
#             if success:
#                 st.success(message + " You can now log in from the Login tab.")
#             else:
#                 st.error(message)


# st.title("🎓 Admit Sure")
# st.caption("Predict which colleges & branches you're eligible for, based on your entrance exam percentile.")

# if st.session_state.logged_in:
#     st.success(f"You are logged in as **{st.session_state.user['username']}**")
#     st.info("👈 Use the sidebar to open **Predict College** or **My History**.")
#     if st.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.user = None
#         st.rerun()
# else:
#     tab_login, tab_signup = st.tabs(["🔐 Login", "🆕 Sign Up"])
#     with tab_login:
#         login_form()
#     with tab_signup:
#         signup_form()

# st.divider()
# st.caption(
#     "Sample data notice: the cutoff numbers shipped with this project are "
#     "randomly generated for demo purposes. Replace `data/cutoff_data.csv` "
#     "with real cutoff data for accurate predictions."
# )
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

SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

if st.button("🔵 Continue with Google"):
    response = supabase.auth.sign_in_with_oauth(
        {
            "provider": "google",
            "options": {
                "redirect_to": "http://localhost:8501"
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