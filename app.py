import streamlit as st

st.title("Main Title (H1)")
st.header("Header (H2)")
st.subheader("Subheader (H3)")

st.text("Plain text, no formatting.")
st.markdown("**Bold**, *italic*, `inline code`, [link](https://streamlit.io)")

# st.write is universal — pass it almost anything!
st.write("Simple string")
st.write({"key": "value", "number": 42})  # dict → shown as JSON
st.write(3.14)                              # number → displayed

# Code block with syntax highlighting
st.code("for i in range(10):\n    print(i)", language="python")

# Math formula (LaTeX)
st.latex(r"E = mc^2")

# Horizontal separator
st.divider()
st.caption("Small grey text — great for notes and footnotes.")
