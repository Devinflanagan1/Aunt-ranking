import streamlit as st

st.title("🏆 Aunt Ranking Board")
st.write("Use the select boxes below to rank each aunt from 1 to 5:")

# Define our aunts
aunts = ["Nora", "Anne", "Janet & Cinta (Tie)", "Margo", "Maureen"]

# Create ranking slots
rank_1 = st.selectbox("Rank #1", aunts, index=0)
rank_2 = st.selectbox("Rank #2", aunts, index=1)
rank_3 = st.selectbox("Rank #3", aunts, index=2)
rank_4 = st.selectbox("Rank #4", aunts, index=3)
rank_5 = st.selectbox("Rank #5", aunts, index=4)

st.markdown("---")
st.subheader("📋 Your Final Ranking Result:")

# Display the final order clearly
final_list = [rank_1, rank_2, rank_3, rank_4, rank_5]
for i, aunt in enumerate(final_list, 1):
  st.write(f"**#{i}:** {aunt}")
