"""
Script para treinar modelo de predicao de evasao escolar
Usando dados reais de escolas (INSE e taxas de abandono)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

def main():
    print("=" * 60)
    print("TREINAMENTO DO MODELO DE PREDICAO DE EVASAO ESCOLAR")
    print("=" * 60)
    
    # Carregar dados
    print("\n1. Carregando dados...")
    df = pd.read_csv('data/dados_limpos.csv')
    print(f"   [OK] Total de registros: {len(df)}")
    
    # Criar variavel alvo baseada na taxa de abandono
    print(f"\n2. Criando variavel alvo...")
    df['TAXA_ABANDONO_GERAL'] = pd.to_numeric(df['TAXA_ABANDONO_GERAL'], errors='coerce')
    df['risco_evasao'] = (df['TAXA_ABANDONO_GERAL'] > 5).astype(int)  # Risco se taxa > 5%
    
    # Selecionar features relevantes
    features = [
        'MEDIA_INSE',
        'PC_NIVEL_1', 'PC_NIVEL_2', 'PC_NIVEL_3', 'PC_NIVEL_4',
        'PC_NIVEL_5', 'PC_NIVEL_6', 'PC_NIVEL_7', 'PC_NIVEL_8',
        'TP_TIPO_REDE', 'TP_LOCALIZACAO', 'TP_CAPITAL'
    ]
    
    # Remover valores nulos
    df_clean = df[features + ['risco_evasao']].dropna()
    print(f"   [OK] Registros apos limpeza: {len(df_clean)}")
    print(f"   [OK] Distribuicao: {dict(df_clean['risco_evasao'].value_counts())}")
    
    X = df_clean[features]
    y = df_clean['risco_evasao']
    
    # Split treino/teste
    print(f"\n3. Dividindo dados (80% treino, 20% teste)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   [OK] Treino: {len(X_train)}, Teste: {len(X_test)}")
    
    # Criar modelo
    print(f"\n4. Criando modelo Random Forest...")
    modelo = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1
    )
    print(f"   [OK] Modelo criado")
    
    # Validacao cruzada
    print(f"\n5. Executando validacao cruzada (5 folds)...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(modelo, X_train, y_train, cv=cv, scoring='accuracy', n_jobs=-1)
    
    print(f"   Acuracia por fold: {[f'{s:.4f}' for s in scores]}")
    print(f"   [OK] Acuracia media: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
    
    # Treinar modelo final
    print(f"\n6. Treinando modelo final...")
    modelo.fit(X_train, y_train)
    print(f"   [OK] Modelo treinado")
    
    # Avaliar no teste
    print(f"\n7. Avaliacao no conjunto de teste:")
    y_pred = modelo.predict(X_test)
    print("\n" + classification_report(y_test, y_pred, zero_division=0))
    
    # Importancia das features
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': modelo.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n8. Top 10 Features mais importantes:")
    for idx, row in feature_importance.head(10).iterrows():
        print(f"   {row['feature']}: {row['importance']:.4f}")
    
    # Salvar modelo
    print(f"\n9. Salvando modelo...")
    
    # Criar diretorios
    os.makedirs('models', exist_ok=True)
    os.makedirs('deployments/dashboard', exist_ok=True)
    
    # Salvar na pasta models
    joblib.dump(modelo, 'models/modelo_evasao.joblib')
    joblib.dump(features, 'models/colunas_modelo.joblib')
    print(f"   [OK] Salvos em models/")
    
    # Copiar para pasta dashboard
    joblib.dump(modelo, 'deployments/dashboard/modelo_evasao.joblib')
    joblib.dump(features, 'deployments/dashboard/colunas_modelo.joblib')
    print(f"   [OK] Copiados para deployments/dashboard/")
    
    # Verificar arquivos
    print(f"\n10. Verificacao dos arquivos:")
    for pasta in ['models', 'deployments/dashboard']:
        print(f"\n   {pasta}/:")
        for arquivo in ['modelo_evasao.joblib', 'colunas_modelo.joblib']:
            caminho = os.path.join(pasta, arquivo)
            if os.path.exists(caminho):
                size = os.path.getsize(caminho) / 1024
                print(f"      [OK] {arquivo} ({size:.2f} KB)")
            else:
                print(f"      [ERRO] {arquivo} (NAO ENCONTRADO)")
    
    print("\n" + "=" * 60)
    print("[SUCESSO] MODELO TREINADO E SALVO COM SUCESSO!")
    print("=" * 60)
    print("\nAgora voce pode executar o dashboard com:")
    print("  streamlit run deployments/dashboard/app.py")

if __name__ == "__main__":
    main()
