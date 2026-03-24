import requests

def download_data(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        print(f"Downloading started (Status Code: {response.status_code})")

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                f.write(chunk)
        print(f"File '{filename}' downloaded successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")

url_tx_rend_escolar = "https://download.inep.gov.br/informacoes_estatisticas/indicadores_educacionais/2021/tx_rend_escolas_2021.zip"
url_nivel_socioeconomico = "https://download.inep.gov.br/informacoes_estatisticas/indicadores_educacionais/2021/nivel_socioeconomico/INSE_2021_escolas.xlsx"

download_data(url_tx_rend_escolar, "tx_rend_escolar.zip")
download_data(url_nivel_socioeconomico, "INSE_2021_escolas.xlsx")



