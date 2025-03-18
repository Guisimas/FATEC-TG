import fitz  # PyMuPDF para manipular PDFs
import os

# Função para extrair os textos


def extrair_texto(pdf_path, pasta_textos):
    doc = fitz.open(pdf_path)
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
        pasta_textos, os.path.basename(pdf_path).replace(".pdf", ".txt"))

    with open(nome_arquivo_txt, "w", encoding="utf-8") as arquivo_txt:
        for texto in textos:
            arquivo_txt.write(texto)

    return nome_arquivo_txt

# Função para coletar pdfs armazenados


def processar_pdfs_da_pasta(pasta_pdf, pasta_textos):
    arquivos_pdf = [f for f in os.listdir(pasta_pdf) if f.endswith(".pdf")]
    for arquivo in arquivos_pdf:
        pdf_path = os.path.join(pasta_pdf, arquivo)
        print(f"Processando PDF: {arquivo}")

        nome_arquivo_txt = extrair_texto(pdf_path, pasta_textos)
        print(f"Texto extraído em: {nome_arquivo_txt}")


pasta_pdf = "./database/coleta_pdf/pdfs"
pasta_txt = "./database/coleta_pdf/extrair_txt/textos_extraidos"
processar_pdfs_da_pasta(pasta_pdf, pasta_txt)
