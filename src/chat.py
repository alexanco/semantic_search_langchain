import os

from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from search import PROMPT_TEMPLATE, search_prompt

load_dotenv()


def create_chat_chain():
    """Cria o chain do chat com modelo e prompt"""

    try:
        # Inicializar o modelo de chat do Google
        chat_model = ChatGoogleGenerativeAI(
            model=os.getenv("gemini-2.5-flash-lite", "gemini-2.5-flash-lite").strip(
                "'\""
            ),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0,
        )

        # Criar o template do prompt
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        # Criar o chain
        chain = prompt | chat_model

        return chain
    except Exception as e:
        print(f"❌ Erro ao criar o chat: {e}")
        return None


def format_search_results(results):
    """Formata os resultados da busca semântica para usar como contexto"""
    if not results:
        return "Nenhum contexto encontrado."

    contexto_parts = []
    for i, (doc, score) in enumerate(results, start=1):
        contexto_parts.append(f"Documento {i} (relevância: {score:.2f}):")
        contexto_parts.append(doc.page_content.strip())
        contexto_parts.append("")  # linha em branco

    return "\n".join(contexto_parts)


def main():
    print("🤖 Chat RAG - Sistema de Busca Semântica")
    print("=" * 50)
    print("Digite suas perguntas sobre o documento carregado.")
    print("Comandos: 'sair', 'exit', 'quit' para encerrar")
    print("=" * 50)

    # Criar o chain do chat
    chat_chain = create_chat_chain()

    if not chat_chain:
        print("❌ Não foi possível inicializar o sistema de chat.")
        return

    print("✅ Sistema inicializado com sucesso!")
    print()

    while True:
        try:
            # Receber pergunta do usuário
            user_question = input("🧑 Você: ").strip()

            # Verificar comandos de saída
            if user_question.lower() in ["sair", "exit", "quit", ""]:
                print("👋 Obrigado por usar o chat! Até logo!")
                break

            print("🔍 Buscando informações relevantes...")

            # Realizar busca semântica
            search_results = search_prompt(user_question)

            if not search_results:
                print("🤖 Bot: Não encontrei informações relevantes para sua pergunta.")
                continue

            # Formatar contexto
            contexto = format_search_results(search_results)

            print("💭 Gerando resposta...")

            # Gerar resposta usando o chat chain
            response = chat_chain.invoke(
                {"contexto": contexto, "pergunta": user_question}
            )

            # Exibir resposta
            print(f"🤖 Bot: {response.content}")
            print()

        except KeyboardInterrupt:
            print("\n👋 Chat interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            print("Tente novamente ou digite 'sair' para encerrar.")
            print()


if __name__ == "__main__":
    main()
