import os
import sys
import chromadb
import spacy
import torch
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from database.coleta_pdf.extrair_txt.chat_mistral import gerar_resposta_mistral

# Carregar modelo de embedding e NLP
modelo_embedding = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
nlp = spacy.load("pt_core_news_sm")

# Conectar ao banco vetorial
client = chromadb.PersistentClient(
    path="./database/chroma_db/banco", settings=Settings()
)
colecao = client.get_collection("digitalTwin")


def buscar_no_chroma(query, top_k=1):
    query_embedding = modelo_embedding.encode([query]).tolist()
    resultados = colecao.query(query_embedding, n_results=top_k)
    return resultados


def gerar_resposta(query):
    resultados = buscar_no_chroma(query, top_k=3)

    if not resultados["metadatas"] or not resultados["metadatas"][0]:
        return "Desculpe, não encontrei informações relevantes."

    contexto = "\n\n".join([r["texto"] for r in resultados["metadatas"][0]])
    resposta = gerar_resposta_mistral(query, contexto)
    return resposta
