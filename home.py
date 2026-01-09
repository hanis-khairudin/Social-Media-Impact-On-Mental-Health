import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

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
