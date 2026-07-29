# Checklist final do projeto

Use este checklist como referência rápida para auditar o projeto. O objetivo continua sendo um só: **outra pessoa clona, instala, testa e roda o seu projeto sem precisar te chamar.**

## Fundação

- [ ] **Versão do Python:** travada com uv no arquivo `.python-version`.
- [ ] **Ambiente e dependências:** declaradas com uv no `pyproject.toml` e no `uv.lock`.
- [ ] **Controle de versão:** repositório Git limpo com `.gitignore` configurado.
- [ ] **README.md:** mapa básico explicando o propósito do projeto e como executá-lo do zero.
- [ ] **CLAUDE.md:** convenções do projeto descritas de forma clara para agentes de IA (uv, ruff, pytest, etc.).
- [ ] **Estrutura de pastas:** padronizada com `app/` (código), `tests/` (testes), `docs/` (docs), e `data/` (dados locais e ignorados).

## Código profissional

- [ ] **Modularização:** lógica quebrada em funções pequenas e módulos com responsabilidade única (ex. extract, transform, load).
- [ ] **Docstrings e type hints:** assinaturas bem-definidas em todas as funções públicas (estilo Google preferencial).
- [ ] **Estrutura de pacotes:** presença de arquivos `__init__.py` e uso correto do `if __name__ == "__main__"` nos scripts principais.

## Garantia de qualidade

- [ ] **Testes automatizados:** cobertura via `pytest` no padrão *Arrange-Act-Assert*.
- [ ] **Regressão:** a cada bug corrigido, um teste de regressão correspondente é criado.
- [ ] **Padrão de código:** estilo e qualidade garantidos pelo `Ruff` (linter + formatador) configurado no `pyproject.toml`.
- [ ] **Atalhos de tarefas:** comandos do dia a dia simplificados via `taskipy` (`task format`, `task lint`, `task test`).

## Documentação e fluxo

- [ ] **Site de documentação:** configurado com MkDocs (tema Material, mkdocstrings, Mermaid) e publicável via `gh-deploy`.
- [ ] **Pre-commit hooks:** instalados e configurados no `.pre-commit-config.yaml` (`ruff-check`, `ruff-format`, `uv-lock`).
- [ ] **CI (Integração Contínua):** pipeline no GitHub Actions configurada para rodar testes e linters a cada push/PR.
- [ ] **Revisão:** revisões humanas de código obrigatórias e PRs curtos/atômicos.

---

> Estrutura não é burocracia — é o que permite errar com segurança e criar sem medo.
