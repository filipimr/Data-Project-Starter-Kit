# Guia de boas práticas

Do "na minha máquina funciona" a um projeto profissional, reproduzível e
testado — passo a passo aplicável a qualquer projeto de dados (ETL, ML,
API, dashboard), usando **uv** e **Ruff** como base de ferramental e o
Claude Code como acelerador.

## Por que este guia existe

Existem dois projetos que fazem exatamente a mesma coisa. O primeiro é uma
pasta com um único arquivo de código: funciona na máquina de quem escreveu
e em nenhuma outra. Ninguém sabe qual versão de Python usar, quais
bibliotecas instalar, nem como executar. O segundo tem a mesma
funcionalidade, mas qualquer pessoa consegue clonar, instalar e rodar em
minutos — porque ele é estruturado.

A diferença entre os dois não é inteligência nem talento: é processo. Este
guia descreve, passo a passo, o processo que transforma um script solitário
em um projeto de engenharia de dados profissional. Os exemplos usam um ETL
(ler vários arquivos Excel de mesmo formato, consolidar e salvar), porque
ETL é o feijão-com-arroz de dados — mas cada prática aqui vale para
qualquer projeto: API, dashboard, biblioteca, pipeline de ML.

!!! abstract "A meta final"
    Todo o esforço abaixo serve a um único objetivo — que outro
    desenvolvedor consiga rodar o seu código na máquina dele. O README é o
    mapa; o resto é o que garante que o mapa não minta.

## Como ler este guia

São 14 práticas agrupadas em 5 blocos. Você não precisa adotar tudo de uma
vez — veja "Como aplicar isto em qualquer projeto", mais abaixo, para uma
ordem de adoção incremental que evita over-engineering. Cada passo segue a
mesma estrutura: o que é, por que importa, como fazer.

A ordem dos blocos:

1. **Fundação do ambiente** — o que você faz no "primeiro dia" do projeto.
2. **Código profissional** — modularização, docstrings, pacotes.
3. **Garantia de qualidade** — testes, padrões de código, automação de tarefas.
4. **Documentação** — uma doc viva que nasce do próprio código.
5. **Fluxo e colaboração** — hooks, integração contínua e revisão de código.

