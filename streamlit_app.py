import streamlit as st
import pandas as pd

st.set_page_config(page_title="Edge Quest Dashboard", layout="wide")

st.title("Edge Quest Trading Dashboard")

file = st.file_uploader("Upload Trade Log", type=["csv"])

if file:

    df = pd.read_csv(file)

    st.subheader("Trade Log")
    st.dataframe(df)

    total_r = df["R"].sum()
    win_rate = (df["R"] > 0).mean() * 100

    equity = df["R"].cumsum()

    col1, col2 = st.columns(2)

    col1.metric("Total R", round(total_r,2))
    col2.metric("Win Rate", f"{win_rate:.1f}%")

    st.subheader("Equity Curve")
    st.line_chart(equity)