# Adoção Incremental e Retrofit

Esta seção explica como adotar o checklist de boas práticas de forma incremental, sem cair em over-engineering, e como aplicar a estrutura em repositórios legados existentes.

## Como aplicar isto em qualquer projeto

A tentação depois de ver tudo isso é querer implantar as 14 práticas no primeiro dia. Não faça isso. O maior erro é o over-engineering: passar um mês montando estrutura perfeita e não entregar nada. A régua é sempre: **qual dor este passo resolve agora?**

### Ordem de adoção incremental sugerida

1. **[Fundação do ambiente](fundacao.md)** (Passos 1–4) — elimina metade dos problemas de "na minha máquina funciona".
2. **[Código profissional](codigo.md)** (Passos 5–7) — faça isso conforme o código e a complexidade do projeto crescem.
3. **[Garantia de qualidade](qualidade.md)** (Passo 8) — adicione testes para a lógica principal e, a cada bug, um teste novo de regressão.
4. **Padronize o estilo** (Passos 9–10) — introduza Ruff e tarefas automatizadas quando mais de uma pessoa toca o código.
5. **[Documente](documentacao.md) de verdade** (Passo 11) — faça isso quando outras áreas ou desenvolvedores precisam entender o projeto.
6. **[Automatize o fluxo](colaboracao.md)** (Passos 12–14) — ideal quando o time cresce e a colaboração exige garantias automáticas de qualidade.

### Monorepo vs. multirepo

Não há certo — depende dos padrões do time. Centralizando, crie pastas como `analise/`, `dashboard/`, `pipeline/`. Quebrando, publique sua pipeline como biblioteca e importe-a de outros projetos. O importante é ser consistente.

---

## Retrofit: aplicando em projetos que já existem

Raramente começamos um projeto do zero. O cenário mais comum é herdar um repositório legado que já está em execução, mas sem estrutura definida: ausência de testes automatizados, falta de padrões de estilo e dependências não declaradas formalmente. O [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) é ideal para esse trabalho de auditoria e modernização incremental.

1. **Diagnóstico (em Plan Mode)** — abra o terminal na raiz do repositório, rode `claude`, entre em Plan Mode e peça:
   > «Audite este repositório contra o checklist deste guia. Não altere nada ainda — só me diga o que falta e proponha uma ordem de implementação.»

   O Plan Mode faz o Claude Code ler o código e devolver um plano sem tocar nos arquivos.

2. **Escreva um `CLAUDE.md` com as convenções do projeto** — rode `/init` para gerar um rascunho e ajuste: ambiente (uv), padrão de código (Ruff), testes (pytest + AAA), commits (ex.: Conventional Commits), a regra crítica «nunca use `git commit --no-verify`», e onde ficam código, testes e documentação.

3. **Migre uma coisa por vez, cada uma em seu PR** — não peça para "arrumar tudo". Envie um prompt por branch/PR, na ordem incremental sugerida: ambiente → padrão → testes → docstrings → documentação → automação.

4. **Deixe as travas cuidarem do agente** — depois que o pre-commit e a CI existem, eles passam a guardar as próprias mudanças do Claude Code: se ele gerar código fora do padrão ou quebrar um teste, o commit ou o PR trava. Ainda assim, revise sempre o diff e o PR.

!!! warning "Menos é mais"
    Peça diffs pequenos. Um PR gigante gerado por IA é impossível de revisar e vira dívida técnica. Uma prática por PR mantém o histórico limpo e a revisão sã.
