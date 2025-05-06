from sentence_transformers import SentenceTransformer
import spacy
import math
import os
import sys

from chat_mistral import gerar_resposta_mistral


sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'chroma_db')))
from ConfgChroma import connect_chroma


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

# Configurações
pasta_txt = "./database/coleta_pdf/extrair_txt/textos_extraidos"
tokens_por_trecho = 200

# Processamento
trechos = processar_pasta_com_txt(pasta_txt, tokens_por_trecho)
print(f"Texto dividido em {len(trechos)} trechos.")

modelo_embedding = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = gerar_embeddings(trechos)
print(f"Gerados {len(embeddings)} embeddings.")

# Conexão com o banco ChromaDB
client = connect_chroma()
colecao = client.get_or_create_collection(name="digitalTwin")

# Armazenar embeddings
for i, (embedding, trecho) in enumerate(zip(embeddings, trechos)):
    colecao.add(
        ids=[str(i)],
        embeddings=[embedding.tolist()],
        metadatas=[{"indice": i, "texto": trecho}]
    )

print("Embeddings armazenados no ChromaDB.")
print(f"Total de documentos na coleção: {colecao.count()}")

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
