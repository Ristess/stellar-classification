import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cosmic Object Finder",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌌 3D Cosmic Object Finder")

@st.cache_data
def load_data():
    return pd.read_csv('DEEPP_Final_Sampled_Dataset.csv')

df = load_data()

st.sidebar.header("Filter by Characteristics")


redshift_range = st.sidebar.slider(
    'Select Redshift Range',
    min_value=float(df['redshift'].min()),
    max_value=float(df['redshift'].max()),
    value=(0.0, 1.0)
)


selected_classes = st.sidebar.multiselect(
    'Select Object Type',
    options=df['predicted_class'].unique(),
    default=df['predicted_class'].unique()
)

filtered_df = df[
    (df['redshift'] >= redshift_range[0]) &
    (df['redshift'] <= redshift_range[1]) &
    (df['predicted_class'].isin(selected_classes))
]

color_map = {
    'GALAXY': '#e0e0e0',  
    'QSO': '#ffa500',     
    'STAR': '#ff1493'     
}

fig = px.scatter_3d(
    filtered_df,
    x='alpha',
    y='delta',
    z='redshift',
    color='predicted_class',
    color_discrete_map=color_map, 
    size='redshift',
    hover_name='obj_ID',
    title="Interactive 3D Celestial Map"
)

fig.update_layout(
    scene={
        'bgcolor': 'rgb(0, 0, 0)',  
        # 'xaxis': {'visible': False, 'showgrid': False},
        # 'yaxis': {'visible': False, 'showgrid': False},
        # 'zaxis': {'visible': False, 'showgrid': False},
    },
    title_font_size=28,
    font=dict(color='white')
)

fig.update_traces(
    marker=dict(
        line=dict(width=0),
        symbol='circle',
        opacity=0.8
    )
)

st.plotly_chart(fig, use_container_width=True)