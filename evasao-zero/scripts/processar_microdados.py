import pandas as pd
import numpy as np
import sys
import os

print("--- INICIANDO PASSO 2: LIMPEZA E ANÁLISE ---")

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

# ----- CORREÇÃO IMPORTANTE AQUI -----
# Usar os nomes de coluna corretos que vêm do arquivo de merge
col_abandono_ef = 'Taxa de Abandono - Ensino Fundamental de 8 e 9 anos - Total'
col_abandono_em = 'Taxa de Abandono -  Ensino Médio - Total  '

# Função para limpar os dados de taxa
def limpar_coluna_taxa(series):
    series_limpa = series.replace('--', np.nan)
    series_limpa = series_limpa.str.replace(',', '.', regex=False)
    series_numerica = pd.to_numeric(series_limpa, errors='coerce')
    return series_numerica

# Aplicar a função de limpeza
# Verificar se as colunas existem antes de tentar limpá-las
if col_abandono_ef in df_final.columns:
    df_final['abandono_ef_num'] = limpar_coluna_taxa(df_final[col_abandono_ef])
    print("Coluna de abandono EF limpa.")
else:
    print(f"AVISO: Coluna '{col_abandono_ef}' não encontrada para limpeza.")
    df_final['abandono_ef_num'] = np.nan # Criar coluna vazia se não existir

if col_abandono_em in df_final.columns:
    df_final['abandono_em_num'] = limpar_coluna_taxa(df_final[col_abandono_em])
    print("Coluna de abandono EM limpa.")
else:
    print(f"AVISO: Coluna '{col_abandono_em}' não encontrada para limpeza.")
    df_final['abandono_em_num'] = np.nan # Criar coluna vazia se não existir


# --- 3. Engenharia de Features (Criar Alvo Unificado) ---
print("\n--- Engenharia de Feature (Alvo Unificado) ---")
df_final['TAXA_ABANDONO_GERAL'] = df_final[['abandono_ef_num', 'abandono_em_num']].mean(axis=1, skipna=True)
print("Coluna 'TAXA_ABANDONO_GERAL' criada.")

linhas_antes = len(df_final)
print(f"Total de escolas no dataset antes da limpeza: {linhas_antes}")
print(f"Escolas sem nenhuma taxa de abandono (NaN): {df_final['TAXA_ABANDONO_GERAL'].isna().sum()}")

df_final = df_final.dropna(subset=['TAXA_ABANDONO_GERAL'])
linhas_depois = len(df_final)
print(f"DataFrame final (após remover nulos): {linhas_depois} linhas.")

df_final.to_csv(file_to_save, index=False)
print(f"DataFrame limpo salvo em '{file_to_save}'")

# --- 4. Análise Exploratória (EDA) ---
print("\n--- Análise Exploratória (EDA) ---")
print("\n--- Descrição Estatística da Taxa de Abandono (Geral) ---")
print(df_final['TAXA_ABANDONO_GERAL'].describe())

print("\n--- Descrição Estatística da Média do INSE ---")
print(df_final['MEDIA_INSE'].describe())

print("\n--- Correlação entre Abandono e INSE ---")
correlacao = df_final['MEDIA_INSE'].corr(df_final['TAXA_ABANDONO_GERAL'])
print(f"Correlação de Pearson (Abandono x MEDIA_INSE): {correlacao:.4f}")
print("\n--- PASSO 2 CONCLUÍDO! ---")