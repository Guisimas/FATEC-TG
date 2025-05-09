import gradio as gr
from pipeline import gerar_resposta

def responder(pergunta):
    if not pergunta.strip():
        return "Digite uma pergunta válida."
    
    return gerar_resposta(pergunta)

interface = gr.Interface(
    fn=responder,
    inputs=gr.Textbox(label="Digite sua pergunta sobre Linux", placeholder="Ex: O que faz o comando 'chmod'?"),
    outputs=gr.Textbox(label="Resposta do Professor Virtual"),
    title="🧠 Professor Virtual Inteligente",
    description="Faça perguntas sobre Linux e receba respostas geradas por uma IA treinada com conteúdo específico.",
    theme="soft",
    allow_flagging="never"
)

if __name__ == "__main__":
    interface.launch()
