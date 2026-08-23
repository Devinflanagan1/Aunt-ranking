import json
import os
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Irish Aunt Leaderboard", layout="centered")

HISTORY_FILE = "ranking_history.json"


def load_history():
  if os.path.exists(HISTORY_FILE):
    try:
      with open(HISTORY_FILE, "r") as f:
        return json.load(f)
    except:
      return []
  return []


def save_history_entry(order_list):
  history = load_history()
  now = datetime.now().strftime("%B %d, %Y at %I:%M %p")
  history.insert(0, {"time": now, "order": order_list})
  with open(HISTORY_FILE, "w") as f:
    json.dump(history, f)


# Irish Theme Styling
st.markdown(
    """
    <style>
    .stApp { background-color: #F5F5DC; }
    h1 { color: #165B33; font-family: sans-serif; text-align: center; }
    p, label { color: #1a1a1a; font-weight: 500; }
    .stButton>button {
        background-color: #165B33;
        color: #FFFDD0;
        border: 2px solid #D4AF37;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #0b301a;
        color: #ffffff;
    }
    .history-box {
        background: #ffffff;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 12px;
        font-size: 15px;
        border-left: 5px solid #165B33;
        border-top: 1px solid #ddd;
        border-right: 1px solid #ddd;
        border-bottom: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .history-time { font-weight: bold; color: #165B33; margin-bottom: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("☘️ Irish Aunt Leaderboard")
st.write(
    "Set your ranking positions below. You can assign the same rank number to"
    " multiple aunts to create ties!"
)

aunts = ["Nora", "Anne", "Janet", "Cinta", "Margo", "Maureen"]

# Use an interactive form styled with Irish layout for absolute cross-device reliability
with st.form("ranking_form"):
  st.subheader("🏆 Configure Ranks")

  # Allow selecting positions/ties explicitly
  col1, col2 = st.columns(2)
  with col1:
    r1 = st.multiselect("Rank #1", aunts, default=["Nora"])
    r2 = st.multiselect("Rank #2", aunts, default=["Anne"])
    r3 = st.multiselect("Rank #3", aunts, default=["Janet", "Cinta"])
  with col2:
    r4 = st.multiselect("Rank #4", aunts, default=[])
    r5 = st.multiselect("Rank #5", aunts, default=["Margo"])
    r6 = st.multiselect("Rank #6", aunts, default=["Maureen"])

  submitted = st.form_submit_button("📸 Save Global Snapshot")

  if submitted:
    # Compile the layout into a clean structured list
    formatted_order = []
    for rank_num, group in enumerate(
        [r1, r2, r3, r4, r5, r6], start=1
    ):
      if group:
        formatted_order.append(f"#{rank_num}: " + ", ".join(group))

    if formatted_order:
      save_history_entry(formatted_order)
      st.success("Snapshot saved globally across all devices!")
      st.rerun()
    else:
      st.warning("Please assign at least one aunt to a rank.")

st.markdown("---")
st.subheader("📜 Global History Log")

history_data = load_history()
if not history_data:
  st.info("No snapshots saved yet.")
else:
  for entry in history_data:
    st.markdown(
        f"""
        <div class="history-box">
            <div class="history-time">🕒 {entry['time']}</div>
            <div>{' | '.join(entry['order'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
