import streamlit as st
import pandas as pd

# Sample data
df = pd.DataFrame({
    "Name":       ["Alice","Bob","Charlie","Diana","Emile"],
    "Department": ["IT","HR","IT","Finance","HR"],
    "Salary":     [4500, 3800, 5200, 4100, 3600],
    "Active":     [True, True, False, True, True]
})

st.title("Data Explorer")

# Filters in the sidebar
with st.sidebar:
    st.header("🔍 Filters")
    depts = st.multiselect(
        "Department",
        df["Department"].unique(),
        default=df["Department"].unique()
    )
    sal_min, sal_max = st.slider(
        "Salary ($)", 3000, 6000, (3000, 6000), step=100
    )
    active_only = st.checkbox("Active employees only", value=True)

# Apply filters
mask = (
    df["Department"].isin(depts) &
    df["Salary"].between(sal_min, sal_max)
)
if active_only:
    mask &= df["Active"]

df_filtered = df[mask]

st.metric("Results", len(df_filtered))
st.dataframe(df_filtered, use_container_width=True, hide_index=True)
