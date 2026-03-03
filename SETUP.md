# 🔧 Configuração Inicial

## ⚠️ IMPORTANTE: Modelos não incluídos no repositório

Os arquivos de modelo (`.joblib`) são muito grandes e não estão no GitHub.

## 🚀 Após clonar o repositório:

### 1. Instalar dependências
```bash
pip install pandas numpy scikit-learn joblib streamlit plotly
```

### 2. Treinar o modelo
```bash
python scripts/train_model_real.py
```

Isso vai criar:
- `models/modelo_evasao.joblib`
- `models/colunas_modelo.joblib`
- `deployments/dashboard/modelo_evasao.joblib`
- `deployments/dashboard/colunas_modelo.joblib`

### 3. Executar o dashboard
```bash
streamlit run deployments/dashboard/app_simples.py
```

## ⏱️ Tempo estimado
- Instalação: ~2 minutos
- Treinamento: ~1 minuto
- Total: ~3 minutos

---

**Pronto!** Agora você pode usar o dashboard normalmente.
