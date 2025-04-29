# chat_mistral.py
import os
from mistralai import Mistral

# Certifique-se de definir a variável de ambiente 'MISTRAL_API_KEY' ou coloque a chave direto
client = Mistral(api_key="da6NnTH1RXeu77gxjvNjrgKLAxHqX4sQ")  # ou: Mistral(api_key="sua-chave-aqui")

# Modelo disponível (pode ser: mistral-tiny, mistral-small, mistral-medium, mistral-large-latest)
MODEL = "mistral-large-latest"

def gerar_resposta_mistral(pergunta: str, contexto: str) -> str:
    messages = [
        {"role": "system", "content": "Você é um assistente que responde com base no contexto fornecido."},
        {"role": "user", "content": f"Contexto:\n{contexto}\n\nPergunta:\n{pergunta}"}
    ]

    resposta = client.chat.complete(
        model=MODEL,
        messages=messages,
    )

    return resposta.choices[0].message.content
