import shutil
from sentence_transformers import SentenceTransformer
import spacy
import math
import os
import sys

from database.coleta_pdf.extrair_txt.extract_text import extrair_texto
# from .chat_mistral import gerar_resposta_mistral


sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'chroma_db')))
from ConfgChroma import connect_chroma

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))

pasta_incremental = os.path.join(PROJECT_ROOT, "database", "coleta_pdf", "extrair_txt", "textos_incrementais")
pasta_pdf_dest = os.path.join(PROJECT_ROOT, "database", "coleta_pdf", "pdfs")
pasta_extraidos = os.path.join(PROJECT_ROOT, "database", "coleta_pdf", "extrair_txt", "textos_extraidos")

nlp = spacy.load("pt_core_news_sm")

def dividir_em_trechos(texto, tokens_por_trecho):
    paragrafos = texto.split("\n\n")
    trechos = []

    tamanho_trecho = math.ceil(tokens_por_trecho / 0.75)

    for par in paragrafos:
        par = par.strip()
        if not par:
            continue

        if len(par) > 1000000:
            # Se o parágrafo for grande demais, corta em pedaços menores
            for i in range(0, len(par), 1000000):
                sub_par = par[i:i+1000000]
                doc = nlp(sub_par)
                palavras = [token.text for token in doc]
                trechos.extend([
                    " ".join(palavras[i:i + tamanho_trecho])
                    for i in range(0, len(palavras), tamanho_trecho)
                ])
        else:
            doc = nlp(par)
            palavras = [token.text for token in doc]
            trechos.extend([
                " ".join(palavras[i:i + tamanho_trecho])
                for i in range(0, len(palavras), tamanho_trecho)
            ])

    return trechos


def adicionar_novo_texto(texto, tokens_por_trecho=200):
    trechos = dividir_em_trechos(texto, tokens_por_trecho)
    print(f"Texto dividido em {len(trechos)} trechos.")

    embeddings = modelo_embedding.encode(trechos).tolist()
    novos_ids = []

    for idx, (emb, trecho) in enumerate(zip(embeddings, trechos)):
        novo_id = f"novo_{colecao.count()}_{idx}"
        novos_ids.append(novo_id)
        colecao.add(
            ids=[novo_id],
            embeddings=[emb],
            metadatas=[{"texto": trecho}]
        )

    print(f"{len(novos_ids)} novos trechos adicionados à coleção.")
    print(f"Total de documentos agora: {colecao.count()}")
    return novos_ids

def processar_pasta_com_txt(pasta_txt, tokens_por_trecho):
    trechos = []

    arquivos_txt = [f for f in os.listdir(pasta_txt) if f.endswith(".txt")]

    for arquivo_txt in arquivos_txt:
        caminho_arquivo = os.path.join(pasta_txt, arquivo_txt)
        with open(caminho_arquivo, "r", encoding="utf-8") as file:
            texto = file.read()

        trechos_arquivo = dividir_em_trechos(texto, tokens_por_trecho)
        trechos.extend(trechos_arquivo)

        print(f"Arquivo {arquivo_txt} processado. {len(trechos_arquivo)} trechos extraídos.")

    return trechos

def gerar_embeddings(trechos):
    return modelo_embedding.encode(trechos, convert_to_tensor=True)

def adicionar_novo_pdf(tokens_por_trecho=200):
    arquivos_pdf = [f for f in os.listdir(pasta_incremental) if f.endswith('.pdf')]

    for arquivo_pdf in arquivos_pdf:
        try:
            print(f"Processando {arquivo_pdf}...")

            caminho_pdf = os.path.join(pasta_incremental, arquivo_pdf)
            # Extrair texto
            caminho_txt = extrair_texto(caminho_pdf, pasta_incremental)

            with open(caminho_txt, "r", encoding="utf-8") as f:
                texto = f.read()

            # Dividir em trechos
            trechos = dividir_em_trechos(texto, tokens_por_trecho)
            print(f"Texto dividido em {len(trechos)} trechos.")

            # Gerar embeddings
            embeddings = modelo_embedding.encode(trechos).tolist()

            novos_ids = []
            for idx, (emb, trecho) in enumerate(zip(embeddings, trechos)):
                novo_id = f"novo_{colecao.count()}_{idx}"
                novos_ids.append(novo_id)
                colecao.add(
                    ids=[novo_id],
                    embeddings=[emb],
                    metadatas=[{"texto": trecho}]
                )

            print(f"{len(novos_ids)} novos trechos adicionados ao ChromaDB.")

            # Mover PDF para pasta de PDFs
            shutil.move(caminho_pdf, os.path.join(pasta_pdf_dest, arquivo_pdf))
            print(f"PDF movido para {pasta_pdf_dest}")

            # Mover TXT para pasta de textos extraídos
            novo_txt_path = os.path.join(pasta_extraidos, os.path.basename(caminho_txt))
            shutil.move(caminho_txt, novo_txt_path)
            print(f"TXT movido para {pasta_extraidos}")

        except Exception as e:
            print(f"Erro ao processar {arquivo_pdf}: {e}")

    print(f"Processamento finalizado. Total na coleção: {colecao.count()}")


# # Configurações
# pasta_txt = "./database/coleta_pdf/extrair_txt/textos_extraidos"
# tokens_por_trecho = 200

# # Processamento
# trechos = processar_pasta_com_txt(pasta_txt, tokens_por_trecho)
# print(f"Texto dividido em {len(trechos)} trechos.")

modelo_embedding = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# embeddings = gerar_embeddings(trechos)
# print(f"Gerados {len(embeddings)} embeddings.")

# Conexão com o banco ChromaDB
client = connect_chroma()
colecao = client.get_or_create_collection(name="digitalTwin")

# # Armazenar embeddings
# for i, (embedding, trecho) in enumerate(zip(embeddings, trechos)):
#     colecao.add(
#         ids=[str(i)],
#         embeddings=[embedding.tolist()],
#         metadatas=[{"indice": i, "texto": trecho}]
#     )

# print("Embeddings armazenados no ChromaDB.")
# print(f"Total de documentos na coleção: {colecao.count()}")


# # Exemplo de busca
# def buscar_no_chroma(query, top_k=1):
#     query_embedding = modelo_embedding.encode([query]).tolist()
#     resultados = colecao.query(query_embedding, n_results=top_k)
#     return resultados

# consulta = "O que faz o comando ps no Linux?"
# resultados = buscar_no_chroma(consulta)

# contexto = "\n\n".join([r["texto"] for r in resultados["metadatas"][0]])
# resposta = gerar_resposta_mistral(consulta, contexto)
# print(f"\n💬 Resposta gerada:\n{resposta}")


# adicionar_novo_pdf(tokens_por_trecho=200)