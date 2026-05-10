import streamlit as st

# 3 equal columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Sales", "$12,450", "+8%")
with col2:
    st.metric("Customers", "342", "+15")
with col3:
    st.metric("Satisfaction", "4.8/5", "+0.1")

# Columns with custom proportions (2:1 ratio)
left, right = st.columns([2, 1])
with left:
    st.write("Main content (wider)")
with right:
    st.write("Side panel (narrower)")
