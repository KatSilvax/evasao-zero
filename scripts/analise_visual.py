import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

print("--- INICIANDO PASSO 3: ANÁLISE VISUAL (EDA) ---")

# --- 0. Definição de Caminhos (Paths) ---
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
file_to_load = os.path.join(BASE_DIR, 'data', 'processed', 'dados_consolidados_limpos.csv')

# Pasta para salvar os gráficos
path_output_folder = os.path.join(BASE_DIR, 'reports', 'figures')
os.makedirs(path_output_folder, exist_ok=True)
print(f"Gráficos serão salvos em: {path_output_folder}")

# --- 1. Carregar DataFrame Limpo ---
print(f"Carregando {file_to_load}...")
try:
    df = pd.read_csv(file_to_load, dtype={'ID_ESCOLA': str})
    print(f"...DataFrame carregado com sucesso ({len(df)} linhas).")
except FileNotFoundError:
    print(f"ERRO: Ficheiro '{file_to_load}' não encontrado.")
    print("Verifique se você executou o 'processar_microdados.py' (Passo 2) primeiro.")
    sys.exit()

# --- 2. Preparar Colunas Categóricas (Mapeamento) ---
# As colunas 'TP_TIPO_REDE' e 'TP_LOCALIZACAO' são números (1, 2, 3)
# Vamos mapeá-las para nomes legíveis para os gráficos.
df['REDE_ENSINO'] = df['TP_TIPO_REDE'].map({
    1: 'Federal',
    2: 'Estadual',
    3: 'Municipal'
}).fillna('Desconhecido') # Adiciona tratamento para outros valores, se houver

df['LOCALIZACAO'] = df['TP_LOCALIZACAO'].map({
    1: 'Urbana',
    2: 'Rural'
}).fillna('Desconhecido')

# --- 3. Criar Gráficos ---

# GRÁFICO 1: Distribuição da Taxa de Abandono (Nosso Alvo)
print("Gerando Gráfico 1: Distribuição da Taxa de Abandono...")
plt.figure(figsize=(10, 6))
# Filtra valores extremos (taxas acima de 30%) para melhor visualização
sns.histplot(df[df['TAXA_ABANDONO_GERAL'] <= 30]['TAXA_ABANDONO_GERAL'], bins=50, kde=True)
plt.title('Distribuição da Taxa de Abandono (Ensino Fundamental)\n(Escolas com taxa <= 30%)')
plt.xlabel('Taxa de Abandono (%)')
plt.ylabel('Contagem de Escolas')
plt.savefig(os.path.join(path_output_folder, '01_dist_abandono_ef.png'))
plt.close() # Fecha a figura para libertar memória

# GRÁFICO 2: Distribuição da Média INSE (Nosso Preditor)
print("Gerando Gráfico 2: Distribuição da Média INSE...")
plt.figure(figsize=(10, 6))
sns.histplot(df['MEDIA_INSE'], bins=40, kde=True, color='blue')
plt.title('Distribuição da Média INSE (Escolas do Ens. Fundamental)')
plt.xlabel('Média INSE')
plt.ylabel('Contagem de Escolas')
plt.savefig(os.path.join(path_output_folder, '02_dist_inse.png'))
plt.close()

# GRÁFICO 3: Correlação INSE x Abandono (A Hipótese Central)
print("Gerando Gráfico 3: Correlação INSE vs. Abandono...")
plt.figure(figsize=(10, 6))
# 'regplot' cria um scatter plot com uma linha de regressão
sns.regplot(data=df, x='MEDIA_INSE', y='TAXA_ABANDONO_GERAL',
            scatter_kws={'alpha': 0.1, 's': 5},  # Pontos semitransparentes
            line_kws={'color': 'red'})
plt.title('Correlação: Média INSE vs. Taxa de Abandono (Ens. Fundamental)')
plt.xlabel('Média INSE (Maior = Melhor Nível Socioeconómico)')
plt.ylabel('Taxa de Abandono (%)')
plt.ylim(0, 30) # Focar na maioria dos dados (abaixo de 30%)
plt.savefig(os.path.join(path_output_folder, '03_corr_inse_abandono_ef.png'))
plt.close()

# GRÁFICO 4: Abandono por Tipo de Rede (Análise Categórica)
print("Gerando Gráfico 4: Abandono por Tipo de Rede...")
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='REDE_ENSINO', y='TAXA_ABANDONO_GERAL', 
            order=['Federal', 'Estadual', 'Municipal'])
plt.title('Taxa de Abandono (Ens. Fundamental) por Rede de Ensino')
plt.xlabel('Rede de Ensino')
plt.ylabel('Taxa de Abandono (%)')
plt.ylim(0, 20) # Focar na maioria dos dados (abaixo de 20%)
plt.savefig(os.path.join(path_output_folder, '04_boxplot_rede_abandono_ef.png'))
plt.close()

print("\n--- PASSO 3 CONCLUÍDO! ---")
print(f"Gráficos salvos em {path_output_folder}")