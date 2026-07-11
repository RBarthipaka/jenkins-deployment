import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Dummy Dashboard", layout="wide")

st.title("📊 Dummy Deployment Test App")
st.caption(f"Server time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown("""
This is a placeholder app used to test the **Docker + Jenkins multibranch pipeline**
deployment flow. Replace this with your real application code.
""")

# --- Sidebar controls ---
st.sidebar.header("Controls")
rows = st.sidebar.slider("Number of rows", 5, 100, 20)
seed = st.sidebar.number_input("Random seed", value=42)

# --- Dummy data ---
np.random.seed(seed)
df = pd.DataFrame({
    "id": range(1, rows + 1),
    "category": np.random.choice(["A", "B", "C"], rows),
    "value": np.random.randint(10, 500, rows),
    "score": np.round(np.random.uniform(0, 1, rows), 2),
})

col1, col2, col3 = st.columns(3)
col1.metric("Total Rows", len(df))
col2.metric("Avg Value", round(df["value"].mean(), 2))
col3.metric("Avg Score", round(df["score"].mean(), 2))

st.subheader("Data Table")
st.dataframe(df, use_container_width=True)

st.subheader("Value by Category")
st.bar_chart(df.groupby("category")["value"].sum())

st.success("If you can see this page, your container is running correctly ✅")
