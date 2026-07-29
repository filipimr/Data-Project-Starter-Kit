# Bloco 4 — Documentação viva

## Passo 11 — Documentação com MkDocs

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
uv add --dev mkdocs mkdocs-material "mkdocstrings[python]" mkdocstrings-python pygments pymdown-extensions

uv run mkdocs serve        # sobe o site local em http://127.0.0.1:8000
```

| Pacote | Para que serve |
|--------|-----------------|
| [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/) | Tema Material Design para o MkDocs — o mais usado do ecossistema. |
| [`mkdocstrings-python`](https://mkdocstrings.github.io/python/) | Handler do `mkdocstrings` (instalado via `mkdocstrings[python]`) que gera documentação automaticamente a partir das docstrings de código Python. |
| [`pygments`](https://pygments.org/) | Biblioteca de destaque de sintaxe (syntax highlighting) usada nos blocos de código. |
| [`pymdown-extensions`](https://facelessuser.github.io/pymdown-extensions/) | Conjunto de extensões Markdown — blocos de código avançados, abas, admonitions (os quadros de dica/aviso deste guia), e mais. |

Declare os quatro como dependências diretas (não só transitivas) — é o que
garante que `uv sync` sempre instala exatamente essas versões, mesmo que a
resolução transitiva de algum deles mude no futuro.

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
