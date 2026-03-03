from huggingface_hub import snapshot_download, login
import os

# 🔐 Your Hugging Face token

token = os.getenv("HUGGINGFACE_TOKEN")  # <-- replace with your real token

# Login using token
login(token=HF_TOKEN)

# Dataset repository ID
REPO_ID = "kueka/alunos-evasao-dados-inep"  # <-- replace with correct repo

# Download entire dataset
local_path = snapshot_download(
    repo_id=REPO_ID,
    repo_type="dataset",
    local_dir="./alunos-evasao-dados-inep"
)

print("Download completed!")
print("Saved at:", local_path)