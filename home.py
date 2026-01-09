import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from data_loader import load_data

# ================= PAGE CONFIG (MUST BE FIRST) =================
st.set_page_config(
    page_title="Internet Use and Mental Health Dashboard",
    page_icon="🧠",
    layout="wide"
)

st.set_page_config(page_title="Students Mental Health Analysis", layout="wide")

# Define Pages
home = st.Page("home.py", title="Home", icon=":material/home:")

internetUsage = st.Page("Nur_Aishah_Sakinah.py", title="Internet Use vs. Mental Health", icon=":material/insights:")
ilya = st.Page("Ilya.py", title="Advanced Visualizations", icon=":material/show_chart:")
hanis = st.Page("Hanis_Nabila.py", title="Correlation Insights", icon=":material/share:")
ainun = st.Page("Ainun.py", title="Riding Behavior Insights", icon=":material/pedal_bike:")

# Sidebar Navigation
pg = st.navigation({
    "Menu": [home],
    "Motor Accident Severity Analysis": [
        internetUsage,
        ilya,
        hanis,
        ainun
    ]
})

# Run navigation
pg.run()

# ================= HELPER FUNCTION =================
def safe_corr(df, col_x, col_y):
    if col_x not in df.columns or col_y not in df.columns:
        return None
    temp = df[[col_x, col_y]].dropna()
    if len(temp) < 3:
        return None
    return temp.corr().iloc[0, 1]

# ================= TITLE =================
st.title("🧠 Student Mental Health Monitoring Insights Dashboard")
st.markdown("Exploring the Relationship Between Internet Use and Mental Health.")

# ================= LOAD DATA =================
df = load_data()

st.title("🧠 Student Mental Health Dashboard")
st.markdown("Overview of Internet Use and Mental Health Dataset")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", len(df))
col2.metric("Average Age", f"{df['Age'].mean():.1f}")
col3.metric("Top Academic Performance", df['General_Academic_Performance'].mode()[0])
col4.metric("Top Social Media Usage", df['Social_Media_Use_Frequency'].mode()[0])

st.markdown("### 🔍 Dataset Preview")
st.dataframe(df.head(20), use_container_width=True)
