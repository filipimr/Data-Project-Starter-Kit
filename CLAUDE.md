# CLAUDE.md

Guia para o Claude Code (claude.ai/code) trabalhar neste repositório.

## O que é este repositório

- Template público para começar projetos de dados em Python (ETL, ML, API,
  dashboard) já com uv, Ruff, pytest, MkDocs, pre-commit e CI prontos.
- Leia `docs/guia-boas-praticas.md` para entender o *porquê* de cada
  convenção abaixo, com links para a documentação oficial de cada
  ferramenta.
- `app/pipeline/{extract,transform,load}.py` são placeholders
  (`raise NotImplementedError` + TODO). Não implemente por especulação —
  este repositório É o template, não um pipeline pronto.
- `.agents/skills/` guarda skills reutilizáveis (guias operacionais para
  tarefas recorrentes). Para criar uma, copie
  `.agents/skills/_template/SKILL.md`; veja `.agents/skills/README.md`
  para a convenção completa e para o link do
  [skillsmp.com](https://skillsmp.com/) (marketplace de skills prontas).

## Comandos

```bash
uv sync                        # instala as dependências
uv run task format              # ruff check --fix . && ruff format .
uv run task lint                 # ruff check . && ruff format --check .
uv run task test                 # pytest -v
uv run task docs                 # mkdocs serve
uv run mkdocs build --strict     # confere se os docs buildam sem erro
uv run pre-commit run --all-files
```

Teste único: `uv run pytest tests/test_transform.py -k nome_do_teste`.

`uv run python app/main.py` levanta `NotImplementedError` de propósito.
Não "conserte" isso — é o estado de placeholder do template.

## Arquitetura

- `app/` é importado como pacote de nível superior comum:
  `[tool.uv] package = false` no `pyproject.toml`, sem build de wheel, o
  `app.*` resolve via inserção de rootdir do pytest. Não reintroduza
  `[build-system]`/hatchling sem motivo — já quebrou o `uv sync` antes
  (exigia um README no momento do build).
- `docs/pipeline.md` é renderizado ao vivo a partir das docstrings de
  `app/pipeline` via mkdocstrings. Edite a docstring, não a página de doc.
- A tag `!!python/name:` do `mkdocs.yml` quebra o parser seguro do hook
  `check-yaml` do pre-commit — esse arquivo é excluído do hook de
  propósito, não é um bug.
- Ruff: `select = ["E","F","I","D","UP","B","S"]`, docstrings estilo
  Google. `tests/*` é isento de `D`/`S101`.
- `docs/stylesheets/extra.css` aplica a identidade visual Selbetti (cores
  Forest/Signal Orange/Selbetti Green, fonte Oswald nos títulos) por cima
  do tema Material padrão — carregado via `extra_css` no `mkdocs.yml`, que
  também tem `theme.font: false` de propósito (a tipografia é 100%
  controlada por esse CSS, não pela config do Material). Os `!important`
  nos admonitions são necessários para vencer a especificidade do CSS do
  Material; não remova. Se o pedido for "deixar genérico"/"tirar a marca",
  isso é decisão do usuário, não um bug a corrigir sozinho.

## Fluxo de Git

- Nunca use `git commit --no-verify`. Corrija o que o hook apontar.
- Um commit/PR por assunto, na ordem de adoção: ambiente → código → testes
  → lint/tasks → docs → hooks/CI. Nada de commit "arruma tudo".
- Ao preencher um placeholder: troque um `TODO` por vez e habilite o teste
  correspondente na mesma mudança. Não reescreva o pipeline inteiro de uma vez.

## Estilo de código

- Funções: 4-20 linhas. Quebre se passar disso.
- Arquivos: até 500 linhas. Divida por responsabilidade.
- Uma coisa por função, uma responsabilidade por módulo (SRP).
- Nomes: específicos e únicos. Evite `data`, `handler`, `Manager`.
  Prefira nomes que retornem menos de 5 ocorrências no grep do repositório.
- Tipos: explícitos. Nada de `any`, `Dict` genérico ou função sem tipo.
- Sem duplicação de código. Extraia lógica compartilhada para uma
  função/módulo.
- Early return em vez de ifs aninhados. No máximo 2 níveis de indentação.
- Mensagens de exceção devem incluir o valor problemático e o formato
  esperado.

## Comentários

- Preserve os comentários existentes. Não os remova ao refatorar — eles
  carregam intenção e proveniência.
- Escreva o PORQUÊ, não o QUÊ. Não comente `# incrementa o contador`
  acima de `i += 1`.
- Docstrings em funções públicas: intenção + um exemplo de uso.
- Referencie números de issue / SHAs de commit quando uma linha existe por
  causa de um bug específico ou de uma restrição externa.

## Testes

- Rode os testes com um único comando: `uv run pytest -v` (ou
  `uv run task test`).
- Toda função nova ganha um teste. Todo bug corrigido ganha um teste de
  regressão.
- Mocke I/O externo (API, banco, sistema de arquivos) com classes fake
  nomeadas, não com stubs inline.
- Testes devem seguir F.I.R.S.T: rápidos, independentes, repetíveis,
  auto-verificáveis e no tempo certo.

## Dependências

- Injete dependências via construtor/parâmetro, não via global/import.
- Encapsule bibliotecas de terceiros atrás de uma interface fina de
  propriedade deste projeto.

## Estrutura

- `app/` concentra todo o código, `tests/` espelha essa estrutura, `docs/`
  é o MkDocs. Se um framework (Django, FastAPI, Next.js...) entrar em
  cena, siga a convenção dele dentro de `app/`.
- Prefira módulos pequenos e focados a arquivos "faz-tudo".
- Caminhos previsíveis: controller/model/view, src/lib/test, etc.

## Formatação

- Use o formatador do projeto: `uv run ruff format .`. Não discuta estilo
  além disso.
- Isso cobre só Python. CSS/YAML/Markdown não têm formatador automatizado
  configurado neste repo — reformatação nesses arquivos (ex.: pelo editor
  do usuário) é cosmética e não precisa ser revertida nem replicada
  manualmente em outros arquivos.

## Logging

- JSON estruturado ao logar para debug/observabilidade.
- Texto puro apenas para saída de CLI voltada ao usuário.
