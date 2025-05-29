import gradio as gr
import shutil
from pipeline import gerar_resposta, adicionar_novo_texto, adicionar_novo_pdf

# ✅ Função de pergunta
def responder(pergunta):
    if not pergunta.strip():
        return "Digite uma pergunta válida."
    return gerar_resposta(pergunta)

# ✅ Função para adicionar texto manualmente
def treinar_texto(texto):
    if not texto.strip():
        return "Digite um texto válido para treinar."
    adicionar_novo_texto(texto)
    return "✅ Texto adicionado com sucesso ao banco vetorial."

# ✅ Função para upload de PDF
def upload_pdf(arquivo):
    if arquivo is None:
        return "⚠️ Nenhum arquivo enviado."

    destino = r"C:\Developer\tcc\FATEC-TG\database\coleta_pdf\extrair_txt\textos_incrementais"
    caminho_destino = shutil.copy(arquivo.name, destino)
    return f"✅ Arquivo {arquivo.name} enviado com sucesso para {destino}."

# ✅ Função para processar os PDFs adicionados
def processar_pdfs():
    adicionar_novo_pdf(tokens_por_trecho=200)
    return "✅ PDFs processados e adicionados ao banco vetorial."

# ✅ Interface de Perguntas
pergunta_interface = gr.Interface(
    fn=responder,
    inputs=gr.Textbox(label="Digite sua pergunta sobre Linux", placeholder="Ex: O que faz o comando 'chmod'?"),
    outputs=gr.Textbox(label="Resposta do Professor Virtual"),
    title="🧠 Professor Virtual Inteligente",
    description="Faça perguntas sobre Linux e receba respostas geradas por uma IA treinada com conteúdo específico.",
    theme="soft",
    allow_flagging="never"
)

# ✅ Interface de Treinamento
treinamento_interface = gr.Interface(
    fn=treinar_texto,
    inputs=gr.Textbox(label="Insira um texto para treinar a IA", lines=5, placeholder="Digite aqui o conteúdo..."),
    outputs=gr.Textbox(label="Status"),
    theme="soft",
    allow_flagging="never"
)

# ✅ Interface de Upload PDF
upload_interface = gr.Interface(
    fn=upload_pdf,
    inputs=gr.File(label="Envie um arquivo PDF"),
    outputs=gr.Textbox(label="Status do upload"),
    theme="soft",
    allow_flagging="never"
)

# ✅ Interface de Processamento
processamento_interface = gr.Interface(
    fn=processar_pdfs,
    inputs=[],
    outputs=gr.Textbox(label="Status do processamento"),
    theme="soft",
    allow_flagging="never"
)

# ✅ Tabs organizadas
interface = gr.TabbedInterface(
    interface_list=[
        pergunta_interface,
        treinamento_interface,
        upload_interface,
        processamento_interface
    ],
    tab_names=["Perguntar", "Treinar com Texto", "Upload de PDF", "Processar PDFs"]
)

if __name__ == "__main__":
    interface.launch()
