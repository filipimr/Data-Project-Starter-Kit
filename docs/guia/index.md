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

As práticas estão agrupadas em 5 blocos. Você não precisa adotar tudo de uma
vez — veja a seção de [Retrofit / Adoção Incremental](retrofit.md) para uma
ordem de adoção incremental que evita over-engineering. Cada passo segue a
mesma estrutura: o que é, por que importa, como fazer.

A ordem dos blocos:

1. **[Fundação do ambiente](fundacao.md)** — o que você faz no "primeiro dia" do projeto.
2. **[Código profissional](codigo.md)** — modularização, docstrings, pacotes.
3. **[Garantia de qualidade](qualidade.md)** — testes, padrões de código, automação de tarefas.
4. **[Documentação viva](documentacao.md)** — uma doc viva que nasce do próprio código.
5. **[Fluxo e colaboração](colaboracao.md)** — hooks, integração contínua e revisão de código.

Ao longo do texto, os quadros "Com o Claude Code" mostram, para cada prática, como delegar aquilo ao [Claude Code](https://docs.claude.com/en/docs/claude-code/overview), a ferramenta de linha de comando da Anthropic.

Este template já usa **[uv](https://docs.astral.sh/uv/)** (ambiente e dependências) e **[Ruff](https://docs.astral.sh/ruff/)** (lint e formatação) — as duas ferramentas modernas da Astral que consolidam boa parte do ferramental clássico do ecossistema Python (pyenv, pip, venv, Poetry, black, isort, flake8, pydocstyle, bandit).

Além disso, o kit integra as seguintes ferramentas:
- **[pytest](https://docs.pytest.org/)** para a suíte de testes (padrão Arrange-Act-Assert)
- **[taskipy](https://github.com/taskipy/taskipy)** para atalhos de tarefas
- **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** + **[mkdocstrings](https://mkdocstrings.github.io/)** para a documentação viva
- **[pre-commit](https://pre-commit.com/)** para hooks de Git (regras locais)
- **[GitHub Actions](https://docs.github.com/en/actions)** para Integração Contínua (CI)

Este guia foca nelas; se você herdar um projeto legado com o stack clássico, veja a seção de [Retrofit](retrofit.md).

Após finalizar o guia, consulte o [Checklist final](checklist.md) para validação rápida.
