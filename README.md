# Data Project Starter Kit

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue.svg)](https://filipimr.github.io/Data-Project-Starter-Kit/)

Template padronizado para começar projetos de **engenharia, ciência e
análise de dados**, ETL, pipelines de ML, APIs, dashboards, já com
ambiente reprodutível, código modular, testes, padrão de lint/formatação,
documentação viva e automação de fluxo (pre-commit + CI) prontos.

A meta é simples: **qualquer pessoa consegue clonar, instalar e rodar em
minutos**, sem depender de "na minha máquina funciona".

Vale a leitura do [Guia de boas práticas](docs/guia/index.md) para
entender o *porquê* de cada prática — o que é, por que importa e como fazer
com uv/Ruff, com links para a documentação oficial de cada ferramenta
citada.

## Como usar este template

1. No GitHub, clique em **"Use this template"** para criar seu próprio
   repositório a partir deste (ou dê `git clone` se preferir só copiar
   localmente).
2. Instale as dependências e os hooks do pre-commit:

   ```bash
   uv sync
   uv run pre-commit install
   ```

3. Inicialize o seu projeto de dados executando o script de bootstrap interativo:

   ```bash
   uv run task init
   ```

   *Esse comando solicitará o nome, a descrição e o autor do seu projeto, atualizará automaticamente os arquivos `pyproject.toml` e `mkdocs.yml`, removerá todos os guias explicativos de documentação e deixará a estrutura limpa e pronta para uso (ready-to-go).*

4. Configure sua IDE (VS Code, Antigravity, Cursor, PyCharm, etc.) para utilizar o interpretador Python da pasta `.venv` criada na raiz do projeto. Veja o detalhamento no [Passo 5 do Guia de boas práticas](docs/guia/fundacao.md#passo-5-integracao-e-configuracao-da-ide).
5. Substitua os `TODO` em `app/pipeline/extract.py`, `transform.py` e
   `load.py` pela lógica real do seu projeto, e remova os
   `pytest.skip(...)` correspondentes em `tests/` conforme for
   implementando.

Veja [`docs/ia-como-acelerador.md`](docs/ia-como-acelerador.md) para prompts
prontos de como usar o Claude Code em cada um desses passos.

## Estrutura de pastas

```text
app/                 # todo o código do projeto vive aqui
├── main.py          # ponto de entrada: orquestra o pipeline
└── pipeline/         # extract / transform / load
tests/               # testes automatizados (pytest), espelhando app/
docs/                 # site MkDocs (gerado a partir das docstrings)
data/                 # dados de exemplo — input/ e output/, gitignored
.github/              # workflow de CI e template de Pull Request
.agents/skills/        # skills de IA reutilizáveis (ver .agents/skills/README.md)
```

Detalhes de cada pasta em [`docs/estrutura.md`](docs/estrutura.md).

## Stack

| Necessidade                  | Ferramenta                                   |
| ----------------------------- | --------------------------------------------- |
| Versão do Python + ambiente   | [uv](https://docs.astral.sh/uv/)              |
| Testes                        | [pytest](https://docs.pytest.org/) (padrão Arrange-Act-Assert) |
| Lint + formatação             | [Ruff](https://docs.astral.sh/ruff/)          |
| Atalhos de tarefa             | [taskipy](https://github.com/taskipy/taskipy) |
| Documentação                  | [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) + [mkdocstrings](https://mkdocstrings.github.io/) |
| Hooks de pre-commit           | [pre-commit](https://pre-commit.com/) (ruff-check, ruff-format, uv-lock) |
| Integração contínua           | [GitHub Actions](https://docs.github.com/en/actions) |

## Comandos do dia a dia

```bash
uv sync                  # instala tudo a partir do uv.lock
uv run task init         # inicializa o projeto limpando as explicações
uv run task format       # ruff check --fix . && ruff format .
uv run task lint         # ruff check . && ruff format --check .
uv run task test         # pytest -v
uv run task docs         # mkdocs serve (site local em http://127.0.0.1:8000)
```

Rodar um teste específico: `uv run pytest tests/test_transform.py -k nome_do_teste`.

## IA como acelerador

Este template foi desenhado para ser usado com o
[Claude Code](https://docs.claude.com/en/docs/claude-code/overview). O arquivo
[`CLAUDE.md`](CLAUDE.md) na raiz registra as convenções do projeto (uv,
Ruff, pytest, padrão de commit, "nunca use `--no-verify`"), e
[`docs/ia-como-acelerador.md`](docs/ia-como-acelerador.md) traz prompts
prontos para avançar em cada etapa. Regra de ouro: peça mudanças pequenas e
revisáveis — uma prática por PR — e sempre revise o diff.

`.agents/skills/` guarda skills reutilizáveis (guias operacionais mais
longos que um prompt). Use o template em
[`.agents/skills/_template/SKILL.md`](.agents/skills/_template/SKILL.md)
para criar uma nova, ou busque uma pronta em
[skillsmp.com](https://skillsmp.com/) antes de escrever do zero — veja
[`.agents/skills/README.md`](.agents/skills/README.md) para as boas
práticas.

## Checklist de adoção

Use como referência rápida do que este template já cobre:

- [x] Versão do Python travada (`.python-version`, via uv)
- [x] Ambiente e dependências reprodutíveis (`pyproject.toml` + `uv.lock`)
- [x] Repositório Git com `.gitignore` e histórico de commits pequenos
- [x] `CLAUDE.md` com as convenções do projeto
- [x] Estrutura de pastas: `app/`, `tests/`, `docs/`, `data/`
- [x] Pipeline modularizado (extract/transform/load) com docstrings e type hints
- [x] Testes com pytest, padrão Arrange-Act-Assert
- [x] Padrão de código com Ruff (lint + format)
- [x] Atalhos de tarefa (taskipy): `task format`, `task lint`, `task test`, `task init`
- [x] Documentação em MkDocs (Material + mkdocstrings)
- [x] Pre-commit hooks (ruff-check, ruff-format, uv-lock)
- [x] CI no GitHub Actions (setup-uv + ruff + pytest)
- [x] Template de Pull Request com checklist de revisão
- [ ] Lógica real de `extract`/`transform`/`load` (os `TODO` são seus)

## Licença

[MIT](LICENSE).

---
Desenvolvido para a comunidade de engenharia de dados.


