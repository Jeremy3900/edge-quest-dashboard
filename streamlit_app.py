import streamlit as st
import pandas as pd

st.set_page_config(page_title="Edge Quest Dashboard", layout="wide")

st.title("Edge Quest Trading Dashboard")

st.write("Upload a trade log to analyze your performance.")

uploaded_file = st.file_uploader("Upload Trade Log CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Trade Log")
    st.dataframe(df)

    total_r = df["R"].sum()
    win_rate = (df["R"] > 0).mean() * 100

    avg_win = df[df["R"] > 0]["R"].mean()
    avg_loss = df[df["R"] < 0]["R"].mean()

    expectancy = (win_rate/100 * avg_win) + ((1 - win_rate/100) * avg_loss)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total R", round(total_r,2))
    col2.metric("Win Rate", f"{win_rate:.1f}%")
    col3.metric("Expectancy", round(expectancy,2))

    st.subheader("Equity Curve")

    equity = df["R"].cumsum()

    st.line_chart(equity)