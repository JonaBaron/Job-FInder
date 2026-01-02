import streamlit as st

st.title("Job bank App")
st.write("This app helps you find job listings.")

# 100 elements, 4 per row = 25 rows
total_items = 100
items_per_row = 4

for row in range(0, total_items, items_per_row):
    cols = st.columns(4)
    
    for i, col in enumerate(cols):
        item_num = row + i + 1
        if item_num <= total_items:
            with col:
                with st.container(border=True):
                    if st.button(f"Box {item_num}", key=f"btn_{item_num}"):
                        st.write(f"You clicked Box {item_num}")
                    elif st.button(f"Link {item_num}", key=f"link_{item_num}"):
                        st.write(f"You clicked Link {item_num}")