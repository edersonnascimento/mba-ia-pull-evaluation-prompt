# AGENTS.md — Guidelines for Agentic Coding Agents

## Project Overview

Python project for pulling, optimizing, and evaluating prompts using LangChain and LangSmith. Converts bug reports into well-structured User Stories and evaluates them against custom metrics (Tone, Acceptance Criteria, User Story Format, Completeness) targeting scores >= 0.9.

## Commands

### Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in API keys
```

### Run Scripts

```bash
python src/pull_prompts.py      # Pull prompts from LangSmith Hub
python src/push_prompts.py      # Push optimized prompts to LangSmith Hub
python src/evaluate.py          # Run evaluation against dataset
python src/metrics.py           # Test metric functions locally
```

### Testing

```bash
pytest tests/test_prompts.py         # Run all tests
pytest tests/test_prompts.py -v      # Verbose output
pytest tests/test_prompts.py -v --tb=short   # Verbose, short tracebacks
pytest tests/test_prompts.py::TestPrompts::test_prompt_has_system_prompt  # Run single test
pytest tests/test_prompts.py -k "role"   # Run tests matching keyword
```

## Code Style

### Imports

- Standard library imports first, then third-party, then local — separated by blank lines
- Use `from module import X` style (already used throughout codebase)
- Lazy imports inside functions for provider-specific packages (see `utils.py:get_llm`)
- `load_dotenv()` called at module level in scripts that need env vars

### Formatting

- 4-space indentation (no tabs)
- Single quotes for strings, double quotes for docstrings
- Maximum line length: follow existing code (~120 chars acceptable for long strings/prompts)
- Trailing commas in multi-line structures

### Type Hints

- Use `typing` module: `Dict`, `List`, `Any`, `Optional`, `Tuple`
- All function parameters and return types should be annotated
- Use `Optional[T]` for values that can be `None`
- Return tuples as `tuple[bool, list]` for validation results

### Naming Conventions

- **Files/modules:** `snake_case.py` (e.g., `pull_prompts.py`, `test_prompts.py`)
- **Functions:** `snake_case` (e.g., `load_dataset_from_jsonl`, `evaluate_f1_score`)
- **Classes:** `PascalCase` (e.g., `TestPrompts`)
- **Constants:** `UPPER_SNAKE_CASE` (none currently, but follow if added)
- **Test methods:** `test_` prefix with descriptive names (e.g., `test_prompt_has_system_prompt`)

### Error Handling

- Use `try/except` blocks with specific exception types (`FileNotFoundError`, `json.JSONDecodeError`, `yaml.YAMLError`)
- Catch bare `Exception` only as last resort, always log/print the error
- Return safe defaults on failure (e.g., `{"score": 0.0, "reasoning": "..."}` for metrics)
- Use `sys.exit(main())` pattern in scripts, return `0` for success, `1` for failure
- Validate environment variables early with `check_env_vars()` before proceeding

### Docstrings

- Triple-quoted docstrings for all public functions
- Include `Args:`, `Returns:`, and optionally `Raises:` sections
- Module-level docstrings describe the script's purpose and flow

### YAML Prompts

- Prompt files use `snake_case` keys (e.g., `system_prompt`, `techniques_applied`)
- Required fields: `description`, `system_prompt`, `version`, `tags`
- Use `|` for multi-line string values
- `techniques_applied` must list >= 2 techniques for validation to pass

### Testing

- Tests use `pytest` with class-based organization (`class TestPrompts`)
- Load YAML fixtures from `prompts/` directory
- Import from `src/utils.py` via `sys.path.insert` (project convention)
- All 6 required tests must pass: system_prompt, role_definition, format, few_shot, no_todos, minimum_techniques

### Environment Variables

- Never commit `.env` — use `.env.example` as template
- Required: `LANGSMITH_API_KEY`, `LLM_PROVIDER`
- Provider-specific: `OPENAI_API_KEY` or `GOOGLE_API_KEY`
- Models: `LLM_MODEL` (default: `gpt-4o-mini`), `EVAL_MODEL` (default: `gpt-4o`)

### Project Structure

```
├── datasets/bug_to_user_story.jsonl   # Evaluation dataset (do not modify)
├── prompts/
│   ├── bug_to_user_story_v1.yml       # Original prompt (from pull)
│   └── bug_to_user_story_v2.yml       # Optimized prompt (deliverable)
├── src/
│   ├── evaluate.py                    # Evaluation orchestration
│   ├── metrics.py                     # Custom metric implementations
│   ├── pull_prompts.py               # LangSmith pull script
│   ├── push_prompts.py               # LangSmith push script
│   └── utils.py                       # Shared utilities
└── tests/test_prompts.py             # Validation tests
```
