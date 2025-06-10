from sentence_transformers import SentenceTransformer
import spacy
import math
import os
import shutil
from app.database.chroma_db.config import connect_chroma

# Carregar modelo SpaCy
nlp = spacy.load("pt_core_news_sm")

# Carregar modelo de embedding
modelo_embedding = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2")


# ------------------------------------
# Dividir texto em trechos
# ------------------------------------
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
                sub_par = par[i:i + 1000000]
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


# -----------------------------------
# Processar pasta com os arquivos TXT
# -----------------------------------
def processar_pasta_com_txt(pasta_txt, tokens_por_trecho):
    todos_trechos = []
    origem_trechos = []
    trecho_num_por_arquivo = []

    arquivos_txt = [f for f in os.listdir(pasta_txt) if f.endswith(".txt")]

    for arquivo_txt in arquivos_txt:
        caminho_arquivo = os.path.join(pasta_txt, arquivo_txt)
        with open(caminho_arquivo, "r", encoding="utf-8") as file:
            texto = file.read()

        trechos_arquivo = dividir_em_trechos(texto, tokens_por_trecho)
        todos_trechos.extend(trechos_arquivo)
        origem_trechos.extend([arquivo_txt] * len(trechos_arquivo))
        trecho_num_por_arquivo.extend(list(range(len(trechos_arquivo))))

        print(
            f"Arquivo {arquivo_txt} processado. {len(trechos_arquivo)} trechos extraídos.")

    return todos_trechos, origem_trechos, trecho_num_por_arquivo


# -----------------
# Gerar embeddings
# -----------------
def gerar_embeddings(trechos):
    return modelo_embedding.encode(trechos, convert_to_tensor=True)


# -------------------------
# Função principal: token()
# -------------------------
def token():
    # Configurações
    pasta_txt = "./app/pdf/textos_extraidos"
    tokens_por_trecho = 200

    # Processamento
    trechos, origens, trechos_num = processar_pasta_com_txt(
        pasta_txt, tokens_por_trecho)
    embeddings = gerar_embeddings(trechos)
    print(f"Gerados {len(embeddings)} embeddings.")

    # Conexão com o banco ChromaDB
    client = connect_chroma()
    colecao = client.get_or_create_collection(name="digitalTwin")

    # Armazenar embeddings com metadados completos
    for i, (embedding, trecho, arquivo_origem, trecho_num) in enumerate(zip(embeddings, trechos, origens, trechos_num)):
        colecao.add(
            ids=[str(i)],
            embeddings=[embedding.tolist()],
            metadatas=[{
                "indice_global": i,
                "texto": trecho,
                "arquivo_origem": arquivo_origem,
                "trecho_num": trecho_num
            }]
        )

    print("Embeddings armazenados no ChromaDB.")
    print(f"Total de documentos na coleção: {colecao.count()}")

    # Mover os arquivos processados para a pasta "complet"
    pasta_destino = "./app/pdf/textos_extraidos/completo"
    os.makedirs(pasta_destino, exist_ok=True)

    arquivos_processados = [f for f in os.listdir(
        pasta_txt) if f.endswith(".txt")]
    for arquivo in arquivos_processados:
        caminho_origem = os.path.join(pasta_txt, arquivo)
        caminho_destino = os.path.join(pasta_destino, arquivo)
        shutil.move(caminho_origem, caminho_destino)
