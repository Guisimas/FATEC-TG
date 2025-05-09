from pipeline import gerar_resposta

def iniciar_interface():
    print("=" * 60)
    print("🎓 Professor Virtual Inteligente - Ensino de Linux com IA")
    print("Digite sua pergunta ou 'sair' para encerrar.")
    print("=" * 60)

    while True:
        pergunta = input("\n❓ Você: ")
        if pergunta.lower().strip() in ["sair", "exit", "quit"]:
            print("👋 Encerrando. Até logo!")
            break

        print("💭 Processando...\n")
        resposta = gerar_resposta(pergunta)
        print(f"🤖 Professor: {resposta}")

if __name__ == "__main__":
    iniciar_interface()
