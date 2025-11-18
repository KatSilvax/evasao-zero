from huggingface_hub import HfApi
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

api = HfApi(token=os.getenv("HF_TOKEN"))
api.upload_folder(
    folder_path="../data/",
    repo_id="kueka/alunos-evasao-dados-inep",
    repo_type="dataset",
)
