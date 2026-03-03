"""Script para executar notebooks automaticamente."""
import subprocess
import sys

notebooks = [
    "notebooks/01_limpeza_e_analise.ipynb",
    "notebooks/02_treinamento_do_modelo.ipynb"
]

print("🚀 Executando notebooks...\n")

for notebook in notebooks:
    print(f"📓 Executando: {notebook}")
    result = subprocess.run(
        ["jupyter", "nbconvert", "--to", "notebook", "--execute", 
         "--inplace", notebook],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ {notebook} executado com sucesso!\n")
    else:
        print(f"❌ Erro ao executar {notebook}")
        print(result.stderr)
        sys.exit(1)

print("🎉 Todos os notebooks foram executados!")
print("\nAgora você pode rodar o dashboard:")
print("  uv run streamlit run deployments/dashboard/app.py")
