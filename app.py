
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configurações da Página ---
st.set_page_config(layout="wide", page_title="Dashboard de Análise de Vendas Online")

# --- Carregar e Limpar Dados (função cacheada para performance) ---
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv('/online_retail.csv')
    df['total vendas'] = df['Quantity'] * df['UnitPrice']
    df_cleaned = df.dropna(subset=['Description', 'CustomerID']).copy()
    return df_cleaned

df_cleaned = load_and_clean_data()

# --- Título e Descrição do Dashboard ---
st.title("Dashboard de Análise de Vendas Online")
st.markdown("""
Este dashboard interativo apresenta insights sobre as vendas de varejo online.
Utilize os filtros na barra lateral para explorar os dados.
""")

# --- Barra Lateral para Filtros/Controles ---
st.sidebar.header("Configurações do Dashboard")

# --- Top 10 Produtos Mais Vendidos ---
st.header("Top 10 Produtos Mais Vendidos por Quantidade")
top_10_products = df_cleaned.groupby('Description')['Quantity'].sum().nlargest(10).reset_index()

fig_products = px.bar(
    top_10_products,
    x='Quantity',
    y='Description',
    orientation='h', # Gráfico de barras horizontal
    title='Top 10 Produtos por Quantidade Vendida',
    labels={'Quantity': 'Quantidade Vendida', 'Description': 'Produto'},
    color='Quantity',
    color_continuous_scale=px.colors.sequential.Viridis
)
fig_products.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False) # Ordena as barras
st.plotly_chart(fig_products, use_container_width=True)

# --- Vendas Totais por País ---
st.header("Vendas Totais por País")

num_countries = st.sidebar.slider(
    "Número de países a exibir",
    min_value=5,
    max_value=min(20, len(df_cleaned['Country'].unique())),
    value=10
)

sales_by_country = df_cleaned.groupby('Country')['total vendas'].sum().sort_values(ascending=False).reset_index()
top_countries_sales = sales_by_country.head(num_countries)

fig_country = px.bar(
    top_countries_sales,
    x='total vendas',
    y='Country',
    orientation='h',
    title=f'Top {num_countries} Países por Vendas Totais',
    labels={'total vendas': 'Vendas Totais', 'Country': 'País'},
    color='total vendas',
    color_continuous_scale=px.colors.sequential.Magma
)
fig_country.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
st.plotly_chart(fig_country, use_container_width=True)

st.write("--- ")
st.markdown("Desenvolvido para análise de vendas online.")
