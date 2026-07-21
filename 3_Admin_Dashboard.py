
import pandas as pd
import streamlit as st

from database import get_all_users, get_all_predictions

st.set_page_config(page_title="Admin Dashboard", page_icon="🛠️", layout="wide")

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