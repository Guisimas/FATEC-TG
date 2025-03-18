from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os

# Função para gerar um novo nome de arquivo com número incremental


def nomes_unicos(filepath):
    if not os.path.exists(filepath):
        return filepath
    base, ext = os.path.splitext(filepath)
    i = 1
    while os.path.exists(f"{base}_{i}{ext}"):
        i += 1
    return f"{base}_{i}{ext}"


# Configurar o driver do navegador (precisa do ChromeDriver instalado)
driver = webdriver.Chrome()

# URL para buscar PDFs
url = "https://scholar.google.com.br/scholar?hl=pt-BR&as_sdt=0%2C5&q=linux&btnG=&lr=lang_pt"

# Pasta para armazenar PDFs
pdf_dir = "./database/coleta_pdf/pdfs"

# Abrir a página no navegador
driver.get(url)
time.sleep(3)  # Aguarda a página carregar

# Coletar todos os links da página
links = driver.find_elements(By.TAG_NAME, "a")

# Cria pasta caso não exista
if not os.path.exists(pdf_dir):
    os.makedirs(pdf_dir)

# Baixar arquivos PDF
for link in links:
    pdf_url = link.get_attribute("href")
    if pdf_url and pdf_url.endswith(".pdf"):
        # Obter nome do arquivo
        pdf_name = pdf_url.split("/")[-1]
        # Gerar caminho único para o arquivo
        pdf_path = os.path.join(pdf_dir, pdf_name)
        unico_pdf_path = nomes_unicos(pdf_path)

        # Baixar o PDF
        try:
            response = requests.get(pdf_url)
            if response.status_code == 200:
                with open(unico_pdf_path, "wb") as f:
                    f.write(response.content)
                print(f"Baixado: {unico_pdf_path}")
            else:
                print(f"Falha ao baixar {pdf_url}. Código de status: {
                      response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar {pdf_url}: {e}")

# Fechar o navegador
driver.quit()
