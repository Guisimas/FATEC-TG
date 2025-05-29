# chat_mistral.py
import os
from dotenv import load_dotenv
from mistralai import Mistral


load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=API_KEY)

# Modelo disponível (pode ser: mistral-tiny, mistral-small, mistral-medium, mistral-large-latest)
MODEL = "mistral-large-latest"

def gerar_resposta_mistral(pergunta: str, contexto: str) -> str:
    messages = [
        {"role": "system", "content": (
    "Você é um professor virtual especializado em Sistemas Operacionais, com foco em Linux. "
    "Responda apenas perguntas relacionadas a esse assunto. "
    "Se a pergunta for fora desse tema, diga que não pode responder."
)},
        {"role": "user", "content": f"Contexto:\n{contexto}\n\nPergunta:\n{pergunta}"}
    ]

    resposta = client.chat.complete(
        model=MODEL,
        messages=messages,
    )

    return resposta.choices[0].message.content
