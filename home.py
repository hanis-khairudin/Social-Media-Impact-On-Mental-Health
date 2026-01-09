import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

def safe_corr(df, col_x, col_y):
    if col_x not in df.columns or col_y not in df.columns:
        return None
    temp = df[[col_x, col_y]].dropna()
    if len(temp) < 3:
        return None
    return temp.corr().iloc[0, 1]


# --- MAIN TITLE ---
st.title(" Student Mental Health Monitoring Insights Dashboard")
st.markdown("Exploring the Relationship Between Internet Use and Mental Health.")

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Internet Use and Mental Health Dashboard",
    page_icon="🧠",
    layout="wide"
)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQnrGG72xRS-qLoiM2zon4eP8t5XMiO5MhoLUEe2jJer0G5EzodiU4e0NOmx_ssmCwZf-AnbQXhBbTM/pub?gid=1791189796&single=true&output=csv"
    return pd.read_csv(url)

df = load_data()

# Clean Column Names
df.columns = df.columns.str.strip()

# Rename Columns
df = df.rename(columns={
    "Age / Umur:": "Age",
    "Gender / Jantina:": "Gender",
    "Race / Bangsa:": "Race",
    "Year of Study / Tahun Belajar:": "Year_of_Study",
    "Programme of Study / Program Pembelajaran (cth., SST):": "Programme_of_Study",
    "Current living situation / Keadaan hidup sekarang:": "Current_Living_Situation",
    "Employment Status / Status Pekerjaan:": "Employment_Status",
    "Relationship Status / Status Perhubungan:": "Relationship_Status",
    "How would you describe your general academic performance? / Bagaimanakah anda menerangkan prestasi akademik umum anda?": "General_Academic_Performance",
    "How many hours do you study per week (outside class)? / Berapa jam anda belajar setiap minggu (di luar kelas)?": "Hours_Study_per_Week",
    "How often do you use social media? / Berapa kerap anda menggunakan media sosial?": "Social_Media_Use_Frequency",
    "Platforms you use most often (select all) / Platform yang paling kerap anda gunakan (pilih semua):": "Platforms_Most_Often_Used",
    "I have been feeling stressed or overwhelmed with assignments. / Saya telah berasa tertekan atau terbeban dengan tugasan.": "Assignments_Stress",
    "I often feel anxious about my academic workload. / Saya sering berasa bimbang tentang beban kerja akademik saya.": "Academic_Workload_Anxiety",
    "I have difficulty sleeping due to university-related pressure. / Saya sukar tidur kerana tekanan berkaitan universiti.": "Difficulty_Sleeping_University_Pressure",
    "I feel supported by friends or family when I am stressed. / Saya berasa disokong oleh rakan atau keluarga apabila saya tertekan.": "Friends_Family_Support",
    "I can manage my emotions well during stressful periods. / Saya boleh menguruskan emosi saya dengan baik semasa tempoh tekanan.": "Manage_Emotion_Stressful_Periods",
    "I use social media to relax or escape from academic stress. / Saya menggunakan media sosial untuk berehat atau melarikan diri daripada tekanan akademik.": "Social_Media_Relaxation",
    "I feel emotionally connected to my social media accounts. / Saya berasa tersambung secara emosi dengan akaun media sosial saya.": "Emotional_Connection_Social_Media",
    "Using social media is an important part of my daily routine. / Menggunakan media sosial adalah bahagian penting dalam rutin harian saya.": "Social_Media_Daily_Routine",
    "I sometimes lose track of time when using social media. / Saya kadang-kadang terlepas masa apabila menggunakan media sosial.": "Social_Media_Waste_Time",
    "Social media has affected my sleep (sleeping late or difficulty sleeping). / Media sosial telah menjejaskan tidur saya (tidur lewat atau sukar tidur).": "Sleep_Affected_By_Social_Media",
    "Social media affects my ability to concentrate on studies. / Media sosial menjejaskan keupayaan saya untuk menumpukan perhatian kepada pelajaran.": "Studies_Affected_By_Social_Media",
    "I use the Internet to look for mental health information (e.g., coping tips, stress-relief content). / Saya menggunakan Internet untuk mencari maklumat kesihatan mental (cth., petua mengatasi tekanan, kandungan melegakan tekanan).": "Mental_Health_Info_Through_Internet",
    "I have come across upsetting or disturbing content online. / Saya telah menemui kandungan yang menjengkelkan atau mengganggu dalam talian.": "Across_Upsetting_Content_Online",
    "When I feel stressed, I prefer to seek help online rather than talk to someone in person. / Apabila saya berasa tertekan, saya lebih suka mencari bantuan dalam talian daripada bercakap dengan seseorang secara peribadi.": "Seek_Help_Online_When_Stress",
    "I know where to find reliable mental health information online. / Saya tahu di mana untuk mencari maklumat kesihatan mental yang boleh dipercayai dalam talian.": "Find_Mental_Health_Info_Online",
    "I follow accounts that post motivational or mental health content. / Saya mengikuti akaun yang menyiarkan kandungan motivasi atau kesihatan mental.": "Follow_Motivational_Mental_Health_Content",
    "I use online communities for academic or emotional support. / Saya menggunakan komuniti dalam talian untuk sokongan akademik atau emosi.": "Use_Online_Communities_for_Support",
    "Social media has a generally positive impact on my wellbeing. / Media sosial secara amnya mempunyai kesan positif terhadap kesejahteraan saya.": "Social_Media_Positive_Impact_on_Wellbeing",
    "Social media has a generally negative impact on my wellbeing. / Media sosial secara amnya mempunyai kesan negatif terhadap kesejahteraan saya.": "Social_Media_Negative_Impact_on_Wellbeing",
    "Do you think universities should provide more online mental health resources? / Adakah anda fikir universiti harus menyediakan lebih banyak sumber kesihatan mental dalam talian?": "Do you think universities should provide more online mental health resources?",
    "What type of online content affects you the most (positive or negative)? / Apakah jenis kandungan dalam talian yang paling mempengaruhi anda (positif atau negatif)?": "Type_of_Online_Content_Affects",
    "What do you think universities can do to support student wellbeing? / Pada pendapat anda, apakah yang boleh dilakukan oleh universiti untuk menyokong kesejahteraan pelajar?": "Universities_Support_Actions"
})

