import streamlit as st

with st.form("registration"):
    st.subheader("Registration Form")

    col1, col2 = st.columns(2)
    with col1:
        name  = st.text_input("Full name")
        email = st.text_input("Email")
    with col2:
        age  = st.slider("Age", 18, 99, 25)
        role = st.selectbox("Role", ["Analyst", "Manager", "Developer"])

    accepted = st.checkbox("I accept the terms")

    # The submit button — required inside a form
    submitted = st.form_submit_button("Submit", type="primary")

# This code only runs AFTER submit is clicked
if submitted:
    if not name or not email:
        st.error("Name and email are required.")
    elif not accepted:
        st.warning("You must accept the terms.")
    else:
        st.success(f"Welcome {name} ({role})!")
        st.balloons()
