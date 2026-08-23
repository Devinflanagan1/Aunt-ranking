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


st.markdown(
    """
    <style>
    .main { background-color: #F5F5DC; }
    h1 { color: #165B33; font-family: sans-serif; text-align: center; }
    p, label { color: #333; text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("☘️ Irish Aunt Leaderboard")
st.write(
    "Drag the ☰ handle to reorder. Use the dropdowns below to save your exact"
    " ranking globally!"
)

# Aunts list
aunts = ["Nora", "Anne", "Janet", "Cinta", "Margo", "Maureen"]

# Since cross-iframe communication in Streamlit can be finicky on mobile,
# using a clean native form ensures it saves 100% of the time on any device!
with st.form("ranking_form"):
  st.subheader("📋 Set Current Ranks")
  col1, col2 = st.columns(2)

  with col1:
    r1 = st.selectbox("Rank 1", aunts, index=0)
    r2 = st.selectbox("Rank 2", aunts, index=1)
    r3 = st.selectbox("Rank 3", aunts, index=2)
  with col2:
    r4 = st.selectbox("Rank 4", aunts, index=3)
    r5 = st.selectbox("Rank 5", aunts, index=4)
    r6 = st.selectbox("Rank 6", aunts, index=5)

  submitted = st.form_submit_button(
      "📸 Save Global Snapshot", use_container_width=True
  )

  if submitted:
    current_order = [f"#1 {r1}", f"#2 {r2}", f"#3 {r3}", f"#4 {r4}", f"#5 {r5}", f"#6 {r6}"]
    save_history_entry(current_order)
    st.success("Snapshot saved globally!")
    st.rerun()

st.markdown("---")
st.subheader("📜 Global History Log")

history_data = load_history()
if not history_data:
  st.info("No snapshots saved yet.")
else:
  for entry in history_data:
    st.markdown(
        f"""
        <div style="background: #ffffff; padding: 12px; border-radius: 8px; margin-bottom: 10px; font-size: 14px; border-left: 5px solid #165B33; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="font-weight: bold; color: #165B33; margin-bottom: 4px;">🕒 {entry['time']}</div>
            <div>{' | '.join(entry['order'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
