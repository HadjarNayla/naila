import streamlit as st

# Inject custom CSS
st.markdown("""
<style>
    /* Change the app background */
    .stApp { background-color: #fafafa; }

    /* Custom class for a red title */
    .red-title {
        color: #FF4B4B;
        font-size: 2rem;
        font-weight: 800;
    }

    /* Target Streamlit metric values */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        color: #0066cc;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="red-title">Custom Title!</h1>',
            unsafe_allow_html=True)
st.metric("Revenue", "$125,000", "+12%")
