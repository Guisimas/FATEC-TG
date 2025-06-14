import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import quote_plus
from app.pdf.extractor import processar_pdfs_da_pasta


def busca_sites(termo_busca):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    termo_codificado = quote_plus(termo_busca)
    urls_coletadas = []

    for pagina in range(1, 6):
        url_busca = f"https://guialinux.uniriotec.br/page/{pagina}/?s={termo_codificado}"
        print(f"[INFO] Acessando página {pagina}: {url_busca}")

        response = requests.get(url_busca, headers=headers)
        if response.status_code != 200:
            print(
                f"[ERRO] Falha ao acessar a página {pagina} - Status: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        resultados = soup.find_all("h1", class_="entry-title")

        for resultado in resultados:
            a_tag = resultado.find("a")
            if a_tag:
                href = a_tag.get("href")
                texto = a_tag.text.strip().lower()
                if "sumário" not in texto and href not in urls_coletadas:
                    urls_coletadas.append(href)

    print(f"[INFO] {len(urls_coletadas)} links coletados no total")

    # Criar pasta para salvar textos
    html_dir = "./app/pdf/textos_extraidos"
    os.makedirs(html_dir, exist_ok=True)

    for idx, url in enumerate(urls_coletadas):
        try:
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                page = BeautifulSoup(resp.content, "html.parser")
                conteudo = page.get_text()
                nome_arquivo = f"pagina_{termo_busca}_{idx+1}.txt"
                caminho_arquivo = os.path.join(html_dir, nome_arquivo)
                with open(caminho_arquivo, "w", encoding="utf-8") as f:
                    f.write(conteudo)
                print(f"[HTML] Texto salvo em: {caminho_arquivo}")
            else:
                print(
                    f"[ERRO] Falha ao acessar {url} - Status: {resp.status_code}")
        except Exception as e:
            print(f"[ERRO] Falha ao processar {url}: {e}")

    processar_pdfs_da_pasta()
