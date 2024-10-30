# Importa as bibliotecas necessárias
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_community.document_loaders import PyPDFLoader  # Para carregar arquivos PDF
from langchain.text_splitter import CharacterTextSplitter  # Para dividir texto em partes menores
from langchain_huggingface import HuggingFaceEmbeddings  # Para gerar embeddings de texto
from langchain_community.vectorstores import Chroma  # Para armazenar e recuperar embeddings de texto
from langchain.chains import ConversationalRetrievalChain  # Para criar uma cadeia de perguntas e respostas
import sys  # Importa a biblioteca sys para manipulação do sistema

# Carrega o modelo e o tokenizador do Hugging Face
token = "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"  # Substitua pelo seu token de autenticação
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1", token=token)
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1", token=token)

# Carrega o arquivo PDF e divide em partes menores
loader = PyPDFLoader('report.pdf')  # Carrega o documento PDF especificado
documents = loader.load()  # Carrega o conteúdo do PDF como documentos

# Divide os documentos em partes menores
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)  # Configura o divisor de texto
texts = text_splitter.split_documents(documents)  # Divide o documento carregado em partes menores

# Usaremos embeddings do HuggingFace
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # Inicializa a geração de embeddings usando HuggingFace

# Usando o banco de dados Chroma para armazenar e recuperar os embeddings do nosso texto
db = Chroma.from_documents(texts, embeddings)  # Cria um banco de dados a partir dos textos e embeddings
retriever = db.as_retriever(search_kwargs={'k': 2})  # Configura o recuperador para buscar os 2 documentos mais relevantes

# Configura a Cadeia de Recuperação de Conversação
qa_chain = ConversationalRetrievalChain.from_llm(model, retriever, return_source_documents=True)

# Executa um loop para perguntar ao modelo e recuperar respostas até que o usuário queira sair
chat_history = []  # Inicializa uma lista para manter o histórico de conversas
while True:  # Inicia um loop infinito
    query = input('Prompt: ')  # Solicita que o usuário insira uma pergunta
    # Para sair: use 'exit', 'quit', 'q', ou Ctrl-D.
    if query.lower() in ["exit", "quit", "q"]:  # Verifica se o usuário deseja sair
        print('Exiting')  # Informa que o programa está saindo
        sys.exit()  # Sai do programa

    # Gera a resposta
    input_text = ' '.join([f'User: {q[0]}\nBot: {q[1]}' for q in chat_history]) + f" User: {query} Bot:"
    inputs = tokenizer(input_text, return_tensors='pt', truncation=True, max_length=1024)

    # Gera a resposta com pad_token_id
    outputs = model.generate(**inputs, max_length=150, pad_token_id=tokenizer.eos_token_id)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print('Answer: ' + answer + '\n')  # Exibe a resposta recebida
    chat_history.append((query, answer))  # Adiciona a pergunta e a resposta ao histórico de conversas
