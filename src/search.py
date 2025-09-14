import os

from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

load_dotenv()


def search_prompt(question=None):
    """
    Realiza busca semântica no banco de dados vetorial

    Args:
        question (str): Pergunta do usuário

    Returns:
        list: Lista de tuplas (documento, score) com os resultados mais relevantes
    """
    if not question:
        return []

    for k in (
        "GOOGLE_API_KEY",
        "DATABASE_URL",
        "PG_VECTOR_COLLECTION_NAME",
    ):
        if not os.getenv(k):
            raise RuntimeError(f"Environment variable {k} is not set")

    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001").strip(
                "'\""
            ),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

        store = PGVector(
            embeddings=embeddings,
            collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
            connection=os.getenv("DATABASE_URL"),
            use_jsonb=True,
        )

        # Realizar busca por similaridade
        results = store.similarity_search_with_score(question, k=10)

        return results

    except Exception as e:
        print(f"Erro na busca semântica: {e}")
        return []
