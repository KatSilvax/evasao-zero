import streamlit as st
import pandas as pd
import plotly.express as px
import os
import joblib

# --- Configuração da Página ---
st.set_page_config(
    page_title="Predikt IFMS | Dashboard de Evasão",
    page_icon="🎓",
    layout="wide"
)

# --- Carregamento dos Dados e Modelos ---

@st.cache_data
def carregar_dados():
    # Caminhos corretos quando executado de dentro da pasta dashboard
    caminhos_tentativos = [
        '../../data/dados_limpos.csv',  # Subir 2 níveis
        'data/dados_limpos.csv',
        os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'dados_limpos.csv')
    ]
    
    for caminho in caminhos_tentativos:
        if os.path.exists(caminho):
            df = pd.read_csv(caminho)
            return df
    
    st.error("Arquivo 'dados_limpos.csv' não encontrado! Procurei em:")
    for caminho in caminhos_tentativos:
        st.write(f"- {caminho} ({'existe' if os.path.exists(caminho) else 'não existe'})")
    return None

@st.cache_resource
def carregar_modelo():
    # Caminhos corretos quando executado de dentro da pasta dashboard
    caminhos_modelo = [
        'modelo_evasao.joblib',  # Mesmo diretório
        '../../models/modelo_evasao.joblib',  # Pasta models
        os.path.join(os.path.dirname(__file__), 'modelo_evasao.joblib')  # Absoluto
    ]
    
    caminhos_colunas = [
        'colunas_modelo.joblib',
        '../../models/colunas_modelo.joblib',
        os.path.join(os.path.dirname(__file__), 'colunas_modelo.joblib')
    ]
    
    modelo = None
    colunas_modelo = None
    
    for caminho_m in caminhos_modelo:
        if os.path.exists(caminho_m):
            modelo = joblib.load(caminho_m)
            break
    
    for caminho_c in caminhos_colunas:
        if os.path.exists(caminho_c):
            colunas_modelo = joblib.load(caminho_c)
            break
    
    if modelo is None or colunas_modelo is None:
        st.error("Arquivos de modelo não encontrados!")
        st.write("Procurou em:")
        for caminho in caminhos_modelo + caminhos_colunas:
            st.write(f"- {caminho} ({'existe' if os.path.exists(caminho) else 'não existe'})")
    
    return modelo, colunas_modelo

df = carregar_dados()
modelo, colunas_modelo = carregar_modelo()

# --- Validação de Carga ---
if df is None or modelo is None:
    st.warning("""
    A aplicação não pode ser totalmente carregada. Verifique:
    1. O arquivo `dados_limpos.csv` está na pasta `data/`
    2. Os arquivos `modelo_evasao.joblib` e `colunas_modelo.joblib` estão na pasta `dashboard/`
    3. A estrutura de pastas está correta
    """)
    st.stop()

# --- Barra Lateral (Sidebar) ---
# CORREÇÃO: Verificar se a logo existe antes de carregar
logo_paths = ['../assets/logo.jpg', './assets/logo.jpg', 'assets/logo.jpg']
logo_path = None
for path in logo_paths:
    if os.path.exists(path):
        logo_path = path
        break

if logo_path:
    st.sidebar.image(logo_path, use_column_width=True)
else:
    st.sidebar.warning("Logo não encontrada")

st.sidebar.header("Previsão de Risco Individual")

# Coleta de dados do aluno para previsão
curso_selecionado = st.sidebar.selectbox("Curso do Aluno", options=df['curso'].unique())
periodo_selecionado = st.sidebar.slider("Período do Aluno", min_value=1, max_value=10, value=1)
idade_selecionada = st.sidebar.number_input("Idade do Aluno", min_value=15, max_value=70, value=18)
genero_selecionado = st.sidebar.selectbox("Gênero", options=df['genero'].unique())
raca_selecionada = st.sidebar.selectbox("Cor/Raça", options=df['cor_raca'].unique())
renda_selecionada = st.sidebar.selectbox("Renda Familiar", options=df['renda_familiar'].unique())
trabalha_selecionado = st.sidebar.selectbox("Trabalha Atualmente?", options=df['trabalha'].unique())

if st.sidebar.button("Analisar Risco de Evasão"):
    # Criar um DataFrame com os dados do aluno
    dados_aluno = pd.DataFrame({
        'curso': [curso_selecionado],
        'periodo': [periodo_selecionado],
        'idade': [idade_selecionada],
        'genero': [genero_selecionado],
        'cor_raca': [raca_selecionada],
        'renda_familiar': [renda_selecionada],
        'trabalha': [trabalha_selecionado]
    })

    # Aplicar One-Hot Encoding
    dados_aluno_encoded = pd.get_dummies(dados_aluno)
    # Reindexar para garantir que as colunas sejam as mesmas do modelo
    dados_aluno_final = dados_aluno_encoded.reindex(columns=colunas_modelo, fill_value=0)

    # Fazer a predição
    predicao = modelo.predict(dados_aluno_final)
    probabilidade = modelo.predict_proba(dados_aluno_final)

    st.sidebar.subheader("Resultado da Análise:")
    if predicao[0] == 'Sim':
        st.sidebar.error("ALTO RISCO DE EVASÃO")
        st.sidebar.metric("Probabilidade de Risco", f"{probabilidade[0][1]*100:.2f}%")
    else:
        st.sidebar.success("BAIXO RISCO DE EVASÃO")
        st.sidebar.metric("Probabilidade de Permanência", f"{probabilidade[0][0]*100:.2f}%")

