from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import requests
import time
import os
from urllib.parse import urlencode
from app.pdf.extractor import processar_pdfs_da_pasta

# Busca por PDFs no Google Scholar


def busca_sites(termo_busca, paginas=5):
    # Cabeçalhos para simular um navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Firefox em modo invisível
    options = FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Firefox(options=options)

    # Diretório para salvar PDFs
    pdf_dir = "./pdfs/2"
    os.makedirs(pdf_dir, exist_ok=True)

    base_url = "https://scholar.google.com.br/scholar"

    for i in range(paginas):
        start = i * 10
        params = {
            "hl": "pt-BR",
            "as_sdt": "0,5",
            "q": termo_busca,
            "lr": "lang_pt",
            "start": str(start)
        }
        url = f"{base_url}?{urlencode(params)}"
        print(f"[INFO] Buscando: {url}")
        driver.get(url)
        time.sleep(3)

        links = driver.find_elements(By.TAG_NAME, "a")

        for link in links:
            href = link.get_attribute("href")
            if href and href.endswith(".pdf"):
                try:
                    response = requests.get(href, headers=headers)
                    if response.status_code == 200:
                        nome_arquivo = href.split("/")[-1].split("?")[0]
                        caminho_pdf = os.path.join(pdf_dir, nome_arquivo)
                        with open(caminho_pdf, "wb") as f:
                            f.write(response.content)
                        print(f"[PDF] Baixado: {caminho_pdf}")
                    else:
                        print(
                            f"[ERRO] Falha ao baixar {href} - Status: {response.status_code}")
                except requests.RequestException as e:
                    print(f"[ERRO] Erro ao baixar PDF: {e}")

    driver.quit()
    processar_pdfs_da_pasta()


# Executar a função de busca
busca_sites("chmod")
