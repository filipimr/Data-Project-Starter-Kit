# IA como acelerador

Este template foi feito para ser usado junto com o
[Claude Code](https://docs.claude.com/en/docs/claude-code/overview), a
ferramenta de linha de comando da Anthropic. O arquivo `CLAUDE.md` na raiz
do repositório já registra as convenções do projeto (uv, Ruff, pytest,
padrão de commit, "nunca use `--no-verify`"), então o agente não precisa
redescobrir isso a cada sessão.

Abaixo, prompts prontos para avançar em cada parte ainda pendente do
template (os `TODO` deixados em `app/pipeline/`) ou para adaptá-lo a um
projeto real. Peça uma coisa de cada vez, em Plan Mode quando a mudança for
grande, e revise o diff antes de aceitar.

Se em vez de partir deste template você estiver aplicando estas práticas a
um repositório que já existe, veja a seção "Retrofit" no final do
[Guia de boas práticas](guia-boas-praticas.md) — ela cobre o fluxo de
diagnóstico, `CLAUDE.md` e migração incremental por PR.

## Adaptar o pipeline a um caso real

> «Substitua o `extract()` em `app/pipeline/extract.py` para ler arquivos
> `.xlsx` de `data/input/` com pandas, mantendo a assinatura e a docstring.»

> «Implemente `transform()` para concatenar a lista de DataFrames recebida e
> habilite o teste em `tests/test_transform.py`, removendo o
> `pytest.skip`.»

> «Implemente `load()` para salvar o DataFrame em Excel na pasta de saída,
> criando a pasta se não existir, e habilite o teste correspondente.»

## Ambiente e dependências

> «Adicione `<biblioteca>` como dependência com uv e rode `uv run pytest`
> para confirmar que nada quebrou.»

## Qualidade

> «Rode `ruff check --fix .` e `ruff format .`, e me mostre o diff antes de
> eu aceitar.»

> «Todo bug corrigido vira um teste de regressão em pytest, no padrão
> Arrange-Act-Assert.»

## Documentação

> «Adicione uma nova página em `docs/` documentando `<módulo novo>` via
> mkdocstrings, e rode `mkdocs serve` para eu conferir.»

## Fluxo e PRs

> «Abra um PR com título e descrição resumindo estas mudanças» — o Claude
> Code cria o PR pelo `gh` e a CI roda sozinha; a revisão continua sendo
> sua.

## Biblioteca de skills (`.agents/skills/`)

Além de prompts avulsos, este repositório guarda **skills** reutilizáveis
em `.agents/skills/` — guias operacionais mais longos que ensinam o agente
a executar bem uma tarefa recorrente (protocolo de uma ferramenta, padrões
testados, armadilhas conhecidas). Veja `.agents/skills/README.md` na raiz
do repositório para a estrutura completa e as boas práticas de uso; em
resumo:

- Para criar uma skill nova, copie `.agents/skills/_template/SKILL.md` e
  preencha o frontmatter e as seções indicadas nos comentários do template.
- Antes de escrever uma do zero, busque em
  [skillsmp.com](https://skillsmp.com/) — é um marketplace de skills para
  agentes de IA, muitas vezes já existe uma pronta para adaptar.
- Skills baixadas de fontes externas são instruções que o agente vai
  seguir — revise antes de usar, como revisaria código de terceiros.

> «Crie uma skill em `.agents/skills/` a partir do template para
> `<ferramenta/tarefa>`, documentando o workflow e as armadilhas que já
> encontramos.»

**Regra crítica:** nunca peça (e nunca aceite) `git commit --no-verify`. Se
um hook do pre-commit ou a CI falhar, corrija o que foi apontado em vez de
pular a verificação.
