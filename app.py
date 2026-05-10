import streamlit as st

# Button — returns True only when clicked
if st.button("Click me!", type="primary"):
    st.balloons()
    st.success("Button clicked! 🎉")

# Checkbox — returns True or False
is_active = st.checkbox("Enable advanced option")
if is_active:
    st.info("Option is ON")

# Slider — returns the selected number
age = st.slider("Age", min_value=0, max_value=100, value=25, step=1)
st.write(f"Your age: {age} years old")

# Range slider (picks two values)
price_range = st.slider("Price range ($)", 0, 1000, (100, 500))
st.write(f"From ${price_range[0]} to ${price_range[1]}")

# Radio buttons
color = st.radio("Favourite color", ["Red", "Green", "Blue"], horizontal=True)

# Toggle switch
dark_mode = st.toggle("Dark mode")
