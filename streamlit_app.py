import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time

st.set_page_config(page_title="Edge Quest", layout="wide")

st.sidebar.image("20230812_202115_0000.png", width=200)
st.sidebar.title("Edge Quest")

live_mode = st.sidebar.checkbox("Live Trading Mode")

if live_mode:

    st.sidebar.write("Live trade feed enabled")

    file_path = st.sidebar.text_input(
        "Trade Log Path",
        "C:/Users/YOU/Documents/trades.csv"
    )

    try:
        df = pd.read_csv(file_path)

        st.sidebar.success("Live feed connected")

        time.sleep(5)
        st.experimental_rerun()

    except:
        st.sidebar.warning("Waiting for trade log...")

else:

    uploaded_file = st.sidebar.file_uploader(
        "Upload Trade Log",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

    # -----------------------------
    # CLEAN BROKER EXPORT
    # -----------------------------

    if "Closed PnL" in df.columns:

        df["Closed PnL"] = (
            df["Closed PnL"]
            .astype(str)
            .str.replace("$","",regex=False)
            .str.replace(",","",regex=False)
        )

        df["Closed PnL"] = pd.to_numeric(df["Closed PnL"], errors="coerce")

        df = df.dropna(subset=["Closed PnL"])

        risk_per_trade = 100

        df["R"] = df["Closed PnL"] / risk_per_trade

    if "Open" in df.columns:
        df["Date"] = pd.to_datetime(df["Open"])

    # -----------------------------
    # DISPLAY DATA
    # -----------------------------

    st.title("📊 Edge Quest Trading Dashboard")

    st.subheader("Trade Log")
    st.dataframe(df)

    if "R" in df.columns:

        # EQUITY
        df["Equity"] = df["R"].cumsum()

        # DRAWDOWN
        df["Drawdown"] = df["Equity"] - df["Equity"].cummax()

        # METRICS
        total_r = df["R"].sum()
        win_rate = (df["R"] > 0).mean() * 100

        avg_win = df[df["R"] > 0]["R"].mean()
        avg_loss = df[df["R"] < 0]["R"].mean()

        expectancy = (win_rate/100 * avg_win) + ((1 - win_rate/100) * avg_loss)

        col1, col2, col3 = st.columns(3)

        col1.metric("Total R", round(total_r,2))
        col2.metric("Win Rate", f"{win_rate:.1f}%")
        col3.metric("Expectancy", round(expectancy,2))

        # -----------------------------
        # EQUITY CURVE
        # -----------------------------

        st.subheader("Equity Curve")

        fig = px.line(df, y="Equity")
        st.plotly_chart(fig, use_container_width=True)

        # -----------------------------
        # DRAWDOWN
        # -----------------------------

        st.subheader("Drawdown Curve")

        fig2 = px.line(df, y="Drawdown")
        st.plotly_chart(fig2, use_container_width=True)

        # -----------------------------
        # R DISTRIBUTION
        # -----------------------------

        st.subheader("R Distribution")

        fig_hist = px.histogram(df, x="R", nbins=20)
        st.plotly_chart(fig_hist, use_container_width=True)

        # -----------------------------
        # MONTE CARLO
        # -----------------------------

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

        # -----------------------------
        # MAE / MFE EFFICIENCY
        # -----------------------------

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
        # RISK GUARDIAN
        # -----------------------------

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