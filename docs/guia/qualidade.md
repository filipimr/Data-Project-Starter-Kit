# Bloco 3 — Garantia de qualidade

Aqui o projeto ganha rede de segurança. Testes, padrões de código e
automação de tarefas são o que permitem mexer no código sem medo.

## Passo 8 — Testes automatizados com pytest

**O que é.** Um teste é um código que verifica se outro código faz o que
deveria. O [pytest](https://docs.pytest.org/) é a biblioteca mais usada. O
padrão para escrever um teste é o **AAA — Arrange, Act, Assert**:

1. **Arrange**: preparo os dados de entrada e o resultado esperado.
2. **Act**: chamo a função que quero testar.
3. **Assert**: comparo o resultado obtido com o esperado.

**Por que importa.** Testes te dão tranquilidade para refatorar: o que
estava funcionando continua funcionando. Num projeto com muita gente,
ninguém consegue testar tudo na mão — os testes rodam sozinhos e travam
qualquer mudança que quebre o comportamento.

**Como fazer — testando o transform sem depender de Excel.** A sacada dos
mocks/fixtures: em vez de depender de arquivos reais (lentos e frágeis),
você cria os dados na mão dentro do teste.

```python
# tests/test_transform.py
import pandas as pd
from app.pipeline.transform import transform


def test_transform_concatena_dataframes():
    # Arrange
    df1 = pd.DataFrame({"col": [1, 2, 3]})
    df2 = pd.DataFrame({"col": [4, 5, 6]})
    esperado = 6

    # Act
    resultado = transform([df1, df2])

    # Assert
    assert resultado.shape[0] == esperado
```

```bash
uv run pytest
uv run pytest -v
```

**Tipos de teste:** unitário (uma função isolada), integração (o encaixe de
várias partes, ex.: extract → transform juntos) e validação de dados
(checar nº de colunas, nomes esperados, duplicidade — muito comum em
dados).

!!! note "Por que usar bibliotecas prontas"
    Ninguém deve reescrever o pandas ou o [requests](https://requests.readthedocs.io/)
    do zero — os autores testaram cada método exaustivamente. Reinventar
    tudo é garantia de nunca entregar nada.

!!! tip "Com o Claude Code"
    Peça: «escreva testes pytest no padrão Arrange-Act-Assert para a
    função transform, usando DataFrames criados na mão». Deixe no
    `CLAUDE.md` a regra de ouro «todo bug vira um teste unitário» — assim
    o Claude Code cria o teste de regressão junto com a correção.

## Passo 9 — Padrões de código com Ruff

**O que é.** A [PEP 8](https://peps.python.org/pep-0008/) é o guia de
estilo oficial do Python: indentação, convenções de docstring, organização
de imports, etc. O [Ruff](https://docs.astral.sh/ruff/) (Astral, escrito em
Rust) aplica esse estilo automaticamente — e substitui, num único binário
rápido, todo o stack clássico de lint/formatação (black, isort, flake8,
pydocstyle, bandit).

```bash
uv add --dev ruff

ruff check .             # linter
ruff check --fix .       # corrige automaticamente o que dá
ruff format .            # formatador
```

Uma config curta em `pyproject.toml` ativa, de uma vez, todas as regras
relevantes (veja a [lista completa de regras](https://docs.astral.sh/ruff/rules/)):

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
# E=estilo  F=erros  I=imports  D=docstrings  UP=modernização  B=bugs  S=segurança
select = ["E", "F", "I", "D", "UP", "B", "S"]
```

**Por que importa.** Padrão de código não é gosto pessoal — é consenso da
comunidade para que qualquer um se localize em qualquer projeto. O ganho
real é acelerar o onboarding: ninguém perde tempo discutindo estilo e o
foco vai para o que importa.

!!! tip "Com o Claude Code"
    Peça: «configure o Ruff no pyproject.toml, rode `ruff check --fix` e
    `ruff format`, e me mostre o diff». Ele ajusta a config, aplica as
    correções e destaca o que sobrou para você revisar à mão.

## Passo 10 — Automatize as tarefas (taskipy)

**O que é.** Ninguém decora `ruff check --fix . && ruff format . && pytest`
o dia inteiro. O [taskipy](https://github.com/taskipy/taskipy) deixa você
definir "atalhos" no `pyproject.toml` e rodar tudo com um comando curto.

**Por que importa.** Padronização entre projetos: se toda empresa tem um
`task format` e um `task test`, o desenvolvedor chega em qualquer
repositório e não precisa saber quais bibliotecas rodam por baixo.

**Como fazer.**

```toml
# pyproject.toml
[tool.taskipy.tasks]
format = "ruff check --fix . && ruff format ."
lint   = "ruff check . && ruff format --check ."
test   = "pytest -v"
```

```bash
uv run task format
uv run task lint
uv run task test
```

!!! tip "Com o Claude Code"
    Peça: «crie as tasks format/lint/test no pyproject com taskipy, usando
    ruff e pytest». Depois, no `CLAUDE.md`, registre «sempre rode
    `task format` antes de commitar» — e ele passa a fazer isso sozinho a
    cada alteração.
