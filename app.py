import streamlit as st
import pandas as pd

tab_data, tab_chart, tab_settings = st.tabs(["📊 Data", "📈 Charts", "⚙️ Settings"])

with tab_data:
    st.write("Data table")
    st.dataframe(pd.DataFrame({"A": [1,2,3], "B": [4,5,6]}))

with tab_chart:
    st.write("Charts go here")
    st.line_chart({"values": [10, 25, 15, 30, 22]})

with tab_settings:
    threshold = st.slider("Alert threshold", 0, 100, 50)
    st.write(f"Threshold set to {threshold}")
