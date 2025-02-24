# modules/config.py
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


def load_config():
    """Carrega e retorna uma instância do modelo de linguagem configurada com a chave da API."""
    # Carrega as variáveis de ambiente
    load_dotenv()

    # Obtém a chave da API do ambiente
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("A chave da API para OpenAI não foi encontrada.")

    # Cria uma instância do modelo de linguagem
    llm = ChatOpenAI(
        model_name="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key
    )
    return llm
