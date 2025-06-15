from fastapi import FastAPI
from pydantic import BaseModel
from pipeline.process import gerar_resposta  # seu módulo que tem gerar_resposta

app = FastAPI()


class Pergunta(BaseModel):
    pergunta: str


@app.post("/pergunta/")
def responder(pergunta: Pergunta):
    resposta = gerar_resposta(pergunta.pergunta)
    return {"resposta": resposta}
