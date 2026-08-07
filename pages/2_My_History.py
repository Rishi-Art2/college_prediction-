
import pandas as pd
import streamlit as st

from database import get_user_predictions

st.set_page_config(page_title="My History", page_icon="📜", layout="wide")

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

st.title("📜 My Search History")
st.caption("Every prediction you've run is saved to the SQL database and shown here.")

records = get_user_predictions(st.session_state.user["id"])

if not records:
    st.info("You haven't made any predictions yet. Head to **Predict College** to get started.")
else:
    dfh = pd.DataFrame(records).rename(
        columns={
            "percentile": "Percentile",
            "category": "Category",
            "branch": "Branch",
            "cap_round": "CAP Round",
            "results_count": "Results Found",
            "searched_at": "Searched At",
        }
    )
    st.dataframe(
        dfh[["Percentile", "Category", "Branch", "CAP Round", "Results Found", "Searched At"]],
        use_container_width=True,
    )
    st.metric("Total Searches", len(dfh))
