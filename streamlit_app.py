import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Edge Quest Dashboard", layout="wide")

st.title("⚔️ Edge Quest Trading Dashboard")

st.write("Upload a trade log to analyze your performance.")

uploaded_file = st.file_uploader("Upload Trade Log CSV", type=["csv"], key="trade_upload")

if uploaded_file:

    df = pd.read_csv(uploaded_file)
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

    # Core metrics
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

    # Equity curve
    df["Equity"] = df["R"].cumsum()

    st.subheader("Equity Curve")

    fig = px.line(df, y="Equity", title="Equity Curve")
    st.plotly_chart(fig, use_container_width=True)

    # Drawdown
    peak = df["Equity"].cummax()
    df["Drawdown"] = df["Equity"] - peak

    st.subheader("Drawdown")

    fig2 = px.line(df, y="Drawdown", title="Drawdown Curve")
    st.plotly_chart(fig2, use_container_width=True)

    # MAE vs MFE
    if "MAE" in df.columns and "MFE" in df.columns:

        st.subheader("MAE vs MFE")

        fig3 = px.scatter(
            df,
            x="MAE",
            y="MFE",
            color="R",
            title="Trade Efficiency"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # -----------------------------
    # EDGE QUEST TILT METER
    # -----------------------------

    st.subheader("🧠 Tilt Meter")

    current_drawdown = abs(df["Drawdown"].min())

    loss_streak = 0
    max_loss_streak = 0

    for r in df["R"]:
        if r < 0:
            loss_streak += 1
            max_loss_streak = max(max_loss_streak, loss_streak)
        else:
            loss_streak = 0

    oversized_trades = (df["R"] < -2).sum()

    tilt_score = (
        current_drawdown * 10 +
        max_loss_streak * 10 +
        oversized_trades * 15
    )

    tilt_score = min(tilt_score, 100)

    st.progress(int(tilt_score))

    if tilt_score < 30:
        st.success("State: Calm")
    elif tilt_score < 60:
        st.warning("State: Elevated")
    else:
        st.error("State: High Tilt Risk")

    st.write("Tilt Score:", round(tilt_score,1))
# -----------------------------
# SETUP PERFORMANCE ANALYTICS
# -----------------------------

if "Setup" in df.columns:

    st.subheader("📊 Setup Performance")

    setup_stats = df.groupby("Setup")["R"].agg(
        Trades="count",
        Total_R="sum",
        Avg_R="mean"
    ).reset_index()

    st.dataframe(setup_stats)

    import plotly.express as px

    fig_setup = px.bar(
        setup_stats,
        x="Setup",
        y="Total_R",
        title="Total R by Setup"
    )

    st.plotly_chart(fig_setup, use_container_width=True)
# -----------------------------
# EDGE QUEST RISK GUARDIAN
# -----------------------------

st.subheader("🛡 Risk Guardian")

max_allowed_drawdown = -10  # change this to your rule

current_drawdown = df["Drawdown"].min()

remaining_risk = max_allowed_drawdown - current_drawdown

col1, col2, col3 = st.columns(3)

col1.metric("Max Allowed DD", f"{max_allowed_drawdown}R")
col2.metric("Current DD", f"{round(current_drawdown,2)}R")
col3.metric("Remaining Risk", f"{round(remaining_risk,2)}R")

risk_percent = min(abs(current_drawdown / max_allowed_drawdown), 1)

st.progress(int(risk_percent * 100))

if risk_percent < 0.5:
    st.success("Risk Status: Safe")
elif risk_percent < 0.8:
    st.warning("Risk Status: Elevated")
else:
    st.error("Risk Status: Danger Zone")
# -----------------------------
# R DISTRIBUTION
# -----------------------------

st.subheader("📊 R Distribution")

fig_hist = px.histogram(
    df,
    x="R",
    nbins=20,
    title="Distribution of R per Trade"
)

st.plotly_chart(fig_hist, use_container_width=True)
# -----------------------------
# DRAWDOWN DURATION
# -----------------------------

st.subheader("📉 Drawdown Duration")

drawdown_periods = (df["Drawdown"] < 0).astype(int)

duration = []
count = 0

for d in drawdown_periods:
    if d == 1:
        count += 1
    else:
        if count > 0:
            duration.append(count)
            count = 0

if duration:
    st.write("Longest Drawdown (Trades):", max(duration))
    st.write("Average Drawdown Length:", round(sum(duration)/len(duration),2))
# -----------------------------
# ADVANCED TILT DETECTION
# -----------------------------

st.subheader("🧠 Advanced Tilt Detection")

loss_streak = 0
max_streak = 0

for r in df["R"]:
    if r < 0:
        loss_streak += 1
        max_streak = max(max_streak, loss_streak)
    else:
        loss_streak = 0

oversized_trades = (df["R"] < -2).sum()

tilt_score = (
    abs(current_drawdown) * 8 +
    max_streak * 10 +
    oversized_trades * 15
)

tilt_score = min(tilt_score, 100)

st.progress(int(tilt_score))

st.write("Loss Streak:", max_streak)
st.write("Oversized Trades:", oversized_trades)
st.write("Tilt Score:", round(tilt_score,1))

if tilt_score < 30:
    st.success("Psychological State: Calm")
elif tilt_score < 60:
    st.warning("Psychological State: Elevated")
else:
    st.error("Psychological State: High Risk")
# -----------------------------
# EXPECTANCY OVER TIME
# -----------------------------

st.subheader("📈 Expectancy Curve")

rolling_window = 20

df["Rolling Expectancy"] = df["R"].rolling(rolling_window).mean()

fig_expectancy = px.line(
    df,
    y="Rolling Expectancy",
    title="Rolling Expectancy (20 Trades)"
)

st.plotly_chart(fig_expectancy, use_container_width=True)
# -----------------------------
# MONTE CARLO SIMULATION
# -----------------------------

st.subheader("🎲 Monte Carlo Risk Simulation")

import numpy as np

simulations = 100
trades = len(df)

equity_paths = []

for i in range(simulations):

    sample = np.random.choice(df["R"], trades)

    equity = np.cumsum(sample)

    equity_paths.append(equity)

mc_df = pd.DataFrame(equity_paths).T

fig_mc = px.line(
    mc_df,
    title="Monte Carlo Equity Simulations"
)

st.plotly_chart(fig_mc, use_container_width=True)
# -----------------------------
# DISCIPLINE SCORE
# -----------------------------

st.subheader("🧠 Discipline Score")

rule_breaks = (df["R"] < -3).sum()

discipline_score = 100 - (
    rule_breaks * 10 +
    abs(df["Drawdown"].min()) * 2
)

discipline_score = max(discipline_score, 0)

st.metric("Discipline Score", round(discipline_score,1))
# -----------------------------
# WEEKLY REVIEW
# -----------------------------

st.subheader("📅 Weekly Review")

if "Date" in df.columns:

    df["Date"] = pd.to_datetime(df["Date"])

    df["Week"] = df["Date"].dt.isocalendar().week

    weekly = df.groupby("Week")["R"].sum().reset_index()

    fig_week = px.bar(
        weekly,
        x="Week",
        y="R",
        title="Weekly Performance"
    )

    st.plotly_chart(fig_week, use_container_width=True)
# -----------------------------
# EDGE EFFICIENCY ENGINE
# -----------------------------

if "MFE" in df.columns and "MAE" in df.columns:

    st.subheader("⚙️ Edge Efficiency Engine")

    avg_mfe = df["MFE"].mean()
    avg_mae = df["MAE"].mean()
    avg_r = df["R"].mean()

    capture_ratio = avg_r / avg_mfe if avg_mfe != 0 else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg MFE", round(avg_mfe,2))
    col2.metric("Avg MAE", round(avg_mae,2))
    col3.metric("Capture Ratio", round(capture_ratio,2))

    st.write("Capture Ratio shows how much of the available move you capture.")

    fig_eff = px.scatter(
        df,
        x="MAE",
        y="MFE",
        color="R",
        title="Trade Efficiency Map"
    )

    st.plotly_chart(fig_eff, use_container_width=True)