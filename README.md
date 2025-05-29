# Projeto Professor Virtual Inteligente

Este projeto é um sistema de perguntas e respostas sobre Linux, usando IA personalizada. Ele utiliza o modelo Mistral para gerar respostas baseadas em conteúdo específico carregado pelo usuário.

---

## Configuração

### 1. Gerar API Key do Mistral

Para utilizar o modelo Mistral, você precisa criar uma conta e gerar uma chave de API (API_KEY) no site oficial:

- Acesse: https://mistral.ai/
- Crie uma conta (caso não tenha)
- Gere sua API Key no painel de controle

### 2. Criar arquivo `.env`

Na raiz do projeto, crie um arquivo `.env` e adicione sua chave da seguinte forma:

```env
MISTRAL_API_KEY="sua_api_key_aqui"