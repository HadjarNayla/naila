import streamlit as st

# ⚠️ MUST be the very first Streamlit command!
st.set_page_config(
    page_title="My Application",
    page_icon="📊",        # emoji or path to an image
    layout="wide",          # "centered" (default) or "wide"
    initial_sidebar_state="expanded"  # "auto", "expanded", "collapsed"
)

st.title("Page configured!")
st.write("Layout: full width")
