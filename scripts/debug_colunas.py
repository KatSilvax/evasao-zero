import pandas as pd
import numpy as np
import sys
import os

print("--- INICIANDO SCRIPT DE DEBUG DE COLUNAS ---")

# --- 0. Definição de Caminhos ---
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
path_rend = os.path.join(BASE_DIR, 'data', 'raw', 'tx_rend_escolas_2021.csv')

print(f"Lendo cabeçalho de: {path_rend}")

try:
    # Carregar o arquivo de rendimento com a lógica complexa
    df_rend = pd.read_csv(
        path_rend, 
        sep=';', 
        skiprows=5,
        header=[0, 1, 2],
        encoding='latin1'
    )
    
    # Achatar o cabeçalho
    df_rend.columns = [' - '.join(col).strip() for col in df_rend.columns.values]
    
    print("\n[SUCESSO] Arquivo lido. Procurando por colunas de 'ABANDONO'...")
    
    # --- 4. A Lógica de Debug ---
    
    # Obter todas as colunas
    all_columns = df_rend.columns.tolist()
    
    # Filtrar apenas as que contêm "ABANDONO"
    colunas_de_abandono = [col for col in all_columns if "ABANDONO" in col.upper()]
    
    if colunas_de_abandono:
        print("\n--- COLUNAS DE ABANDONO ENCONTRADAS ---")
        for col in colunas_de_abandono:
            # Imprimir o nome exato da coluna
            print(f"'{col}'") 
        print("------------------------------------------")
    else:
        print("\n--- NENHUMA COLUNA DE 'ABANDONO' FOI ENCONTRADA ---")

except Exception as e:
    print(f"ERRO ao processar o arquivo de rendimento: {e}")

print("\n--- DEBUG CONCLUÍDO ---")