from sentence_transformers import SentenceTransformer
import spacy
import math
import sys
import os
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'chroma_db')))

from ConfgChroma import connect_chroma

# Carregar o modelo spaCy para português
nlp = spacy.load("pt_core_news_sm")


def dividir_em_trechos(texto):
    doc = nlp(texto)
    palavras = [token.text for token in doc]

    # Convertendo tokens para palavras
    tamanho_trecho = math.ceil(200 / 0.75)
    trechos = [" ".join(palavras[i:i + tamanho_trecho])
               for i in range(0, len(palavras), tamanho_trecho)]

    return trechos


def processar_pasta_com_txt(pasta_txt):
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
        trechos.extend(dividir_em_trechos(texto))

        print(f"Arquivo {arquivo_txt} processado. {
              len(trechos)} trechos extraídos.")

    return trechos


def gerar_embeddings(trechos):
    return modelo_embedding.encode(trechos, convert_to_tensor=True)


# Caminho da pasta contendo os arquivos .txt
pasta_txt = "./database/coleta_pdf/extrair_txt/textos_extraidos"

# Processar os arquivos da pasta e dividir em trechos
trechos = processar_pasta_com_txt(pasta_txt)

print(f"Texto dividido em {len(trechos)} trechos.")


modelo_embedding = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2")

# Gerar embeddings para os trechos de texto
embeddings = gerar_embeddings(trechos)
print(f"Gerados {len(embeddings)} embeddings.")

# Conexão com o banco de dados
client = connect_chroma()
colecao = client.get_collection(name="digitalTwin")

# Adicionar embeddings ao banco de dados vetorial
for i, (embedding, trecho) in enumerate(zip(embeddings, trechos)):
    colecao.add(
        ids=[str(i)],  # ID único para cada trecho
        embeddings=[embedding.tolist()],
        metadatas=[{"indice": i, "texto": trecho}]
    )

print("Embeddings armazenados no ChromaDB.")

print(colecao.count())
