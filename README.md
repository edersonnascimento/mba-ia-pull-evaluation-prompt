# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Este projeto demonstra o processo completo de engenharia de prompts:

1. **Pull de prompts** do LangSmith Prompt Hub
2. **Refatoração e otimização** com técnicas avançadas de Prompt Engineering
3. **Push dos prompts otimizados** de volta ao LangSmith
4. **Avaliação da qualidade** através de métricas customizadas
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas

## Tecnologias

- **Linguagem:** Python 3.10+
- **Framework:** LangChain 0.3.13
- **Plataforma de avaliação:** LangSmith
- **Formato de prompts:** YAML
- **Testes:** pytest

## Provedores de LLM

### OpenAI (Pago)

| Configuração | Valor |
|---|---|
| Modelo de resposta | `gpt-4o-mini` |
| Modelo de avaliação | `gpt-4o` |
| Custo estimado | ~$1-5 |

Crie sua API Key em: https://platform.openai.com/api-keys

### Google Gemini (Gratuito)

| Configuração | Valor |
|---|---|
| Modelo de resposta | `gemini-2.5-flash` |
| Modelo de avaliação | `gemini-2.5-flash` |
| Limite | 15 req/min, 1500 req/dia |

Crie sua API Key em: https://aistudio.google.com/app/apikey

## Como Executar

### 1. Pré-requisitos

- Python 3.10 ou superior
- Git
- Uma API Key do LangSmith
- Uma API Key da OpenAI ou Google Gemini

### 2. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd mba-ia-pull-evaluation-prompt
```

### 3. Configurar o Ambiente Python

Crie e ative um ambiente virtual:

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar (Linux/macOS)
source venv/bin/activate

# Ativar (Windows)
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo e preencha suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```bash
# LangSmith
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=sua_chave_aqui
LANGSMITH_PROJECT=seu_projeto
USERNAME_LANGSMITH_HUB=seu_username

# OpenAI (se usar OpenAI)
OPENAI_API_KEY=sua_chave_aqui

# Google Gemini (se usar Gemini)
GOOGLE_API_KEY=sua_chave_aqui

# Configuração do LLM (escolha um provedor)
LLM_PROVIDER=google
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash

# Ou para OpenAI:
# LLM_PROVIDER=openai
# LLM_MODEL=gpt-4o-mini
# EVAL_MODEL=gpt-4o
```

### 5. Executar o Projeto

Siga a ordem abaixo para completar o desafio:

#### Passo 1 — Pull dos Prompts

Baixe os prompts do LangSmith Hub para o ambiente local:

```bash
python src/pull_prompts.py
```

O prompt será salvo em `prompts/bug_to_user_story_v1.yml`.

#### Passo 2 — Otimizar o Prompt

Analise o prompt original e crie a versão otimizada em `prompts/bug_to_user_story_v2.yml` aplicando técnicas como:

- **Few-shot Learning** — exemplos claros de entrada/saída
- **Chain of Thought (CoT)** — instruir o modelo a "pensar passo a passo"
- **Role Prompting** — definir persona e contexto detalhado
- **Skeleton of Thought** — estruturar a resposta em etapas claras

O prompt otimizado deve conter:
- Instruções claras e específicas
- Regras explícitas de comportamento
- Exemplos de entrada/saída
- Tratamento de edge cases
- Separação adequada entre System e User Prompt

#### Passo 3 — Push dos Prompts Otimizados

Envie o prompt otimizado de volta ao LangSmith Hub:

```bash
python src/push_prompts.py
```

O prompt será publicado como público com o nome `{username}/bug_to_user_story_v2`.

#### Passo 4 — Avaliação

Execute a avaliação automática:

```bash
python src/evaluate.py
```

O script irá:
1. Carregar o dataset de avaliação
2. Criar/atualizar o dataset no LangSmith
3. Puxar o prompt otimizado do Hub
4. Executar o prompt contra os exemplos
5. Calcular as métricas
6. Exibir o resumo no terminal

#### Passo 5 — Iteração

Se as métricas não atingirem 0.9, itere:

1. Analise as métricas baixas e identifique problemas
2. Edite `prompts/bug_to_user_story_v2.yml`
3. Execute `python src/push_prompts.py`
4. Execute `python src/evaluate.py`
5. Repita até todas as métricas >= 0.9

#### Passo 6 — Testes de Validação

Execute os testes para validar a estrutura do prompt:

```bash
# Todos os testes
pytest tests/test_prompts.py

# Com saída detalhada
pytest tests/test_prompts.py -v

# Um teste específico
pytest tests/test_prompts.py::TestPrompts::test_prompt_has_system_prompt -v
```

Os 6 testes obrigatórios são:

| Teste | Verificação |
|---|---|
| `test_prompt_has_system_prompt` | Campo `system_prompt` existe e não está vazio |
| `test_prompt_has_role_definition` | Prompt define uma persona |
| `test_prompt_mentions_format` | Prompt exige formato Markdown ou User Story |
| `test_prompt_has_few_shot_examples` | Prompt contém exemplos de entrada/saída |
| `test_prompt_no_todos` | Não há marcadores `[TODO]` no texto |
| `test_minimum_techniques` | Pelo menos 2 técnicas listadas |

## Critério de Aprovação

Todas as 4 métricas devem atingir >= 0.9 individualmente:

| Métrica | Descrição | Mínimo |
|---|---|---|
| Tone Score | Tom profissional e empático | >= 0.9 |
| Acceptance Criteria Score | Qualidade dos critérios de aceitação | >= 0.9 |
| User Story Format Score | Formato correto (Como... Eu quero... Para que...) | >= 0.9 |
| Completeness Score | Completude e contexto técnico | >= 0.9 |

## Estrutura do Projeto

```
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Esta documentação
├── datasets/
│   └── bug_to_user_story.jsonl   # Dataset de avaliação (não modificar)
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt original (após pull)
│   └── bug_to_user_story_v2.yml  # Prompt otimizado (entregável)
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith Hub
│   ├── push_prompts.py       # Push ao LangSmith Hub
│   ├── evaluate.py           # Avaliação automática
│   ├── metrics.py            # Métricas customizadas
│   └── utils.py              # Funções auxiliares
└── tests/
    └── test_prompts.py       # Testes de validação
```

## Dicas

- Use **Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo
- Use o **Tracing do LangSmith** como ferramenta de debug — ele mostra exatamente o que o LLM está "pensando"
- É normal precisar de **3-5 iterações** para atingir 0.9 em todas as métricas
- **Não altere o dataset** de avaliação — apenas os prompts em `prompts/bug_to_user_story_v2.yml`
