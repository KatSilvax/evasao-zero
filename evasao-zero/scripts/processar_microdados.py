import pandas as pd
import numpy as np
import sys
import os

print("--- INICIANDO PASSO 2: LIMPEZA E ANÁLISE (Versão Robusta 2.0) ---")

# --- 0. Definição de Caminhos (Paths) ---
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
file_to_load = os.path.join(BASE_DIR, 'data', 'processed', 'dados_consolidados_inse_evasao.csv')
file_to_save = os.path.join(BASE_DIR, 'data', 'processed', 'dados_consolidados_limpos.csv')


# --- 1. Carregar DataFrame ---
print(f"Carregando {file_to_load}...")
try:
    df_final = pd.read_csv(file_to_load, dtype={'ID_ESCOLA': str})
    print("...DataFrame carregado com sucesso.")
except FileNotFoundError:
    print(f"ERRO: Arquivo '{file_to_load}' não encontrado.")
    print("Você executou o script 'merge_dados.py' (Passo 1) primeiro?")
    sys.exit() 

# --- 2. Limpeza das Colunas-Alvo ---
print("\n--- Iniciando Limpeza das Colunas-Alvo ---")

col_abandono_ef = 'ABANDONO_EF'
col_abandono_em = 'ABANDONO_EM'

# ----- CORREÇÃO IMPORTANTE AQUI -----
# Função de limpeza robusta para lidar com tipos mistos (strings e números)
def limpar_coluna_taxa(series):
    # 1. Força a coluna para string, tratando NaNs
    series_str = series.astype(str)
    # 2. Substitui marcadores de nulo ('--' e 'nan') por um NaN real
    series_limpa = series_str.replace('--', np.nan).replace('nan', np.nan)
    # 3. Agora que é string ou NaN, substitui a vírgula
    series_limpa = series_limpa.str.replace(',', '.', regex=False)
    # 4. Converte para numérico
    series_numerica = pd.to_numeric(series_limpa, errors='coerce')
    return series_numerica

# Aplicar a função de limpeza
if col_abandono_ef in df_final.columns:
    df_final['abandono_ef_num'] = limpar_coluna_taxa(df_final[col_abandono_ef])
    print("Coluna de abandono EF limpa.")
else:
    print(f"AVISO: Coluna '{col_abandono_ef}' não encontrada para limpeza.")
    df_final['abandono_ef_num'] = np.nan 

if col_abandono_em in df_final.columns:
    df_final['abandono_em_num'] = limpar_coluna_taxa(df_final[col_abandono_em])
    print("Coluna de abandono EM limpa.")
else:
    print(f"AVISO: Coluna '{col_abandono_em}' não encontrada para limpeza.")
    df_final['abandono_em_num'] = np.nan 


# --- 3. Engenharia de Features (Criar Alvo Unificado) ---
print("\n--- Engenharia de Feature (Alvo Unificado) ---")
df_final['TAXA_ABANDONO_GERAL'] = df_final[['abandono_ef_num', 'abandono_em_num']].mean(axis=1, skipna=True)
print("Coluna 'TAXA_ABANDONO_GERAL' criada.")

linhas_antes = len(df_final)
print(f"Total de escolas no dataset antes da limpeza: {linhas_antes}")

# Remover apenas as linhas onde o cálculo final da taxa de abandono resultou em Nulo
# (ou seja, a escola não tinha dados de abandono nem no EF nem no EM)
df_final = df_final.dropna(subset=['TAXA_ABANDONO_GERAL'])

linhas_depois = len(df_final)
print(f"Escolas sem nenhuma taxa de abandono (removidas): {linhas_antes - linhas_depois}")
print(f"DataFrame final (após remover nulos): {linhas_depois} linhas.")

df_final.to_csv(file_to_save, index=False)
print(f"DataFrame limpo salvo em '{file_to_save}'")

# --- 4. Análise Exploratória (EDA) ---
print("\n--- Análise Exploratória (EDA) ---")
# Adicionar verificação para evitar erro em dataframe vazio
if linhas_depois > 0:
    print("\n--- Descrição Estatística da Taxa de Abandono (Geral) ---")
    print(df_final['TAXA_ABANDONO_GERAL'].describe())

    print("\n--- Descrição Estatística da Média do INSE ---")
    print(df_final['MEDIA_INSE'].describe())

    print("\n--- Correlação entre Abandono e INSE ---")
    correlacao = df_final['MEDIA_INSE'].corr(df_final['TAXA_ABANDONO_GERAL'])
    print(f"Correlação de Pearson (Abandono x MEDIA_INSE): {correlacao:.4f}")
else:
    print("AVISO: O DataFrame final está vazio. Nenhuma análise estatística foi executada.")

print("\n--- PASSO 2 CONCLUÍDO! ---")