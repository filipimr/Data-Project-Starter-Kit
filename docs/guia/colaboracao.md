# Bloco 5 — Fluxo e colaboração

Os últimos passos automatizam a qualidade no fluxo de trabalho, para que
código ruim simplesmente não chegue à produção.

## Passo 12 — Pre-commit hooks

**O que é.** Um hook de [pre-commit](https://pre-commit.com/) roda antes de
cada commit. Se as verificações falharem, o commit é bloqueado.

**Como fazer.**

```bash
uv add --dev pre-commit
uv run pre-commit install     # instala o hook no git
uv run pre-commit run --all-files
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.16.0
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/astral-sh/uv-pre-commit
    rev: 0.11.33
    hooks:
      - id: uv-lock
```

!!! warning "Escape (com parcimônia)"
    Dá para pular os hooks num aperto com `git commit --no-verify`. Existe
    a saída, mas o objetivo é justamente não subir código fora do padrão.
    Use só em emergência.

!!! tip "Com o Claude Code"
    Peça: «adicione o `.pre-commit-config.yaml` com ruff-check,
    ruff-format e uv-lock e rode `pre-commit install`». Detalhe
    importante: agentes de IA tendem a recorrer ao `--no-verify` mais do
    que humanos. Deixe explícito no `CLAUDE.md` — «nunca use
    `git commit --no-verify`; corrija o que o hook apontar».

## Passo 13 — Integração Contínua (CI) com GitHub Actions

**O que é.** Enquanto o pre-commit roda na sua máquina, a
[CI](https://docs.github.com/en/actions) roda no servidor. A cada push ou
Pull Request, o GitHub sobe uma máquina limpa, instala tudo do zero e roda
seus testes.

**Por que importa.** É a garantia de que o projeto roda numa máquina que
não é a sua — expondo qualquer dependência esquecida. Regra de ouro: a
cada bug corrigido, cria-se um teste unitário para ele.

**Como fazer.** Com [`astral-sh/setup-uv`](https://github.com/astral-sh/setup-uv),
a CI fica rápida: instala Python e dependências e cacheia tudo.

```yaml
# .github/workflows/ci.yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v8
        with:
          python-version: "3.13"
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run pytest
```

!!! tip "Com o Claude Code"
    Peça: «crie o workflow de CI no GitHub Actions com setup-uv, uv sync,
    ruff check e pytest». Ele escreve o YAML; você valida abrindo um PR de
    teste e vendo o check rodar verde.

## Passo 14 — Pull Requests e revisão de código

O [Pull Request (PR)](https://docs.github.com/en/pull-requests) é o
mecanismo de trazer código de uma branch para a principal com revisão. A CI
roda automaticamente nele.

!!! note "O que a CI não faz"
    Ela não substitui a revisão humana. O que ela faz é garantir que o
    código só chegue ao revisor já tendo passado no básico — estilo,
    testes, docstrings.

O passo seguinte natural é o CD (Continuous Delivery/Deployment) —
automatizar a publicação quando o código passa. Foge do escopo deste guia,
mas é a continuação lógica da CI.

!!! tip "Com o Claude Code"
    Peça: «abra um PR com título e descrição resumindo estas mudanças». O
    Claude Code cria o PR pelo `gh` e a CI roda sozinha nele. A revisão
    humana continua sendo sua — o agente acelera, não substitui.
