
import pandas as pd
import streamlit as st

from database import get_all_users, get_all_predictions

st.set_page_config(page_title="Admin Dashboard", page_icon="🛠️", layout="wide")


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

if not st.session_state.get("logged_in"):
    st.warning("Please log in first from the main page (sidebar → app).")
    st.stop()


st.title("🛠️ Admin Dashboard")
st.caption("Everything below is read live from the SQLite database (cutoff_predictor.db).")

st.subheader("👤 Registered Users")
users = get_all_users()
if users:
    st.dataframe(pd.DataFrame(users), use_container_width=True)
    st.metric("Total Registered Users", len(users))
else:
    st.info("No users found yet.")

st.divider()

st.subheader("🔎 All Prediction Searches")
preds = get_all_predictions()
if preds:
    dfp = pd.DataFrame(preds).rename(
        columns={
            "username": "Username",
            "percentile": "Percentile",
            "category": "Category",
            "branch": "Branch",
            "cap_round": "CAP Round",
            "results_count": "Results Found",
            "searched_at": "Searched At",
        }
    )
    st.dataframe(
        dfp[["Username", "Percentile", "Category", "Branch", "CAP Round", "Results Found", "Searched At"]],
        use_container_width=True,
    )
    st.metric("Total Searches (all users)", len(preds))
else:
    st.info("No predictions have been made yet.")
