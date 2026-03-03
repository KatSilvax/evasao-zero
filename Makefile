.PHONY: help install sync data train dashboard test lint format clean docs

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala o uv (gerenciador de pacotes)
	@echo "Instalando uv..."
	@powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

sync: ## Sincroniza dependências com uv
	@echo "Sincronizando dependências..."
	@uv sync

data: ## Baixa o dataset do HuggingFace
	@echo "Baixando dataset..."
	@uv run python scripts/download_dataset.py

process: ## Processa os microdados do INEP
	@echo "Processando microdados..."
	@uv run python scripts/processar_microdados.py

train: ## Treina o modelo (via notebook)
	@echo "Execute: notebooks/02_treinamento_do_modelo.ipynb"

dashboard: ## Inicia o dashboard Streamlit
	@echo "Iniciando dashboard..."
	@uv run streamlit run deployments/dashboard/app.py

test: ## Executa os testes
	@echo "Executando testes..."
	@uv run pytest tests/ -v

test-cov: ## Executa testes com cobertura
	@echo "Executando testes com cobertura..."
	@uv run pytest tests/ --cov=src --cov-report=html

lint: ## Verifica código com ruff
	@echo "Verificando código..."
	@uv run ruff check src/ scripts/ tests/

format: ## Formata código com ruff
	@echo "Formatando código..."
	@uv run ruff format src/ scripts/ tests/

docs: ## Serve a documentação localmente
	@echo "Servindo documentação..."
	@uv run mkdocs serve

docs-build: ## Build da documentação
	@echo "Building documentação..."
	@uv run mkdocs build

clean: ## Remove arquivos temporários
	@echo "Limpando arquivos temporários..."
	@rm -rf .pytest_cache __pycache__ .ruff_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

setup: sync data ## Setup completo do projeto
	@echo "✅ Projeto configurado com sucesso!"
	@echo "Execute 'make dashboard' para iniciar o dashboard"

all: sync test lint ## Executa sync, testes e lint
	@echo "✅ Tudo pronto!"
