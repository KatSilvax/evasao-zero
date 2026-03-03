"""Script para treinar modelo básico."""
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "dados_limpos.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")

print("🤖 Treinando modelo...")

# Carregar dados
df = pd.read_csv(DATA_FILE)
print(f"✅ {len(df)} registros carregados")

# Preparar dados (exemplo simples)
# Selecionar apenas colunas numéricas para o exemplo
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
X = df[numeric_cols].fillna(0)
y = df['TAXA_ABANDONO_GERAL'].fillna(0) > 0  # Classificação binária

# Treinar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Salvar modelo
os.makedirs(MODELS_DIR, exist_ok=True)
joblib.dump(model, os.path.join(MODELS_DIR, "modelo_evasao.joblib"))
joblib.dump(X.columns.tolist(), os.path.join(MODELS_DIR, "colunas_modelo.joblib"))

print(f"✅ Modelo treinado e salvo em {MODELS_DIR}")
print(f"📊 Acurácia: {model.score(X_test, y_test):.2%}")
