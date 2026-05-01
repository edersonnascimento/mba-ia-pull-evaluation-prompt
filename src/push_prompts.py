"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt no formato '{username}/{prompt_name}'
        prompt_data: Dados do prompt com system_prompt, user_prompt, etc.

    Returns:
        True se sucesso, False caso contrário
    """
    from langchain import hub
    from langchain_core.prompts import ChatPromptTemplate

    print(f"📤 Fazendo push do prompt '{prompt_name}'...")

    try:
        # Criar ChatPromptTemplate a partir dos dados YAML
        messages = [
            ("system", prompt_data.get('system_prompt', '')),
            ("human", prompt_data.get('user_prompt', '{input}'))
        ]
        prompt_template = ChatPromptTemplate.from_messages(messages)

        # Push para o Hub como público
        repo_url = hub.push(prompt_template, name=prompt_name, public=True)

        print(f"✅ Prompt publicado com sucesso!")
        print(f"   URL: {repo_url}")
        return True

    except Exception as e:
        print(f"❌ Falha ao publicar prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt.

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    # Verificar campos obrigatórios
    required_fields = ['description', 'system_prompt']
    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: {field}")

    # Verificar se system_prompt não está vazio
    system_prompt = prompt_data.get('system_prompt', '').strip()
    if not system_prompt:
        errors.append("system_prompt está vazio")

    # Verificar se não tem TODOs
    if 'TODO' in system_prompt:
        errors.append("system_prompt contém TODOs não implementados")

    # Verificar técnicas aplicadas (mínimo 2)
    techniques = prompt_data.get('techniques_applied', [])
    if len(techniques) < 2:
        errors.append(f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}")

    # Verificar se há exemplos few-shot
    examples = prompt_data.get('examples', [])
    if len(examples) < 1:
        errors.append("Pelo menos 1 exemplo few-shot é recomendado")

    is_valid = len(errors) == 0
    return (is_valid, errors)


def main():
    """Função principal"""
    try:
        print_section_header("Push de Prompts Otimizados", "=")

        required_vars = ['LANGSMITH_API_KEY', 'LANGSMITH_PROJECT', 'USERNAME_LANGSMITH_HUB']
        if not check_env_vars(required_vars):
            raise ValueError("Credenciais do LangSmith não configuradas!")

        # Carregar prompt otimizado
        prompt_file = "prompts/bug_to_user_story_v2.yml"
        prompt_data = load_yaml(prompt_file)

        if prompt_data is None:
            raise FileNotFoundError(f"Prompt não encontrado: {prompt_file}")

        # Validar prompt
        print("🔍 Validando prompt...")
        is_valid, errors = validate_prompt(prompt_data)

        if not is_valid:
            print("❌ Validação falhou:")
            for error in errors:
                print(f"   - {error}")
            return 1

        print("✅ Prompt válido!")

        # Obter username do .env
        username = os.getenv('USERNAME_LANGSMITH_HUB')
        prompt_name = f"{username}/bug_to_user_story_v2"

        # Fazer push
        success = push_prompt_to_langsmith(prompt_name, prompt_data)

        if success:
            print_section_header("Push Concluído", "=")
            print("✅ Prompt otimizado publicado no LangSmith Hub!")
            return 0
        else:
            return 1

    except FileNotFoundError as e:
        print(f"\n❌ Arquivo não encontrado: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

