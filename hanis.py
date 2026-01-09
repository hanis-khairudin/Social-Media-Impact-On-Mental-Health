import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title("🧠 Social Media Impact on Mental Health")

@st.cache_data
def load_data():
    url = "YOUR_CSV_URL"
    return pd.read_csv(url)

df = load_data()
df.columns = df.columns.str.strip()

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

# ================= SUMMARY BOX =================
st.sidebar.markdown("### 📌 Summary")

high_percentage = (
    df[variable].astype(str).isin(['4', '5']).mean() * 100
)

st.sidebar.metric(
    "Agree / High Level (%)",
    f"{high_percentage:.1f}%"
)
