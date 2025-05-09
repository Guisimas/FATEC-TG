from pipeline import gerar_resposta

def main():
    print("\nProfessor Virtual IA - Ensino de Linux (Local)")
    while True:
        query = input("\nDigite sua pergunta (ou 'sair'): ")
        if query.lower() in ["sair", "exit", "quit"]:
            break
        resposta = gerar_resposta(query)
        print("\nResposta:\n", resposta)

if __name__ == "__main__":
    main()