# --- Layout Principal do Dashboard ---
st.title("Dashboard de Análise de Risco de Evasão")
st.markdown("Instituto Federal de Mato Grosso do Sul (IFMS)")

# KPIs
st.markdown("### Métricas Gerais da Amostra")
total_alunos = len(df)
alunos_em_risco = len(df[df['risco_evasao_declarado'] == 'Sim'])
taxa_risco = (alunos_em_risco / total_alunos) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total de Alunos", f"{total_alunos}")
col2.metric("Alunos com Risco Declarado", f"{alunos_em_risco}")
col3.metric("Taxa de Risco Declarado", f"{taxa_risco:.2f}%")

st.markdown("---")
st.markdown("### Visualizações Analíticas")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    # CORREÇÃO: Gráfico 1 - Risco por Curso
    st.subheader("Risco de Evasão por Curso")
    
    # Calcular percentuais corretamente
    risco_por_curso = df.groupby('curso')['risco_evasao_declarado'].value_counts(normalize=True).mul(100).reset_index(name='percentual')
    risco_por_curso_sim = risco_por_curso[risco_por_curso['risco_evasao_declarado'] == 'Sim']
    
    fig_curso = px.bar(
        risco_por_curso_sim,
        x='curso',
        y='percentual',
        title="Percentual de Alunos com Risco Declarado por Curso",
        labels={'percentual': '% de Alunos em Risco', 'curso': 'Curso'},
        text='percentual'
    )
    fig_curso.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    st.plotly_chart(fig_curso, use_container_width=True)

with col_graf2:
    # CORREÇÃO: Gráfico 2 - Risco por Renda
    st.subheader("Risco de Evasão por Renda Familiar")
    
    df_renda = df.groupby('renda_familiar')['risco_evasao_declarado'].value_counts(normalize=True).mul(100).reset_index(name='percentual')
    df_renda_sim = df_renda[df_renda['risco_evasao_declarado'] == 'Sim']
    
    # Definir ordem correta das categorias de renda
    ordem_renda = [
        'Até 1 salário mínimo (R$ 1.412)',
        'Entre 1 e 2 salários mínimos (R$ 1.413 - R$ 2.824)',
        'Entre 2 e 4 salários mínimos (R$ 2.825 - R$ 5.648)',
        'Mais de 4 salários mínimos (acima de R$ 5.648)'
    ]
    
    # Manter apenas as categorias que existem nos dados
    ordem_renda = [renda for renda in ordem_renda if renda in df_renda_sim['renda_familiar'].values]
    
    fig_renda = px.bar(
        df_renda_sim,
        x='renda_familiar',
        y='percentual',
        title='Percentual de Risco por Faixa de Renda',
        labels={'percentual': '% de Alunos em Risco', 'renda_familiar': 'Renda Familiar'},
        category_orders={"renda_familiar": ordem_renda}
    )
    fig_renda.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    st.plotly_chart(fig_renda, use_container_width=True)

# CORREÇÃO: Adicionar mais visualizações úteis
st.markdown("---")
st.markdown("### Distribuição por Outras Características")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    st.subheader("Risco por Gênero")
    risco_genero = df.groupby('genero')['risco_evasao_declarado'].value_counts(normalize=True).mul(100).reset_index(name='percentual')
    risco_genero_sim = risco_genero[risco_genero['risco_evasao_declarado'] == 'Sim']
    
    fig_genero = px.pie(
        risco_genero_sim,
        values='percentual',
        names='genero',
        title='Distribuição do Risco por Gênero'
    )
    st.plotly_chart(fig_genero, use_container_width=True)

with col_graf4:
    st.subheader("Risco por Situação de Trabalho")
    risco_trabalho = df.groupby('trabalha')['risco_evasao_declarado'].value_counts(normalize=True).mul(100).reset_index(name='percentual')
    risco_trabalho_sim = risco_trabalho[risco_trabalho['risco_evasao_declarado'] == 'Sim']
    
    fig_trabalho = px.bar(
        risco_trabalho_sim,
        x='trabalha',
        y='percentual',
        title='Risco por Situação de Trabalho',
        labels={'percentual': '% em Risco', 'trabalha': 'Trabalha?'}
    )
    fig_trabalho.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    st.plotly_chart(fig_trabalho, use_container_width=True)