# ================= OVERALL (UNFILTERED) DISTRIBUTION =================
st.header("Overall Social Media Usage (All Respondents)")

# ------ DATASET OVERVIEW ------
st.subheader("📋 Dataset Overview")

st.markdown("""
This section provides an **overall overview of the survey dataset** collected from UMK students.
It allows users to understand the **structure, size, and completeness** of the data before any
filtering or visualization is applied.
""")

# --- SUMMARY BOX ---
col1, col2, col3, col4 = st.columns(4)

top_academic = df['General_Academic_Performance'].mode()[0]
top_media = df['Social_Media_Use_Frequency'].mode()[0]

if not df.empty:
    col1.metric("Total Records", f"{len(df):,}", help="PLO 1: Total Respondent Records of Student", border=True)
    col2.metric("Avg. Age", f"{df['Age'].mean():.1f} years", help="PLO 2: Students Age", border=True)
    col3.metric("Academic Performance", top_academic, help="PLO 3: Students Academic Performance", border=True)
    col4.metric("Social Media Usage", top_media, help="PLO 4: Social Media Use Frecuency", border=True)
else:
    col1.metric("Total Records", "0", help="No data available")
    col2.metric("Avg. Age", "N/A", help="No data available")
    col3.metric("Academic Performance", "N/A", help="No data available")
    col4.metric("Social Media Usage", "N/A", help="No data available")

# --- Dataset Preview ---
with st.expander("View Dataset Preview"):
    st.dataframe(df.head(20), use_container_width=True)

st.markdown("---")

