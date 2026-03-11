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