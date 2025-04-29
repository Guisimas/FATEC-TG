import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chat_mistral import gerar_resposta_mistral  # sua função que chama a API do Mistral

# Carrega o modelo de embeddings
modelo_embedding = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Conecta ao ChromaDB existente
cliente_chroma = chromadb.PersistentClient(path="./database/chroma_db", settings=Settings())
colecao = cliente_chroma.get_or_create_collection("curso_software_engineering")

# Função para buscar no banco vetorial
def buscar_no_chroma(query, top_k=3):
    query_embedding = modelo_embedding.encode([query]).tolist()
    resultados = colecao.query(query_embedding, n_results=top_k)
    return resultados

# Função principal de chat
def chat_com_mistral():
    print("🧠 Chat com IA baseada nos textos do ChromaDB. Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("Você: ")

        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("👋 Encerrando o chat. Até logo!")
            break

        # Busca os trechos mais relevantes no ChromaDB
        resultados = buscar_no_chroma(pergunta, top_k=3)

        if not resultados["metadatas"][0]:
            print("⚠️ Nenhum resultado relevante encontrado no banco de dados.")
            continue

        # Monta o contexto com os trechos retornados
        contexto = "\n\n".join([r["texto"] for r in resultados["metadatas"][0]])

        # Gera a resposta com Mistral
        resposta = gerar_resposta_mistral(pergunta, contexto)

        print(f"\n🤖 Mistral: {resposta}\n")

# Executa o chat
if __name__ == "__main__":
    chat_com_mistral()
