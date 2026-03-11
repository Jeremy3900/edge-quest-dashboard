import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Edge Quest Dashboard", layout="wide")

st.title("⚔️ Edge Quest Trading Dashboard")

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

    profit_factor = abs(df[df["R"] > 0]["R"].sum() / df[df["R"] < 0]["R"].sum())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total R", round(total_r,2))
    col2.metric("Win Rate", f"{win_rate:.1f}%")
    col3.metric("Expectancy", round(expectancy,2))
    col4.metric("Profit Factor", round(profit_factor,2))

    # Equity Curve
    df["Equity"] = df["R"].cumsum()

    st.subheader("Equity Curve")

    fig = px.line(df, y="Equity", title="Equity Curve")

    st.plotly_chart(fig, use_container_width=True)

    # Drawdown
    peak = df["Equity"].cummax()
    drawdown = df["Equity"] - peak

    st.subheader("Drawdown")

    fig2 = px.line(drawdown, title="Drawdown Curve")

    st.plotly_chart(fig2, use_container_width=True)

    # MAE vs MFE
    if "MAE" in df.columns and "MFE" in df.columns:

        st.subheader("MAE vs MFE")

        fig3 = px.scatter(
            df,
            x="MAE",
            y="MFE",
            color="R",
            title="Trade Efficiency (MAE vs MFE)"
        )

        st.plotly_chart(fig3, use_container_width=True)