# ================= TAB 3: HANIS NABILA =================
with tab3:
    st.header("📊 Social Media Impact on Mental Health (Hanis Nabila)")

    # ====================================================
    # SUMMARY BOX
    # ====================================================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "High Usage (>5 hrs/day)",
        f"{(hanis_df['Social_Media_Use_Frequency'].isin(['5 to 6 hours per day','More than 6 hours per day']).mean()*100):.1f}%"
    )

    col2.metric(
        "Often/Always Assignment Stress",
        f"{(hanis_df['Assignments_Stress'].astype(str).isin(['4','5']).mean()*100):.1f}%"
    )

    col3.metric(
        "Sleep Frequently Affected",
        f"{(hanis_df['Sleep_Affected_By_Social_Media'].astype(str).isin(['4','5']).mean()*100):.1f}%"
    )

    col4.metric(
        "Agree Negative Impact",
        f"{(hanis_df['Social_Media_Negative_Impact_on_Wellbeing'].astype(str).isin(['4','5']).mean()*100):.1f}%"
    )

    st.markdown("---")

    # ====================================================
    # SUB-TABS FOR VISUALIZATION
    # ====================================================
    tab1, tab2, tab3_viz, tab4 = st.tabs([
        "📈 Assignment Stress",
        "😴 Sleep Disruption",
        "⚖️ Positive vs Negative Impact",
        "📦 Wellbeing Score by Usage"
    ])

    # ====================================================
    # TAB 3.1 – ASSIGNMENT STRESS
    # ====================================================
    with tab1:
        st.subheader("Assignment Stress Distribution")

        fig = px.histogram(
            hanis_df,
            x="Assignments_Stress",
            title="Distribution of Assignment Stress Levels"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.success("""
        **Interpretation:**  
        The distribution shows that many students experience assignment-related stress
        at moderate to high levels, indicating that academic workload is a common
        source of pressure among students.
        """)

        st.markdown("#### Social Media Usage vs Assignment Stress")

        st.write("Unique values in Assignments Stress:")
        st.write(hanis_df['Assignments_Stress'].unique())

        assignments_stress_mapping = {
            '1': 'Never', '2': 'Rarely', '3': 'Sometimes', '4': 'Often', '5': 'Always'
        }

        hanis_df['Assignments_Stress_Categorical'] = (
            hanis_df['Assignments_Stress'].astype(str).map(assignments_stress_mapping)
        )

        contingency_table = pd.crosstab(
            hanis_df['Social_Media_Use_Frequency'],
            hanis_df['Assignments_Stress_Categorical']
        )

        social_media_order = [
            'Less than 1 hour per day',
            '1 to 2 hours per day',
            '3 to 4 hours per day',
            '5 to 6 hours per day',
            'More than 6 hours per day'
        ]
        contingency_table = contingency_table.reindex(social_media_order, fill_value=0)

        assignments_stress_order = ['Never','Rarely','Sometimes','Often','Always']
        contingency_table = contingency_table[
            [c for c in assignments_stress_order if c in contingency_table.columns]
        ]

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(contingency_table, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
        ax.set_title("Social Media Use Frequency vs Assignment Stress")
        ax.set_xlabel("Assignment Stress Level")
        ax.set_ylabel("Social Media Use Frequency")
        st.pyplot(fig)

        st.success("""
        **Interpretation:**  
        Students with higher social media usage tend to report higher assignment stress,
        suggesting that excessive social media use may contribute to academic pressure.
        """)

    # ====================================================
    # TAB 3.2 – SLEEP DISRUPTION
    # ====================================================
    with tab2:
        st.subheader("Social Media Usage vs Sleep Disruption")

        sleep_mapping = {
            '1': 'Never', '2': 'Rarely', '3': 'Sometimes', '4': 'Often', '5': 'Always'
        }

        hanis_df['Sleep_Affected_Categorical'] = (
            hanis_df['Sleep_Affected_By_Social_Media'].astype(str).map(sleep_mapping)
        )

        contingency_sleep = pd.crosstab(
            hanis_df['Social_Media_Use_Frequency'],
            hanis_df['Sleep_Affected_Categorical']
        ).reindex(social_media_order, fill_value=0)

        sleep_order = ['Never','Rarely','Sometimes','Often','Always']
        contingency_sleep = contingency_sleep[
            [c for c in sleep_order if c in contingency_sleep.columns]
        ]

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(contingency_sleep, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
        ax.set_title("Social Media Use Frequency vs Sleep Disruption")
        ax.set_xlabel("Sleep Affected Level")
        ax.set_ylabel("Social Media Use Frequency")
        st.pyplot(fig)

        st.success("""
        **Interpretation:**  
        Increased social media usage is associated with more frequent sleep disruption,
        indicating that prolonged online engagement may negatively affect sleep quality.
        """)

    # ====================================================
    # TAB 3.3 – POSITIVE VS NEGATIVE IMPACT
    # ====================================================
    with tab3_viz:
        st.subheader("Perceived Positive vs Negative Impact on Wellbeing")

        impact_mapping = {
            '1': 'Strongly Disagree', '2': 'Disagree',
            '3': 'Neutral', '4': 'Agree', '5': 'Strongly Agree'
        }

        hanis_df['Positive_Impact_Cat'] = (
            hanis_df['Social_Media_Positive_Impact_on_Wellbeing'].astype(str).map(impact_mapping)
        )
        hanis_df['Negative_Impact_Cat'] = (
            hanis_df['Social_Media_Negative_Impact_on_Wellbeing'].astype(str).map(impact_mapping)
        )

        response_order = list(impact_mapping.values())

        plot_df = pd.DataFrame({
            'Positive Impact': hanis_df['Positive_Impact_Cat'].value_counts().reindex(response_order, fill_value=0),
            'Negative Impact': hanis_df['Negative_Impact_Cat'].value_counts().reindex(response_order, fill_value=0)
        }).T

        fig, ax = plt.subplots(figsize=(10, 7))
        plot_df.plot(kind='bar', stacked=True, ax=ax, colormap='viridis')
        ax.set_title("Positive vs Negative Impact of Social Media on Wellbeing")
        ax.set_xlabel("Impact Type")
        ax.set_ylabel("Number of Respondents")
        ax.set_xticklabels(plot_df.index, rotation=0)
        st.pyplot(fig)

        st.success("""
        **Interpretation:**  
        Students perceive both positive and negative impacts of social media on wellbeing,
        indicating that social media plays a dual role in students’ mental health.
        """)

    # ====================================================
    # TAB 3.4 – WELLBEING SCORE BY USAGE
    # ====================================================
    with tab4:
        st.subheader("Wellbeing Impact Score by Social Media Usage")

        impact_num = {'1':1,'2':2,'3':3,'4':4,'5':5}

        hanis_df['Positive_Num'] = hanis_df['Social_Media_Positive_Impact_on_Wellbeing'].astype(str).map(impact_num)
        hanis_df['Negative_Num'] = hanis_df['Social_Media_Negative_Impact_on_Wellbeing'].astype(str).map(impact_num)

        df_melted = hanis_df.melt(
            id_vars=['Social_Media_Use_Frequency'],
            value_vars=['Positive_Num','Negative_Num'],
            var_name='Impact_Type',
            value_name='Wellbeing_Score'
        )

        fig, ax = plt.subplots(figsize=(14, 8))
        sns.boxplot(
            data=df_melted,
            x='Social_Media_Use_Frequency',
            y='Wellbeing_Score',
            hue='Impact_Type',
            ax=ax
        )
        ax.set_title("Wellbeing Impact Score by Social Media Usage")
        ax.set_xlabel("Social Media Use Frequency")
        ax.set_ylabel("Wellbeing Impact Score")
        ax.tick_params(axis='x', rotation=30)
        st.pyplot(fig)

        st.success("""
        **Interpretation:**  
        Higher social media usage shows greater variability in negative wellbeing scores,
        suggesting that excessive usage may increase the risk of negative mental health
        outcomes among students.
        """)
