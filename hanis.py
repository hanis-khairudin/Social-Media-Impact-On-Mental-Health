import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from data_loader import load_data

st.title("🧠 Social Media Impact on Mental Health")

df = load_data()

# ================= SUMMARY BOX =================
st.sidebar.markdown("### 📌 Summary")

high_percentage = (
    df[variable].astype(str).isin(['4', '5']).mean() * 100
)

st.sidebar.metric(
    "Agree / High Level (%)",
    f"{high_percentage:.1f}%"
)

tabs = st.tabs([
    "📈 Assignment Stress",
    "😴 Sleep Disruption",
    "⚖️ Positive vs Negative Impact",
    "📦 Wellbeing Score"
])

with tabs[0]:
    st.subheader("Assignment Stress Distribution")

    fig = px.histogram(
        df,
        x="Assignments_Stress",
        title="Distribution of Assignment Stress Levels"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Most students report moderate to high levels of assignment stress, "
        "suggesting academic workload is a major mental health concern."
    )

with tabs[1]:
    st.subheader("Social Media Usage vs Sleep Disruption")

    stress_map = {'1':'Never','2':'Rarely','3':'Sometimes','4':'Often','5':'Always'}
    df['Sleep_Cat'] = df['Sleep_Affected_By_Social_Media'].astype(str).map(stress_map)

    sleep_table = pd.crosstab(
        df['Social_Media_Use_Frequency'],
        df['Sleep_Cat']
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(sleep_table, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title("Social Media Usage vs Sleep Disruption")
    st.pyplot(fig)

    st.info(
        "Higher social media usage is associated with more frequent sleep disruption."
    )

with tabs[2]:
    st.subheader("Perceived Impact on Wellbeing")

    impact_map = {
        '1':'Strongly Disagree','2':'Disagree','3':'Neutral',
        '4':'Agree','5':'Strongly Agree'
    }

    pos = df['Social_Media_Positive_Impact_on_Wellbeing'].astype(str).map(impact_map).value_counts()
    neg = df['Social_Media_Negative_Impact_on_Wellbeing'].astype(str).map(impact_map).value_counts()

    impact_df = pd.DataFrame({
        "Positive Impact": pos,
        "Negative Impact": neg
    }).fillna(0)

    st.bar_chart(impact_df)

    st.info(
        "Students perceive social media as having both positive and negative effects, "
        "highlighting its dual impact on wellbeing."
    )

with tabs[3]:
    st.subheader("Wellbeing Score by Social Media Usage")

    num_map = {'1':1,'2':2,'3':3,'4':4,'5':5}
    df['Positive_Num'] = df['Social_Media_Positive_Impact_on_Wellbeing'].astype(str).map(num_map)
    df['Negative_Num'] = df['Social_Media_Negative_Impact_on_Wellbeing'].astype(str).map(num_map)

    melted = df.melt(
        id_vars='Social_Media_Use_Frequency',
        value_vars=['Positive_Num','Negative_Num'],
        var_name='Impact_Type',
        value_name='Score'
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=melted,
        x='Social_Media_Use_Frequency',
        y='Score',
        hue='Impact_Type',
        ax=ax
    )
    ax.tick_params(axis='x', rotation=30)
    st.pyplot(fig)

    st.info(
        "Higher social media usage shows greater variability in negative wellbeing scores."
    )
