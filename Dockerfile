FROM python:3.10-slim

WORKDIR /app

# Instalar uv
RUN pip install uv

# Copiar arquivos de configuração
COPY pyproject.toml uv.lock ./

# Sincronizar dependências
RUN uv sync --frozen

# Copiar código-fonte
COPY . .

# Expor porta do Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Comando para iniciar o dashboard
ENTRYPOINT ["uv", "run", "streamlit", "run", "deployments/dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
