from sentence_transformers import SentenceTransformer
import spacy
import math
import os
import chromadb
from chromadb.config import Settings
from chat_mistral import gerar_resposta_mistral

# Carregar o modelo spaCy para português
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

    # Listar arquivos .txt na pasta
    arquivos_txt = [f for f in os.listdir(pasta_txt) if f.endswith(".txt")]

    # Processar cada arquivo .txt
    for arquivo_txt in arquivos_txt:
        caminho_arquivo = os.path.join(pasta_txt, arquivo_txt)

        # Ler o conteúdo do arquivo
        with open(caminho_arquivo, "r", encoding="utf-8") as file:
            texto = file.read()

        # Dividir o texto em trechos
        trechos.extend(dividir_em_trechos(texto, tokens_por_trecho))

        print(f"Arquivo {arquivo_txt} processado. {
              len(trechos)} trechos extraídos.")

    return trechos


# Caminho da pasta contendo os arquivos .txt
# Substitua pelo caminho real da sua pasta com arquivos .txt
pasta_txt = "database/coleta_pdf/extrair_txt/textos_extraidos"

# Definir quantos tokens deseja por trecho (exemplo: 200 tokens)
tokens_por_trecho = 200

# Processar os arquivos da pasta e dividir em trechos
trechos = processar_pasta_com_txt(pasta_txt, tokens_por_trecho)

print(f"Texto dividido em {len(trechos)} trechos.")


modelo_embedding = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2")

def gerar_embeddings(trechos):
    return modelo_embedding.encode(trechos, convert_to_tensor=True)


# Gerar embeddings para os trechos de texto
embeddings = gerar_embeddings(trechos)
print(f"Gerados {len(embeddings)} embeddings.")

# Criar cliente ChromaDB
cliente_chroma = chromadb.PersistentClient(
    path="./database/chroma_db", settings=Settings())

# Criar ou carregar coleção
colecao = cliente_chroma.get_or_create_collection("curso_software_engineering")

# Adicionar embeddings ao banco de dados vetorial
for i, (embedding, trecho) in enumerate(zip(embeddings, trechos)):
    colecao.add(
        ids=[str(i)],  # ID único para cada trecho
        embeddings=[embedding.tolist()],
        metadatas=[{"indice": i, "texto": trecho}]
    )

print("Embeddings armazenados no ChromaDB.")


def buscar_no_chroma(query, top_k=1):
    query_embedding = modelo_embedding.encode([query]).tolist()
    resultados = colecao.query(query_embedding, n_results=top_k)
    return resultados


# Exemplo de consulta
consulta = "O que faz o comando ps no Linux?"
resultados = buscar_no_chroma(consulta)

# for i, resultado in enumerate(resultados["metadatas"][0]):
#     print(f"🔹 Resultado {i+1}: {resultado['texto'][:300]}...\n")

contexto = "\n\n".join([r["texto"] for r in resultados["metadatas"][0]])
resposta = gerar_resposta_mistral(consulta, contexto)
print(f"\n💬 Resposta gerada:\n{resposta}")