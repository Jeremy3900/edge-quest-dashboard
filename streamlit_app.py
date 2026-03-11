import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Edge Quest", layout="wide")

st.sidebar.title("⚔️ Edge Quest")

uploaded_file = st.sidebar.file_uploader(
    "Upload Trade Log",
    type=["csv"]
)

if uploaded_file is None:

    st.title("⚔️ Edge Quest Trading Dashboard")
    st.write("Upload a trade log to begin.")

else:

    df = pd.read_csv(uploaded_file)

    st.title("⚔️ Edge Quest Trading Dashboard")

    st.subheader("Trade Log")
    st.dataframe(df)

    if "R" in df.columns:

        # Equity + drawdown
        df["Equity"] = df["R"].cumsum()
        df["Drawdown"] = df["Equity"] - df["Equity"].cummax()

        # Core metrics
        total_r = df["R"].sum()
        win_rate = (df["R"] > 0).mean() * 100

        avg_win = df[df["R"] > 0]["R"].mean()
        avg_loss = df[df["R"] < 0]["R"].mean()

        expectancy = (win_rate/100 * avg_win) + ((1 - win_rate/100) * avg_loss)

        col1, col2, col3 = st.columns(3)

        col1.metric("Total R", round(total_r,2))
        col2.metric("Win Rate", f"{win_rate:.1f}%")
        col3.metric("Expectancy", round(expectancy,2))

        # Equity curve
        st.subheader("Equity Curve")
        fig = px.line(df, y="Equity")
        st.plotly_chart(fig, use_container_width=True)

        # Drawdown curve
        st.subheader("Drawdown Curve")
        fig2 = px.line(df, y="Drawdown")
        st.plotly_chart(fig2, use_container_width=True)

        # Distribution
        st.subheader("R Distribution")
        fig_hist = px.histogram(df, x="R", nbins=20)
        st.plotly_chart(fig_hist, use_container_width=True)

        # Monte Carlo
        st.subheader("Monte Carlo Simulation")

        simulations = 100
        trades = len(df)

        equity_paths = []

        for i in range(simulations):
            sample = np.random.choice(df["R"], trades)
            equity_paths.append(np.cumsum(sample))

        mc_df = pd.DataFrame(equity_paths).T

        fig_mc = px.line(mc_df)
        st.plotly_chart(fig_mc, use_container_width=True)

        # Efficiency
        if "MAE" in df.columns and "MFE" in df.columns:


            st.subheader("Trade Efficiency")

            fig_eff = px.scatter(
                df,
                x="MAE",
                y="MFE",
                color="R"
            )

            st.plotly_chart(fig_eff, use_container_width=True)
# -----------------------------
# Risk Guardian
# -----------------------------

if uploaded_file is not None and "Drawdown" in df.columns:

    st.subheader("🛡 Risk Guardian")

    max_allowed_drawdown = -10

    current_drawdown = df["Drawdown"].min()

    remaining_risk = max_allowed_drawdown - current_drawdown

    col1, col2, col3 = st.columns(3)

    col1.metric("Max Allowed DD", f"{max_allowed_drawdown}R")
    col2.metric("Current DD", round(current_drawdown,2))
    col3.metric("Remaining Risk", round(remaining_risk,2))

    risk_percent = min(abs(current_drawdown / max_allowed_drawdown), 1)

    st.progress(int(risk_percent * 100))

    if risk_percent < 0.5:
        st.success("Risk Status: Safe")
    elif risk_percent < 0.8:
        st.warning("Risk Status: Elevated")
    else:
        st.error("Risk Status: Danger Zone")