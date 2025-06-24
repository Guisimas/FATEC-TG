from fastapi import FastAPI
from pydantic import BaseModel
from pipeline.process import gerar_resposta  # seu módulo que tem gerar_resposta
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Pergunta(BaseModel):
    pergunta: str


@app.post("/pergunta/")
def responder(pergunta: Pergunta):
    resposta = gerar_resposta(pergunta.pergunta)
    return {"resposta": resposta}
