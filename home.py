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

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Analysis Settings")

variable = st.sidebar.selectbox(
    "Select Mental Health Variable",
    [
        "Assignments_Stress",
        "Sleep_Affected_By_Social_Media",
        "Social_Media_Positive_Impact_on_Wellbeing",
        "Social_Media_Negative_Impact_on_Wellbeing"
    ]
)
