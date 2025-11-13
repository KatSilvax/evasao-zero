import pandas as pd
import numpy as np
import sys
import os

print("--- INICIANDO PASSO 1: MERGE (Versão Robusta 2.0) ---")

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
except Exception as e:
    print(f"ERRO ao ler o arquivo Excel INSE: {e}")
    sys.exit()

# --- 2. Carregar Target (Rendimento) e Encontrar Colunas ---
print(f"Carregando Rendimento de: {path_rend}")

# Função auxiliar para procurar colunas
def find_column(column_list, keywords):
    """Procura uma coluna que contenha TODAS as palavras-chave."""
    for col in column_list:
        # Normaliza a coluna para remover espaços extras e caracteres invisíveis
        col_normalizada = ' '.join(str(col).split()).upper()
        if all(keyword.upper() in col_normalizada for keyword in keywords):
            return col
    return None

col_ef_real = None
col_em_real = None

try:
    df_rend = pd.read_csv(
        path_rend, sep=';', skiprows=5, header=[0, 1, 2], encoding='latin1'
    )
    
    # Achatar o cabeçalho
    df_rend.columns = [' - '.join(col).strip() for col in df_rend.columns.values]
    
    # Renomear a coluna chave
    chave_col_nome = find_column(df_rend.columns, ["CÓDIGO DA ESCOLA"])
    if not chave_col_nome:
        print("ERRO CRÍTICO: Não foi possível encontrar a coluna 'CÓDIGO DA ESCOLA'.")
        sys.exit()
    
    df_rend.rename(columns={chave_col_nome: 'ID_ESCOLA'}, inplace=True)
    df_rend['ID_ESCOLA'] = df_rend['ID_ESCOLA'].astype(str)

    # ----- CORREÇÃO IMPORTANTE AQUI -----
    # Procurar por "MÉDIO" em vez de "ENSINO MÉDIO"
    col_ef_real = find_column(df_rend.columns, ["TAXA DE ABANDONO", "FUNDAMENTAL", "TOTAL"])
    col_em_real = find_column(df_rend.columns, ["TAXA DE ABANDONO", "MÉDIO", "TOTAL"]) # <--- MUDANÇA AQUI

    if col_ef_real:
        print(f"... Coluna EF encontrada: '{col_ef_real}'")
    else:
        print("... AVISO: Coluna de Abandono do Ensino Fundamental não encontrada.")

    if col_em_real:
        print(f"... Coluna EM encontrada: '{col_em_real}'")
    else:
        print("... AVISO: Coluna de Abandono do Ensino Médio não encontrada.")

    print("... Rendimento carregado e colunas localizadas.")

except Exception as e:
    print(f"ERRO ao processar o arquivo de rendimento: {e}")
    sys.exit()

# --- 3. Executar o Merge ---
print("\n--- Executando o MERGE dos datasets ---")

# Renomear para nomes simples antes do merge
colunas_para_renomear = {}
colunas_para_merge = ['ID_ESCOLA']

if col_ef_real:
    colunas_para_renomear[col_ef_real] = 'ABANDONO_EF'
    colunas_para_merge.append('ABANDONO_EF')
if col_em_real:
    colunas_para_renomear[col_em_real] = 'ABANDONO_EM'
    colunas_para_merge.append('ABANDONO_EM')

df_rend.rename(columns=colunas_para_renomear, inplace=True)
df_rend_selecionado = df_rend[colunas_para_merge]

df_final = pd.merge(
    df_inse,
    df_rend_selecionado,
    on='ID_ESCOLA',
    how='inner'
)

print(f"Merge concluído! {len(df_final)} escolas encontradas em ambos os datasets.")
print(f"Colunas no arquivo de merge: {df_final.columns.tolist()}")

# 4. Salvar o resultado
df_final.to_csv(path_output_file, index=False)
print(f"\n[SUCESSO] Arquivo de merge salvo em: {path_output_file}")
print("--- PASSO 1 CONCLUÍDO ---")