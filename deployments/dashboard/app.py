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
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.warning("Logo não encontrada")

st.sidebar.header("Previsão de Risco por Escola")

# Coleta de dados da escola para previsão
media_inse = st.sidebar.slider("Média INSE", min_value=1.0, max_value=8.0, value=5.0, step=0.1)
tp_tipo_rede = st.sidebar.selectbox("Tipo de Rede", options=[2, 3], format_func=lambda x: "Estadual" if x == 2 else "Municipal")
tp_localizacao = st.sidebar.selectbox("Localização", options=[1, 2], format_func=lambda x: "Urbana" if x == 1 else "Rural")
tp_capital = st.sidebar.selectbox("Capital", options=[1, 2], format_func=lambda x: "Capital" if x == 1 else "Interior")

if st.sidebar.button("Analisar Risco de Evasão"):
    dados_escola = pd.DataFrame([{
        'MEDIA_INSE': media_inse,
        'PC_NIVEL_1': 0.0, 'PC_NIVEL_2': 0.0, 'PC_NIVEL_3': 0.0, 'PC_NIVEL_4': 0.0,
        'PC_NIVEL_5': 0.0, 'PC_NIVEL_6': 0.0, 'PC_NIVEL_7': 0.0, 'PC_NIVEL_8': 0.0,
        'TP_TIPO_REDE': tp_tipo_rede,
        'TP_LOCALIZACAO': tp_localizacao,
        'TP_CAPITAL': tp_capital
    }])
    dados_escola_final = dados_escola.reindex(columns=colunas_modelo, fill_value=0)
    predicao = modelo.predict(dados_escola_final)
    probabilidade = modelo.predict_proba(dados_escola_final)

    st.sidebar.subheader("Resultado da Análise:")
    if predicao[0] == 1:
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
total_escolas = len(df)
df['risco_evasao'] = (df['TAXA_ABANDONO_GERAL'] > 5).astype(int)
escolas_em_risco = len(df[df['risco_evasao'] == 1])
taxa_risco = (escolas_em_risco / total_escolas) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", f"{total_escolas}")
col2.metric("Escolas com Alto Risco", f"{escolas_em_risco}")
col3.metric("Taxa de Risco", f"{taxa_risco:.2f}%")

st.markdown("---")
st.markdown("### Visualizações Analíticas")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Taxa de Abandono por UF")
    risco_uf = df.groupby('SG_UF')['TAXA_ABANDONO_GERAL'].mean().reset_index()
    risco_uf.columns = ['UF', 'Taxa Média de Abandono']
    fig_uf = px.bar(
        risco_uf.sort_values('Taxa Média de Abandono', ascending=False).head(15),
        x='UF', y='Taxa Média de Abandono',
        title='Top 15 UFs por Taxa Média de Abandono',
        text='Taxa Média de Abandono'
    )
    fig_uf.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    st.plotly_chart(fig_uf, use_container_width=True)

with col_graf2:
    st.subheader("Risco por Classificação INSE")
    risco_inse = df.groupby('INSE_CLASSIFICACAO')['risco_evasao'].mean().mul(100).reset_index()
    risco_inse.columns = ['Classificação INSE', '% Escolas em Risco']
    fig_inse = px.bar(
        risco_inse,
        x='Classificação INSE', y='% Escolas em Risco',
        title='% de Escolas em Risco por Nível INSE',
        text='% Escolas em Risco'
    )
    fig_inse.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    st.plotly_chart(fig_inse, use_container_width=True)

# CORREÇÃO: Adicionar mais visualizações úteis
st.markdown("---")
st.markdown("### Distribuição por Outras Características")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    st.subheader("Risco por Tipo de Rede")
    df['Rede'] = df['TP_TIPO_REDE'].map({1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada'})
    risco_rede = df.groupby('Rede')['risco_evasao'].mean().mul(100).reset_index()
    risco_rede.columns = ['Rede', '% Escolas em Risco']
    fig_rede = px.pie(
        risco_rede, values='% Escolas em Risco', names='Rede',
        title='Distribuição do Risco por Tipo de Rede'
    )
    st.plotly_chart(fig_rede, use_container_width=True)

with col_graf4:
    st.subheader("Risco por Localização")
    df['Localização'] = df['TP_LOCALIZACAO'].map({1: 'Urbana', 2: 'Rural'})
    risco_loc = df.groupby('Localização')['risco_evasao'].mean().mul(100).reset_index()
    risco_loc.columns = ['Localização', '% Escolas em Risco']
    fig_loc = px.bar(
        risco_loc, x='Localização', y='% Escolas em Risco',
        title='Risco por Localização',
        text='% Escolas em Risco'
    )
    fig_loc.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    st.plotly_chart(fig_loc, use_container_width=True)