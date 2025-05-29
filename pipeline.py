import os
import shutil
import sys
import chromadb
import spacy
import torch
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from database.chroma_db.ConfgChroma import connect_chroma
from database.coleta_pdf.extrair_txt.chat_mistral import gerar_resposta_mistral
from database.coleta_pdf.extrair_txt.token_text import  dividir_em_trechos
from database.coleta_pdf.extrair_txt.extract_text import extrair_texto

# Carregar modelo de embedding e NLP
modelo_embedding = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
nlp = spacy.load("pt_core_news_sm")

# Conectar ao banco vetorial
client = connect_chroma()
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


def adicionar_novo_pdf(tokens_por_trecho=200):
    pasta_incremental = r"C:\Developer\tcc\FATEC-TG\database\coleta_pdf\extrair_txt\textos_incrementais"
    pasta_pdf_dest = r"C:\Developer\tcc\FATEC-TG\database\coleta_pdf\extrair_txt\pdfs_processados"
    pasta_extraidos = r"C:\Developer\tcc\FATEC-TG\database\coleta_pdf\extrair_txt\textos_extraidos"

    if not os.path.exists(pasta_incremental):
        print(f"⚠️ Pasta não encontrada: {pasta_incremental}")
        return

    arquivos_pdf = [f for f in os.listdir(pasta_incremental) if f.lower().endswith(".pdf")]

    for arquivo_pdf in arquivos_pdf:
        try:
            print(f"🔄 Processando {arquivo_pdf}...")

            caminho_pdf = os.path.join(pasta_incremental, arquivo_pdf)

            # ✅ Extrair texto
            caminho_txt = extrair_texto(caminho_pdf, pasta_incremental)

            with open(caminho_txt, "r", encoding="utf-8") as f:
                texto = f.read()

            # ✅ Dividir em trechos
            trechos = dividir_em_trechos(texto, tokens_por_trecho)
            print(f"✂️ Texto dividido em {len(trechos)} trechos.")

            # ✅ Gerar embeddings
            embeddings = modelo_embedding.encode(trechos).tolist()

            novos_ids = []
            for idx, (emb, trecho) in enumerate(zip(embeddings, trechos)):
                novo_id = f"novo_{colecao.count()}_{idx}"
                novos_ids.append(novo_id)
                colecao.add(
                    ids=[novo_id],
                    embeddings=[emb],
                    metadatas=[{"texto": trecho, "origem": arquivo_pdf}]
                )

            print(f"✅ {len(novos_ids)} novos trechos adicionados ao ChromaDB.")

            # ✅ Mover PDF para pasta de PDFs processados
            os.makedirs(pasta_pdf_dest, exist_ok=True)
            shutil.move(caminho_pdf, os.path.join(pasta_pdf_dest, arquivo_pdf))
            print(f"📦 PDF movido para {pasta_pdf_dest}")

            # ✅ Mover TXT para pasta de textos extraídos
            os.makedirs(pasta_extraidos, exist_ok=True)
            novo_txt_path = os.path.join(pasta_extraidos, os.path.basename(caminho_txt))
            shutil.move(caminho_txt, novo_txt_path)
            print(f"📄 TXT movido para {pasta_extraidos}")

        except Exception as e:
            print(f"❌ Erro ao processar {arquivo_pdf}: {e}")

    print(f"✅ Processamento finalizado. Total de itens na coleção: {colecao.count()}")

def adicionar_novo_texto(texto):
    if not texto.strip():
        print("⚠️ Texto vazio, nada foi adicionado.")
        return

    doc = nlp(texto)
    sentencas = [sent.text for sent in doc.sents]

    for idx, sentenca in enumerate(sentencas):
        embedding = modelo_embedding.encode([sentenca]).tolist()
        colecao.add(
            embeddings=embedding,
            documents=[sentenca],
            metadatas=[{"texto": sentenca, "origem": "insercao_manual"}]
        )

    print("✅ Texto manual adicionado ao banco vetorial.")