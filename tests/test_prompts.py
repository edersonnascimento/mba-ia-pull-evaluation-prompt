"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt_v2 = prompts.get("bug_to_user_story_v2", {})

        assert "system_prompt" in prompt_v2, "Campo system_prompt não existe"
        assert prompt_v2["system_prompt"].strip(), "system_prompt está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt_v2 = prompts.get("bug_to_user_story_v2", {})
        system_prompt = prompt_v2.get("system_prompt", "").lower()

        role_keywords = ["você é", "product manager", "developer", "analyst", "role"]
        has_role = any(keyword in system_prompt for keyword in role_keywords)

        assert has_role, "Prompt não define uma persona/role clara"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt_v2 = prompts.get("bug_to_user_story_v2", {})
        prompt_text = (prompt_v2.get("system_prompt", "") +
                       prompt_v2.get("user_prompt", "")).lower()

        format_keywords = ["markdown", "user story", "as a", "format", "structured", "as a...i want...so that"]
        has_format = any(keyword in prompt_text for keyword in format_keywords)

        assert has_format, "Prompt não especifica formato de saída (Markdown ou User Story)"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt_v2 = prompts.get("bug_to_user_story_v2", {})
        system_prompt = prompt_v2.get("system_prompt", "")

        examples = prompt_v2.get("examples", [])
        has_examples = len(examples) > 0

        has_inline_examples = "exemplo" in system_prompt.lower() or "example" in system_prompt.lower()

        assert has_examples or has_inline_examples, "Prompt não contém exemplos few-shot"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt_v2 = prompts.get("bug_to_user_story_v2", {})

        system_prompt = prompt_v2.get("system_prompt", "")
        user_prompt = prompt_v2.get("user_prompt", "")

        full_text = system_prompt + user_prompt

        assert "[TODO]" not in full_text, "Prompt contém [TODO] não implementado"
        assert "[todo]" not in full_text.lower(), "Prompt contém [todo] não implementado"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        prompt_v2 = prompts.get("bug_to_user_story_v2", {})

        techniques = prompt_v2.get("techniques_applied", [])

        assert isinstance(techniques, list), "techniques_applied deve ser uma lista"
        assert len(techniques) >= 2, f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])