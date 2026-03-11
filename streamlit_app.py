# edge-quest-dashboard
import streamlit as st

st.set_page_config(page_title="Edge Quest Dashboard")

st.title("Edge Quest Trading Dashboard")

st.write("Welcome to the Edge Quest performance system.")

st.subheader("Performance Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total R", "0.0")
col2.metric("Win Rate", "0%")
col3.metric("Expectancy", "0.0R")

st.subheader("Equity Curve")

st.line_chart([0])
