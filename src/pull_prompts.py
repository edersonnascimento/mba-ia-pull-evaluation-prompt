"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith() -> dict:
    """
    Faz pull dos prompts do LangSmith Hub.

    Conecta ao LangSmith usando credenciais do .env,
    faz pull de leonanluppi/bug_to_user_story_v1 e
    retorna os dados serializados.

    Returns:
        Dicionário com o prompt baixado

    Raises:
        ValueError: Se credenciais não estiverem configuradas
        Exception: Se falhar ao conectar ao LangSmith
    """
    print_section_header("Pull de Prompts", "-")

    required_vars = ['LANGSMITH_API_KEY', 'LANGSMITH_PROJECT']
    if not check_env_vars(required_vars):
        raise ValueError("Credenciais do LangSmith não configuradas!")

    from langsmith import Client

    client = Client()

    print("📥 Conectando ao LangSmith Hub...")

    prompt_slug = "leonanluppi/bug_to_user_story_v1"

    try:
        prompt_data = client.pull_repo(prompt_slug)
        print(f"✅ Prompt '{prompt_slug}' baixado com sucesso!")
        print(f"   Total de exemplos: {len(prompt_data)}")

        return prompt_data
    except Exception as e:
        print(f"❌ Falha ao baixar prompt: {e}")
        raise


def main():
    """Função principal"""
    try:
        prompt_data = pull_prompts_from_langsmith()

        output_file = "prompts/bug_to_user_story_v1.yml"
        save_yaml(prompt_data, output_file)

        print(f"\n✅ Prompt salvo em: {output_file}")
        print_section_header("Concluído", "-")
        return 0
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main())
