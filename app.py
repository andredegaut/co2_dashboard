import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIG
st.set_page_config(page_title="CO2 Dashboard", layout="wide")

# LOAD DATA
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    df = pd.read_csv(url)

    df = df[['country', 'year', 'co2', 'co2_per_capita']]
    df = df.dropna()

    return df

df = load_data()

# SIDEBAR
st.sidebar.title("Filtros")

countries = st.sidebar.multiselect(
    "Selecione países",
    options=df['country'].unique(),
    default=["Brazil", "United States", "China"]
)

year_range = st.sidebar.slider(
    "Intervalo de anos",
    int(df['year'].min()),
    int(df['year'].max()),
    (2000, 2020)
)

# FILTER
df_filtered = df[
    (df['country'].isin(countries)) &
    (df['year'].between(year_range[0], year_range[1]))
]

# TITLE
st.title("🌍 Dashboard de Emissões Globais de CO₂")
st.markdown("Análise global de emissões de CO₂ com dados reais")

# LINE CHART
fig_line = px.line(
    df_filtered,
    x='year',
    y='co2',
    color='country',
    title='Evolução das emissões de CO₂'
)

st.plotly_chart(fig_line, use_container_width=True)

# BAR CHART
df_latest = df_filtered[df_filtered['year'] == year_range[1]]

fig_bar = px.bar(
    df_latest,
    x='country',
    y='co2',
    color='country',
    title=f'Emissões no ano {year_range[1]}'
)

st.plotly_chart(fig_bar, use_container_width=True)

# KPI
st.subheader("📊 Indicadores")

col1, col2, col3 = st.columns(3)

total_co2 = int(df_latest['co2'].sum())
top_country = df_latest.sort_values(by='co2', ascending=False).iloc[0]['country']
avg_per_capita = round(df_latest['co2_per_capita'].mean(), 2)

col1.metric("Total CO₂", total_co2)
col2.metric("Maior emissor", top_country)
col3.metric("Média per capita", avg_per_capita)

# INSIGHT
st.markdown("## 🔍 Insights")
st.markdown("""
- Países industrializados dominam emissões absolutas  
- Emissões per capita mostram outra perspectiva  
- Crescimento acelerado em países emergentes  
""")

# FOOTER
st.markdown("---")
st.markdown("Projeto de portfólio em Data Analytics")
