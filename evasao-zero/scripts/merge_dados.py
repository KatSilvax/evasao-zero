import pandas as pd
import numpy as np
import sys
import os

print("--- INICIANDO PASSO 1: MERGE DOS DADOS (Versão .xlsx + encoding) ---")

# --- 0. Definição de Caminhos (Paths) ---
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')

path_inse = os.path.join(BASE_DIR, 'data', 'raw', 'INSE_2021_escolas.xlsx')
path_rend = os.path.join(BASE_DIR, 'data', 'raw', 'tx_rend_escolas_2021.csv')

path_output_folder = os.path.join(BASE_DIR, 'data', 'processed')
path_output_file = os.path.join(path_output_folder, 'dados_consolidados_inse_evasao.csv')

os.makedirs(path_output_folder, exist_ok=True)

# --- 1. Carregar Features (INSE) ---
print(f"Carregando INSE de: {path_inse}")
try:
    df_inse = pd.read_excel(path_inse, sheet_name='INSE_ESC_2021', engine='openpyxl')
    df_inse['ID_ESCOLA'] = df_inse['ID_ESCOLA'].astype(str)
    print("... INSE (.xlsx) carregado com sucesso.")
except FileNotFoundError:
    print(f"ERRO: Arquivo INSE não encontrado em {path_inse}")
    sys.exit()
except Exception as e:
    print(f"ERRO ao ler o arquivo Excel: {e}")
    sys.exit()

# --- 2. Carregar Target (Rendimento) ---
print(f"Carregando Rendimento de: {path_rend}")
try:
    df_rend = pd.read_csv(
        path_rend, 
        sep=';', 
        skiprows=5,
        header=[0, 1, 2],
        encoding='latin1'
    )
    
    # Achatar o cabeçalho
    df_rend.columns = [' - '.join(col).strip() for col in df_rend.columns.values]
    
    # Renomear a coluna chave
    chave_col_nome = [col for col in df_rend.columns if 'CÓDIGO DA ESCOLA' in col.upper()][0]
    df_rend.rename(columns={chave_col_nome: 'ID_ESCOLA'}, inplace=True)

    df_rend['ID_ESCOLA'] = df_rend['ID_ESCOLA'].astype(str)
    print("... Rendimento carregado e cabeçalho processado (com encoding latin1).")

except FileNotFoundError:
    print(f"ERRO: Arquivo de Rendimento não encontrado em {path_rend}")
    sys.exit()
except Exception as e:
    print(f"ERRO ao processar o cabeçalho do arquivo de rendimento: {e}")
    sys.exit()

# --- 3. Executar o Merge ---
print("\n--- Executando o MERGE dos datasets ---")

# ----- CORREÇÃO IMPORTANTE AQUI -----
# Usar os nomes de coluna corretos que vêm do cabeçalho de 3 níveis
colunas_para_merge = [
    'ID_ESCOLA',
    'Taxa de Abandono - Ensino Fundamental de 8 e 9 anos - Total', # Nome EF Correto
    'Taxa de Abandono -  Ensino Médio - Total  '  # Nome EM Correto (com espaços)
]

# Verificar se as colunas existem antes de tentar selecionar
colunas_reais = []
for col in colunas_para_merge:
    if col in df_rend.columns:
        colunas_reais.append(col)
    else:
        print(f"AVISO no Merge: Coluna '{col}' não encontrada no arquivo de rendimento.")

df_rend_selecionado = df_rend[colunas_reais]

df_final = pd.merge(
    df_inse,
    df_rend_selecionado,
    on='ID_ESCOLA',
    how='inner'
)

print(f"Merge concluído! {len(df_final)} escolas encontradas em ambos os datasets.")
print(f"Colunas no arquivo de merge: {df_final.columns.tolist()}") # Debug

# --- 4. Salvar o Resultado ---
df_final.to_csv(path_output_file, index=False)
print(f"\n[SUCESSO] Arquivo de merge salvo em: {path_output_file}")
print("--- PASSO 1 CONCLUÍDO ---")