import streamlit as st

st.set_page_config(
    page_title="Students Mental Health Analysis",
    layout="wide"
)

# Pages
home = st.Page("home.py", title="Home", icon=":material/home:")
internetUsage = st.Page("Nur_Aishah_Sakinah.py", title="Internet Use vs. Mental Health", icon=":material/insights:")
ilya = st.Page("Ilya.py", title="Advanced Visualizations", icon=":material/show_chart:")
hanis = st.Page("hanis.py", title="Impact of Social Media on Mental Health", icon=":material/share:")
ainun = st.Page("Ainun.py", title="Riding Behavior Insights", icon=":material/pedal_bike:")

# Navigation Sidebar (automatically rendered by Streamlit)
pg = st.navigation({
    "Menu": [home],
    "Mental Health Analysis": [
        internetUsage,
        ilya,
        hanis,
        ainun
    ]
})

pg.run()
