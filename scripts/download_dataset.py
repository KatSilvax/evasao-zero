from huggingface_hub import snapshot_download
import os
from dotenv import load_dotenv

load_dotenv("scripts/.env")

token = os.getenv("HF_TOKEN")
if not token:
    print("❌ Erro: HF_TOKEN não encontrado no arquivo scripts/.env")
    print("\nCrie o arquivo scripts/.env com:")
    print("HF_TOKEN=seu_token_aqui")
    print("\nObtenha seu token em: https://huggingface.co/settings/tokens")
    exit(1)

snapshot_download(
    repo_id="kueka/alunos-evasao-dados-inep",
    repo_type="dataset",
    local_dir="../data/",
    local_dir_use_symlinks=False,
    token=token
)

print("✅ Dataset baixado com sucesso em data/")
