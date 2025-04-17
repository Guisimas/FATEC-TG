import chromadb
from chromadb.config import Settings


def connect_chroma():
    return chromadb.PersistentClient(
        path="./database/chroma_db/banco",
        settings=Settings(
            is_persistent=True,
            persist_directory="./database/chroma_db/banco",
            allow_reset=True,
            anonymized_telemetry=False),
    )


# Criar coleção
# collection = client.create_collection(name="digitalTwin")


'''def buscar_no_chroma(query, top_k=1):
    query_embedding = modelo_embedding.encode([query]).tolist()
    resultados = colecao.query(query_embedding, n_results=top_k)
    return resultados


# Exemplo de consulta
consulta = "O que faz o comando ps no Linux?"
resultados = buscar_no_chroma(consulta)

for i, resultado in enumerate(resultados["metadatas"][0]):
    print(f"🔹 Resultado {i+1}: {resultado['texto'][:300]}...\n")'''
