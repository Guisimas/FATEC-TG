import spacy
import re
from sentence_transformers import SentenceTransformer
from app.chat.mistral import connect_mistral
from app.database.chroma_db.config import connect_chroma
from app.pdf.scraper import busca_sites
system_prompt = '''Você é um assistente especializado em Linux, voltado para ensino técnico de nível universitário.
Seu objetivo é responder perguntas sobre sistemas operacionais Linux de forma didática, clara e precisa, com base em livros, apostilas, manuais oficiais e experiências práticas.
Etapa de resposta:
**Tente responder com base no contexto fornecido (base de conhecimento local, como ChromaDB).**
Orientações:
- Explique conceitos com clareza.
- Use linguagem técnica acessível, com exemplos práticos e reais.
- Inclua comandos quando aplicável, formatados assim:
```bash
sudo systemctl restart ssh.
Se a pergunta não estiver relacionada ao contexto, simplesmente diga: 'Esse assunto não faz parte do que estou programado para responder.'''

# Carregar modelo de embedding e NLP
modelo_embedding = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2")
nlp = spacy.load("pt_core_news_sm")
MODEL = "mistral-large-latest"

# Conectar ao banco vetorial
conn_db = connect_chroma()
colecao = conn_db.get_collection("digitalTwin")

client = connect_mistral()


def extrair_termos_relevantes(query):
    """
    Extrai termos relevantes automaticamente da pergunta do usuário,
    incluindo comandos de terminal e termos lematizados.
    """
    doc = nlp(query.lower())
    termos = set()

    # Lematização com filtro de categorias gramaticais úteis
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        if token.pos_ in {"NOUN", "VERB", "PROPN", "ADV"}:
            termos.add(token.lemma_)

    # Entidades nomeadas reconhecidas
    for ent in doc.ents:
        termos.add(ent.text.lower())

    # Comandos de terminal mais comuns (você pode expandir essa lista)
    comandos_frequentes = {
        "ls", "cd", "chmod", "chown", "rm", "mkdir", "touch", "cat", "ps", "kill", "man",
        "top", "df", "du", "grep", "find", "sudo", "echo", "ping", "ifconfig", "tar", "scp"
    }

    # Captura palavras que podem ser comandos
    comandos_possiveis = re.findall(r'\b[a-zA-Z]{1,15}\b', query)
    termos.update(
        {cmd for cmd in comandos_possiveis if cmd in comandos_frequentes})

    return list(termos)


def buscar_no_chroma(query, top_k):
    query_embedding = modelo_embedding.encode([query]).tolist()
    resultados = colecao.query(query_embedding, n_results=top_k)
    return resultados


def gerar_resposta(query):
    termos = extrair_termos_relevantes(query)
    contexto = ""
    total_resultados = 0

    for termo in termos:
        resultados = buscar_no_chroma(termo, top_k=3)
        metadatas = resultados.get("metadatas", [])

        if metadatas and metadatas[0]:
            trecho = "\n\n".join([r["texto"] for r in metadatas[0]])
            contexto += f"\n\n### Contexto para '{termo}':\n{trecho}"
            total_resultados += 1

    if total_resultados == 0:
        print("Com base no que você perguntou, ainda não encontrei nenhuma correspondência na base que estou utilizando no momento.\nVou ampliar a busca em outras fontes para ver se encontramos algo mais relevante.")
        for termo in termos:
            busca_sites(termo)
            resultados = buscar_no_chroma(termo, top_k=3)
            metadatas = resultados.get("metadatas", [])
            if metadatas and metadatas[0]:
                trecho = "\n\n".join([r["texto"] for r in metadatas[0]])
                contexto += f"\n\n### Contexto para '{termo}':\n{trecho}"

    if not contexto.strip():
        contexto = "Nenhuma informação relevante foi encontrada para os termos pesquisados."

    resposta = gerar_resposta_mistral(query, contexto)
    return resposta


def gerar_resposta_mistral(pergunta: str, contexto: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                system_prompt
            )
        },
        {
            "role": "user",
            "content": f"Contexto:\n{contexto}\n\nPergunta:\n{pergunta}"
        }
    ]
    resposta = client.chat.complete(
        model=MODEL,
        messages=messages,
    )

    return resposta.choices[0].message.content
