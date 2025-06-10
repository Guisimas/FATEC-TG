import fitz  # PyMuPDF para manipular PDFs
import os
from app.embeddings.tokenization import token

# ------------------------------------
# Extrair texto do PDF com tratamento de erro
# ------------------------------------


def extrair_texto(pdf_path, pasta_textos):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(
            f"[ERRO] Não foi possível abrir o PDF: {pdf_path}\nDetalhes: {e}")
        return None  # Retorna None para indicar falha

    textos = []

    if not os.path.exists(pasta_textos):
        os.makedirs(pasta_textos)

    # Extração do texto
    for num_pagina in range(len(doc)):
        pagina = doc[num_pagina]
        texto_pagina = pagina.get_text()
        textos.append(texto_pagina)

    # Salvar o texto extraído em um arquivo .txt
    nome_arquivo_txt = os.path.join(
        pasta_textos, os.path.basename(pdf_path).replace(".pdf", ".txt")
    )

    with open(nome_arquivo_txt, "w", encoding="utf-8") as arquivo_txt:
        for texto in textos:
            arquivo_txt.write(texto)

    return nome_arquivo_txt

# ------------------------------------
# Processar PDFs armazenados com verificação de duplicidade
# ------------------------------------


def processar_pdfs_da_pasta(pasta_pdf="./pdfs", pasta_textos="./app/pdf/textos_extraidos", pasta_comp="./app/pdf/textos_extraidos/completo"):
    if not os.path.exists(pasta_textos):
        os.makedirs(pasta_textos)

    # Lista nomes base (sem extensão) dos arquivos de texto já extraídos
    textos_extraidos = {
        os.path.splitext(f)[0] for f in os.listdir(pasta_comp) if f.endswith(".txt")
    }

    # Lista os arquivos PDF
    arquivos_pdf = [f for f in os.listdir(pasta_pdf) if f.endswith(".pdf")]

    for arquivo in arquivos_pdf:
        nome_base = os.path.splitext(arquivo)[0]

        # Pula se o texto já foi extraído
        if nome_base in textos_extraidos:
            print(f"[INFO] Texto já extraído para: {arquivo}. Ignorando.")
            continue

        pdf_path = os.path.join(pasta_pdf, arquivo)
        print(f"Processando PDF: {arquivo}")

        nome_arquivo_txt = extrair_texto(pdf_path, pasta_textos)

        if nome_arquivo_txt:
            print(f"Texto extraído em: {nome_arquivo_txt}")
        else:
            print(f"[AVISO] PDF ignorado: {arquivo}")

    token()
