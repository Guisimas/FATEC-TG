from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Nome do modelo Mistral na Hugging Face
MODEL_NAME = "mistralai/Mistral-7B-v0.1"

# Carregar o tokenizador
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Carregar o modelo na GPU (se disponível) ou na CPU
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"  # Isso já cuida da alocação em CPU/GPU
)

print("✅ Modelo Mistral carregado com sucesso!")

def generate_text(prompt):
    """Gera uma resposta baseada no prompt fornecido."""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=200,  pad_token_id=tokenizer.eos_token_id)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Teste do modelo
prompt = "Explique como funciona o gerenciamento de memória no Linux."
response = generate_text(prompt)
print("🖥️ Resposta do Mistral:", response)
