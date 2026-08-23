import streamlit as st
from streamlit_sortables import sort_items

st.title("🏆 Aunt Ranking Board")
st.write("Drag and drop your aunts to rank them:")

# Initial ranking setup (Janet and Cinta tied)
aunts_ranking = [
    {
        "header": "Current Rankings",
        "items": ["Nora", "Anne", ["Janet", "Cinta"], "Margo", "Maureen"],
    }
]

# Render the interactive drag-and-drop component
sorted_aunts = sort_items(aunts_ranking, direction="vertical")

# Display the final dynamic order
st.markdown("---")
st.subheader("Live Order Results:")
if sorted_aunts and len(sorted_aunts[0]["items"]) > 0:
    for index, aunt in enumerate(sorted_aunts[0]["items"], start=1):
        if isinstance(aunt, list):
            st.write(f"**#{index} (Tie):** {', '.join(aunt)}")
        else:
            st.write(f"**#{index}:** {aunt}")

