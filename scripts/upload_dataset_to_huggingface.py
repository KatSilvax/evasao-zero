from huggingface_hub import HfApi
import os
from dotenv import loadl_dotenv, dotenv_values

api = HfApi(token=os.getenv("HF_TOKEN"))
api.upload_folder(
    folder_path="../data/",
    repo_id="kueka/alunos-evasao-dados-inep",
    repo_type="dataset",
)
