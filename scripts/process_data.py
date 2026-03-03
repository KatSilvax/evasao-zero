"""Script para processar dados e treinar modelo de evasão."""
import pandas as pd
import os

# Diretórios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Criar diretórios se não existirem
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

print("🔄 Processando dados...")
print(f"📂 Procurando em: {DATA_DIR}")

# Verificar se existe arquivo de dados
data_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
if not data_files:
    print("❌ Nenhum arquivo CSV encontrado em data/")
    print("Por favor, adicione os dados do INEP na pasta data/")
    exit(1)

# Usar o primeiro arquivo CSV encontrado
data_file = os.path.join(DATA_DIR, data_files[0])
print(f"📂 Usando arquivo: {data_files[0]}")

try:
    df = pd.read_csv(data_file)
    print(f"✅ Dados carregados: {len(df)} registros")
    
    # Salvar dados processados
    output_file = os.path.join(DATA_DIR, "dados_limpos.csv")
    df.to_csv(output_file, index=False)
    print(f"✅ Dados salvos em: {output_file}")
    
    print("\n📊 Resumo dos dados:")
    print(df.info())
    
except Exception as e:
    print(f"❌ Erro ao processar dados: {e}")
    exit(1)

print("\n✅ Processamento concluído!")
print("\nPróximos passos:")
print("1. Execute os notebooks para análise detalhada")
print("2. Treine o modelo com: uv run python scripts/train_model.py")
