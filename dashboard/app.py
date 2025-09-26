# O código principal da nossa aplicação web (o dashboard)

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da Página 
# Deve ser o primeiro comando do Streamlit
st.set_page_config(
    page_title="Evasão-Zero | Dashboard de evasão",
    page_icon="🎓",
    layout="wide"
)

#Carregamento dos Dados
# Função para carregar os dados (com cache para melhor performance)
@st.cache_data
def carregar_dados():
    caminho_dados = os.path.join('..', 'data', 'dados_limpos.csv')
    try:
        df = pd.read_csv(caminho_dados)
        return df
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado! Verifique o caminho.")
        return None

df = carregar_dados()

# Se o dataframe não for carregado, para a execução
if df is None:
    st.stop()


# Barra Lateral (Sidebar)
st.sidebar.image(os.path.join('..', 'assets', 'logo.jpg'), use_column_width=True)
st.sidebar.header("Filtros")
# Adicionar filtros aqui no futuro (ex: por curso, por período)


# Título Principal
st.title("Dashboard de análise de risco de evasão")
st.markdown("Instituto Federal de Mato Grosso do Sul - Campus Jardim (IFMS)")


# KPIs (Indicadores Chave)
st.markdown("### Métricas gerais")

# Calcula os KPIs
total_alunos = len(df)
alunos_em_risco = len(df[df['risco_evasao_declarado'] == 'Sim'])
taxa_risco = (alunos_em_risco / total_alunos) * 100

# Exibe os KPIs em colunas
col1, col2, col3 = st.columns(3)
col1.metric("Total de Alunos", f"{total_alunos}")
col2.metric("Alunos em Risco Declarado", f"{alunos_em_risco}")
col3.metric("Taxa de Risco", f"{taxa_risco:.2f}%")


# Gráficos -
st.markdown("---") # Linha divisória
st.markdown("### Visualizações")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    # Gráfico 1: Risco de Evasão por Curso
    st.subheader("Risco de Evasão por Curso")
    df_risco_curso = df.groupby('curso')['risco_evasao_declarado'].value_counts().unstack().fillna(0)
    df_risco_curso['Total'] = df_risco_curso.sum(axis=1)
    df_risco_curso = df_risco_curso.sort_values(by='Total', ascending=True)
    
    fig_curso = px.bar(
        df_risco_curso,
        x=['Sim', 'Não', 'Talvez'],
        y=df_risco_curso.index,
        orientation='h',
        title="Contagem de Alunos por Status de Risco em Cada Curso",
        labels={'value': 'Número de Alunos', 'curso': 'Curso'},
        color_discrete_map={'Sim': '#d62728', 'Não': '#2ca02c', 'Talvez': '#ff7f0e'}
    )
    fig_curso.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_curso, use_container_width=True)

with col_graf2:
    # Gráfico 2: Risco por Renda Familiar
    st.subheader("Risco de Evasão por Renda Familiar")
    ordem_renda = [
        'Até 1 salário mínimo (R$ 1.412)',
        'Entre 1 e 2 salários mínimos (R$ 1.413 - R$ 2.824)',
        'Entre 2 e 4 salários mínimos (R$ 2.825 - R$ 5.648)',
        'Mais de 4 salários mínimos (acima de R$ 5.648)'
    ]
    df['renda_familiar_cat'] = pd.Categorical(df['renda_familiar'], categories=ordem_renda, ordered=True)

    fig_renda = px.density_heatmap(
        df,
        x='risco_evasao_declarado',
        y='renda_familiar_cat',
        title='Relação entre Renda Familiar e Risco de Evasão',
        labels={'risco_evasao_declarado': 'Pensou em Desistir?', 'renda_familiar_cat': 'Renda Familiar'}
    )
    st.plotly_chart(fig_renda, use_container_width=True)