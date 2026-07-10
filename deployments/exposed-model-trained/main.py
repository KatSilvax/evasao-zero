from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

# ==============================================================================
# Configurações
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent

#MODELS_DIR = BASE_DIR / "models"
UPLOADS_DIR = BASE_DIR / "uploads"

MODELS_DIR = "/home/kaue/IFMS/evasao-zero/models"
UPLOADS_DIR.mkdir(exist_ok=True)

#MODEL_PATH = MODELS_DIR / "modelo_formulario.joblib"
#COLUMNS_PATH = MODELS_DIR / "colunas_formulario.joblib"
MODEL_PATH = "/home/kaue/IFMS/evasao-zero/models/modelo_formulario.joblib"
COLUMNS_PATH = "/home/kaue/IFMS/evasao-zero/models/colunas_formulario.joblib"

# ==============================================================================
# Inicialização da API
# ==============================================================================

app = FastAPI(
    title="API de Predição",
    description="API para inferência de um modelo de Machine Learning",
    version="1.0.0"
)

# Variáveis globais
model = None
training_columns = None


# ==============================================================================
# Carregamento do modelo
# ==============================================================================

@app.on_event("startup")
def load_model():
    global model
    global training_columns

    try:
        model = joblib.load(MODEL_PATH)
        training_columns = joblib.load(COLUMNS_PATH)

        print("✅ Modelo carregado com sucesso!")

    except FileNotFoundError:
        raise RuntimeError(
            "Modelo ou arquivo de colunas não encontrado."
        )


# ==============================================================================
# Rotas
# ==============================================================================

@app.get("/")
def root():
    return {
        "message": "API Online",
        "docs": "/docs"
    }

@app.get("/features")
def features():
    return {
        "features": training_columns
    }

@app.get("/health")
def health():
    return {
        "status": "online",
        "model_loaded": model is not None
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Somente arquivos CSV são permitidos."
        )

    filepath = UPLOADS_DIR / file.filename

    try:
        # Salva o arquivo enviado
        with open(filepath, "wb") as buffer:
            buffer.write(await file.read())

        # Lê o CSV
        df = pd.read_csv(filepath)

        # Verifica se todas as colunas esperadas existem
        missing = set(training_columns) - set(df.columns)

        #if missing:
         #   raise HTTPException(
         #       status_code=400,
         #       detail=f"Colunas ausentes: {list(missing)}"
          #  )

        # Reorganiza as colunas na mesma ordem do treinamento
        df = df.reindex(columns=training_columns)

        # Predição
        predictions = model.predict(df)

        response = {
            "rows": len(df),
            "predictions": predictions.tolist()
        }

        # Probabilidades (caso existam)
        if hasattr(model, "predict_proba"):
            response["probabilities"] = (
                model.predict_proba(df)
                .max(axis=1)
                .tolist()
            )

        return JSONResponse(response)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if filepath.exists():
            filepath.unlink()


# ==============================================================================
# Execução
# ==============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",   # substitua "main" pelo nome do arquivo
        host="0.0.0.0",
        port=8000,
        reload=True
    )