Os quadros "Com o Claude Code" mostram, para cada prática, como delegar
aquilo ao [Claude Code](https://docs.claude.com/en/docs/claude-code/overview),
a ferramenta de linha de comando da Anthropic.

Este template já usa **[uv](https://docs.astral.sh/uv/)** (ambiente e
dependências) e **[Ruff](https://docs.astral.sh/ruff/)** (lint e
formatação) — as duas ferramentas modernas da Astral que consolidam boa
parte do ferramental clássico do ecossistema Python (pyenv, pip, venv,
Poetry, black, isort, flake8, pydocstyle, bandit). Este guia foca nelas;
se você herdar um projeto legado com o stack clássico, veja a seção
"Retrofit", mais abaixo.

## Bloco 1 — Fundação do ambiente

Estes quatro passos são o que você configura antes de escrever qualquer
lógica. São eles que resolvem 40–50% do clássico "na minha máquina
funciona". No primeiro dia em uma empresa, esse costuma ser o seu trabalho:
colocar o ambiente de pé.

### Passo 1 — Fixe a versão do Python

**O que é.** Sua máquina tem uma versão "global" de Python. Conforme você
instala coisas, versões vão se sobrescrevendo e um dia tudo para de
funcionar. O [`uv`](https://docs.astral.sh/uv/concepts/python-versions/)
resolve isso: instala e gerencia múltiplas versões de Python e fixa qual
versão cada projeto usa, criando um arquivo `.python-version` na pasta. Ao
entrar nela, a versão certa é usada automaticamente.

**Por que importa.** O Python só dá suporte às 3 versões mais recentes.
Rodar em uma versão muito antiga (ex.: 3.8 para trás) é risco de segurança:
falhas descobertas não são mais corrigidas. Fixar a versão também garante
que quem clonar o projeto use exatamente a mesma que você.

**Como fazer.**

```bash
uv python install 3.13     # instala a versão
uv python pin 3.13         # fixa no projeto (cria .python-version)
```

!!! note "Dica"
    Sempre comece pela versão mais moderna e só desça se alguma biblioteca
    crítica ainda não a suportar. Bibliotecas grandes (como o pandas) podem
    levar semanas para suportar uma nova versão do Python — confira no
    [PyPI](https://pypi.org/).

!!! tip "Com o Claude Code"
    Peça: «instale o Python 3.13 e fixe a versão deste projeto». O Claude
    Code roda o `uv` por você e confere o `.python-version` gerado, sem
    você decorar comandos.

### Passo 2 — Ambiente virtual e gestão de dependências

**O que é.** Instalar uma biblioteca globalmente mistura versões entre
projetos: um pede a 3.2 de uma lib, outro pede a 3.1, e um quebra o outro.
Um ambiente virtual isola as dependências por projeto. O
[`uv`](https://docs.astral.sh/uv/guides/projects/) cria e gerencia esse
ambiente automaticamente — não há "ativar" nada manualmente, você só
prefixa comandos com `uv run`.

O [PyPI](https://pypi.org/) (Python Package Index) é o banco de dados
público de onde essas bibliotecas vêm. Ao instalar o pandas, o `uv` lê as
dependências dele (numpy, etc.) e resolve a árvore inteira automaticamente.

**Como fazer.**

```bash
uv add pandas openpyxl      # adiciona dependências + atualiza o uv.lock
uv add --dev pytest         # dependência só de desenvolvimento
uv sync                     # instala tudo a partir do lock (reproduzível)
uv run python app/main.py   # roda dentro do ambiente, sem "ativar" nada
```

O `pyproject.toml` e o `uv.lock` registram exatamente quais versões o
projeto usa. Quem clonar roda um `uv sync` e recebe o ambiente idêntico ao
seu — é isso que torna o projeto determinístico e mata o "na minha máquina
funciona".

!!! tip "Com o Claude Code"
    Peça: «adicione `<biblioteca>` como dependência com uv e rode
    `uv run pytest` para confirmar que nada quebrou». Para migrar um
    projeto legado: «migre este projeto para uv, gerando o pyproject.toml e
    o uv.lock a partir do requirements.txt».

### Passo 3 — Controle de versão com Git

**O que é.** O [Git](https://git-scm.com/doc) é um banco de dados de
versões do seu código — cada commit é um snapshot que aponta para o
anterior.

**Por que importa.**

- **Versionamento**: você viaja no tempo para qualquer ponto do projeto.
- **Backup distribuído**: se perder a máquina, restaura do remoto
  ([GitHub](https://docs.github.com/)) ou de um colega.
- **Colaboração**: é impraticável trabalhar em equipe séria sem Git —
  "trabalho sozinho" não é desculpa, o Git te dá histórico e segurança
  para errar.

**Como fazer.**

```bash
git init
git add .gitignore README.md   # adicione arquivo por arquivo (boa prática)
git commit -m "estrutura inicial do projeto"

git remote add origin <url-do-repo>
git push origin main
```

Trabalhe em branches separadas por funcionalidade e junte com merge — isso
dá rastreabilidade: se algo quebrar, você isola.

```bash
git branch extract
git checkout extract           # ou: git switch extract
# ...trabalha e commita...
git checkout main
git merge extract
```

!!! warning "Cuidado"
    Commite arquivos separadamente e com mensagens claras. Se você junta um
    arquivo bom e um quebrado no mesmo commit, não consegue voltar só o que
    interessa. E lembre: seus commits ficam no histórico para sempre —
    nada de mensagens de raiva.

O README é o arquivo mais importante do repositório: é para o próximo
desenvolvedor (inclusive o "você" de daqui a 6 meses) e deve dizer o que o
projeto faz e, principalmente, como cloná-lo e rodá-lo do zero.

!!! tip "Com o Claude Code"
    Peça: «gere um .gitignore para Python + uv e faça commits pequenos e
    descritivos, um por arquivo». Se você registrar o padrão de mensagem
    (ex.: [Conventional Commits](https://www.conventionalcommits.org/)) no
    `CLAUDE.md`, ele escreve todos os commits nesse formato — e abre o PR
    pelo `gh` quando você pedir.

### Passo 4 — Estrutura de pastas

**O que é.** Uma organização de pastas previsível. Independente do
framework (Django, FastAPI, Streamlit...), o padrão base é sempre o mesmo:

```text
meu-projeto/
├── app/              # (ou src/) todo o CÓDIGO vive aqui dentro
│   └── pipeline/     #   módulos do seu fluxo (ex.: extract, transform, load)
├── tests/            # testes automatizados
├── docs/             # documentação
├── data/             # dados de exemplo (input/ e output/) — normalmente ignorado
├── .python-version   # (uv) versão travada
├── pyproject.toml    # (uv) dependências e config
├── .gitignore
└── README.md
```

A regra de ouro: código fica dentro da pasta de código. Não importa se você
usa Django (models, views), FastAPI (routers) ou um dashboard — tudo isso
mora em `app/`. As pastas `tests/`, `docs/` e `data/` são universais.

!!! note "Sobre dados"
    Em produção você raramente guarda dados localmente — eles vêm de um
    data lake, S3, banco. A pasta `data/` costuma servir só para
    exemplos/testes e quase sempre entra no `.gitignore` (não versione
    dados pesados ou sensíveis).

!!! tip "Com o Claude Code"
    Peça: «monte o esqueleto app/ tests/ docs/ data/ com os `__init__.py`».
    Ele cria a estrutura inteira em segundos; revise o diff antes de
    aceitar.

## Bloco 2 — Escrevendo o código de forma profissional

Com o ambiente pronto, o código em si muda de qualidade quando você o
escreve de forma modular, documentada e reutilizável.

### Passo 5 — Modularize em funções pequenas

**O que é.** Em vez de um arquivo gigante que faz tudo, quebre o fluxo em
módulos com responsabilidade única. Num ETL, o desenho natural é
Extract → Transform → Load:

- `extract` — lê os arquivos de uma pasta e devolve uma lista de DataFrames.
- `transform` — recebe a lista, concatena e devolve um único DataFrame.
- `load` — recebe o DataFrame e salva, criando a pasta de saída se não existir.

**Por que importa.** Você quase nunca coda só para você — coda para outras
áreas (analistas, cientistas de dados) reaproveitarem. Modularizado, o
colega importa apenas a função que precisa. Funções pequenas também são
mais fáceis de testar, documentar e escalar.

**Como fazer — exemplo do extract.**

```python
# app/pipeline/extract.py
from pathlib import Path

import pandas as pd


def extract(input_folder: str) -> list[pd.DataFrame]:
    """Lê todos os arquivos .xlsx de uma pasta e retorna uma lista de DataFrames."""
    files = Path(input_folder).glob("*.xlsx")
    return [pd.read_excel(file) for file in files]
```

!!! tip "Com o Claude Code"
    Peça: «refatore este script único, quebrando em extract/transform/load
    dentro de app/pipeline». Use o Plan Mode primeiro: o Claude Code mostra
    o plano de refatoração para você aprovar antes de tocar em qualquer
    arquivo.

### Passo 6 — Docstrings e type hints

**O que é.** Uma docstring é a documentação embutida logo abaixo da
definição da função. [Type hints](https://docs.python.org/3/library/typing.html)
(`input_folder: str`, `-> list[pd.DataFrame]`) declaram os tipos de entrada
e saída.

**Por que importa.** Documentar antes de escrever ajuda a pensar: quais
argumentos a função recebe? O que retorna? O que ela faz? Quando outra
pessoa (ou uma IA) for usar sua função, ela lê a docstring e sabe o que
passar, sem abrir o código. Mais para a frente, a documentação do projeto é
gerada automaticamente a partir dessas docstrings (Passo 11, mais abaixo).

**Como fazer** (estilo [Google](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)):

```python
def transform(dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    """Concatena uma lista de DataFrames em um único DataFrame.

    Args:
        dataframes: lista de DataFrames com o mesmo esquema.

    Returns:
        Um único DataFrame com todos os registros concatenados.
    """
    return pd.concat(dataframes, ignore_index=True)
```

Você pode cobrar docstrings automaticamente: o Ruff (Passo 9, mais abaixo)
tem as regras `D` (equivalentes ao pydocstyle) que apontam funções sem
documentação e fora da convenção.

!!! tip "Com o Claude Code"
    Peça: «adicione docstrings (estilo Google) e type hints em todas as
    funções públicas deste módulo». Docstrings bem escritas viram
    documentação automática no Passo 11 — vale caprichar.

### Passo 7 — Pacotes e o `if __name__ == "__main__"`

**O guard `__main__`.** Quando você roda um arquivo diretamente, o Python
define `__name__` como `"__main__"`. Quando o arquivo é importado como
módulo, `__name__` recebe o nome do módulo. Veja a
[documentação oficial](https://docs.python.org/3/library/__main__.html).

**Transformando a pasta em [pacote](https://docs.python.org/3/tutorial/modules.html#packages).**
Para importar seus módulos com `from app.pipeline.extract import extract`,
cada pasta de código precisa de um `__init__.py` (pode ser vazio):

```text
app/
├── __init__.py
└── pipeline/
    ├── __init__.py
    ├── extract.py
    ├── transform.py
    └── load.py
```

Com isso, um `main.py` orquestra o fluxo inteiro, reaproveitando as
funções — a saída de um passo alimenta o próximo:

```python
# app/main.py
from app.pipeline.extract import extract
from app.pipeline.transform import transform
from app.pipeline.load import load

if __name__ == "__main__":
    dfs = extract("data/input")
    df = transform(dfs)
    load(df, "data/output", "consolidado.xlsx")
```

!!! tip "Com o Claude Code"
    Peça: «transforme estas pastas em pacotes com `__init__.py` e crie um
    `main.py` que orquestra o ETL». Ele monta o ponto de entrada e ajusta
    os imports para o novo layout.

## Bloco 3 — Garantia de qualidade

Aqui o projeto ganha rede de segurança. Testes, padrões de código e
automação de tarefas são o que permitem mexer no código sem medo.

### Passo 8 — Testes automatizados com pytest

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

### Passo 9 — Padrões de código com Ruff

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

### Passo 10 — Automatize as tarefas (taskipy)

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

## Bloco 4 — Documentação viva

### Passo 11 — Documentação com MkDocs

**O que é.** O [MkDocs](https://www.mkdocs.org/) transforma arquivos
Markdown em um site de documentação navegável. Com o tema
[Material](https://squidfunk.github.io/mkdocs-material/), o resultado tem a
cara das docs profissionais (é o mesmo usado por projetos como o FastAPI).

**Por que importa.** Boa documentação faz o time de negócio e o time
técnico se falarem — e ferramentas hospedadas (Confluence e similares)
cobram por usuário; o MkDocs entrega documentação hospedada de graça via
[GitHub Pages](https://docs.github.com/en/pages).

**Como fazer.**

```bash
uv add --dev mkdocs mkdocs-material "mkdocstrings[python]" pymdown-extensions

uv run mkdocs serve        # sobe o site local em http://127.0.0.1:8000
```

Os três recursos que mais valem a pena:

- **[mkdocstrings](https://mkdocstrings.github.io/)** — documentação que
  nasce do código. Em vez de reescrever, você aponta para a função e o
  plugin puxa a docstring automaticamente:

  ```markdown
  ::: app.pipeline.transform
  ```

  Código e documentação ficam sempre sincronizados — quem altera a função
  altera a doc no mesmo lugar.

- **[Mermaid](https://mermaid.js.org/)** — fluxogramas escritos em texto:

  ````markdown
  ```mermaid
  graph LR
    A[Extract] --> B[Transform] --> C[Load]
  ```
  ````

- **`mkdocs gh-deploy`** — publicação gratuita no GitHub Pages:

  ```bash
  uv run mkdocs build          # gera o site estático em site/
  uv run mkdocs gh-deploy      # publica no GitHub Pages
  ```

!!! tip "Com o Claude Code"
    Peça: «configure o MkDocs Material com mkdocstrings apontando para
    app/ e crie a página que documenta o pipeline». Ele conecta as
    docstrings à doc, gera os diagramas Mermaid do fluxo e sobe o
    `mkdocs serve` para você conferir.

## Bloco 5 — Fluxo e colaboração

Os últimos passos automatizam a qualidade no fluxo de trabalho, para que
código ruim simplesmente não chegue à produção.

### Passo 12 — Pre-commit hooks

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

### Passo 13 — Integração Contínua (CI) com GitHub Actions

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

### Passo 14 — Pull Requests e revisão de código

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

## Como aplicar isto em qualquer projeto

A tentação depois de ver tudo isso é querer implantar as 14 práticas no
primeiro dia. Não faça isso. O maior erro é o over-engineering: passar um
mês montando estrutura perfeita e não entregar nada. A régua é sempre: qual
dor este passo resolve agora?

**Ordem de adoção incremental sugerida:**

1. Fundação (Passos 1–4) — elimina metade dos problemas de "na minha
   máquina funciona".
2. Modularize e documente (Passos 5–7) conforme o código cresce.
3. Adicione testes (Passo 8) — e a cada bug, um teste novo.
4. Padronize o estilo (Passos 9–10) quando mais de uma pessoa toca o código.
5. Documente de verdade (Passo 11) quando outras áreas precisam entender o
   projeto.
6. Automatize o fluxo (Passos 12–14) quando o time cresce e a colaboração
   exige garantias.

**Monorepo vs. multirepo.** Não há certo — depende dos padrões do time.
Centralizando, crie pastas como `analise/`, `dashboard/`, `pipeline/`.
Quebrando, publique sua pipeline como biblioteca e importe-a de outros
projetos. O importante é ser consistente.

## Retrofit: aplicando em projetos que já existem

Raramente você começa do zero. O cenário mais comum é herdar um repositório
que já roda mas não tem estrutura: sem testes, sem padrão, com dependências
soltas. O [Claude Code](https://docs.claude.com/en/docs/claude-code/overview)
foi feito justamente para esse trabalho de arqueologia + reforma
incremental.

1. **Diagnóstico (em Plan Mode)** — abra o terminal na raiz do repositório,
   rode `claude`, entre em Plan Mode e peça: «Audite este repositório
   contra o checklist deste guia. Não altere nada ainda — só me diga o que
   falta e proponha uma ordem de implementação.» O Plan Mode faz o Claude
   Code ler o código e devolver um plano sem tocar nos arquivos.
2. **Escreva um `CLAUDE.md`** com as convenções do projeto — rode `/init`
   para gerar um rascunho e ajuste: ambiente (uv), padrão de código (Ruff),
   testes (pytest + AAA), commits (ex.: Conventional Commits), a regra
   crítica «nunca use `git commit --no-verify`», e onde ficam código,
   testes e documentação.
3. **Migre uma coisa por vez, cada uma em seu PR** — não peça "arruma
   tudo". Um prompt por branch/PR, na ordem incremental acima: ambiente →
   padrão → testes → docstrings → documentação → automação.
4. **Deixe as travas cuidarem do agente** — depois que pre-commit e CI
   existem, eles passam a guardar as próprias mudanças do Claude Code: se
   ele gerar código fora do padrão ou quebrar um teste, o commit ou o PR
   trava. Ainda assim, revise sempre o diff e o PR.

!!! warning "Menos é mais"
    Peça diffs pequenos. Um PR gigante gerado por IA é impossível de
    revisar e vira dívida técnica. Uma prática por PR mantém o histórico
    limpo e a revisão sã.

## Checklist final do projeto

Use como referência rápida. O objetivo continua sendo um só: outra pessoa
clona, instala, testa e roda o seu projeto sem te chamar.

**Fundação**

- [ ] Versão do Python travada com uv (`.python-version`)
- [ ] Ambiente e dependências com uv (`pyproject.toml` + `uv.lock`)
- [ ] Repositório Git com `.gitignore` e histórico de commits limpo
- [ ] README explicando o que é e como rodar do zero
- [ ] `CLAUDE.md` com as convenções do projeto (uv, ruff, pytest, "sem `--no-verify`")
- [ ] Estrutura de pastas: `app/` (código), `tests/`, `docs/`, `data/`

**Código**

- [ ] Lógica modularizada em funções pequenas com responsabilidade única
- [ ] Docstrings e type hints em módulos e funções públicas
- [ ] Pacotes com `__init__.py` e uso correto do `if __name__ == "__main__"`

**Qualidade**

- [ ] Testes com pytest (unitários + integração), padrão Arrange-Act-Assert
- [ ] Um teste novo para cada bug corrigido
- [ ] Padrões de código com Ruff (check + format)
- [ ] Atalhos de tarefa (taskipy): `task format`, `task lint`, `task test`

**Documentação e fluxo**

- [ ] Documentação em MkDocs (Material, mkdocstrings, Mermaid) publicada com `gh-deploy`
- [ ] Pre-commit hooks instalados: ruff-check, ruff-format, uv-lock
- [ ] CI no GitHub Actions (setup-uv + ruff + pytest) a cada push/PR
- [ ] Pull Requests com revisão obrigatória antes do merge

Estrutura não é burocracia — é o que permite errar com segurança e criar
sem medo.
