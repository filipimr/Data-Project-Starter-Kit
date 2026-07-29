# Biblioteca de skills

Esta pasta guarda **skills de IA** reutilizáveis: guias operacionais que
ensinam um agente (Claude Code ou outro) a executar bem uma tarefa
recorrente — protocolo de conexão com uma ferramenta, padrões testados,
armadilhas conhecidas, checklist antes de concluir. Uma skill é
essencialmente a experiência de campo de alguém, escrita de um jeito que o
agente consegue carregar e seguir.

## Estrutura

```text
.agents/skills/
├── README.md            # este arquivo
├── _template/
│   └── SKILL.md          # copie esta pasta para começar uma skill nova
└── <categoria>/
    └── <nome-da-skill>/
        ├── SKILL.md       # obrigatório: frontmatter + workflow
        └── references/    # opcional: conteúdo longo, linkado do SKILL.md
```

Agrupar por categoria (`pbi/`, `aws/`, `dbt/`...) é uma convenção, não uma
regra — use se ajudar a navegar quando a lista crescer.

## Como criar uma skill nova

1. Copie o template: `cp -r .agents/skills/_template .agents/skills/<categoria>/<nome>`.
2. Preencha o `SKILL.md` seguindo os comentários do próprio template —
   principalmente o `description` do frontmatter, que é o que o agente usa
   para decidir quando carregar a skill.
3. Apague as seções que não se aplicam (nem toda skill precisa de
   Pré-requisitos, Troubleshooting, etc.) e o bloco de comentário do topo.
4. Teste: peça ao agente para executar uma tarefa que deveria disparar a
   skill e confira se ele a usou corretamente.

## Onde buscar skills prontas

[skillsmp.com](https://skillsmp.com/) é um marketplace de skills para
agentes de IA — vale buscar lá antes de escrever uma do zero; muitas
tarefas comuns (linguagens, frameworks, ferramentas populares) já têm
skill publicada para adaptar.

## Boas práticas de uso

- **Uma skill, uma responsabilidade.** Evite skills "faz tudo" — elas
  ficam vagas e o agente tem mais dificuldade de saber quando ativá-las.
- **`description` é o gatilho.** Escreva-a pensando em quais frases do
  usuário deveriam ativar a skill. Description genérica = skill que nunca
  é carregada ou é carregada na hora errada.
- **Skill portátil > skill acoplada.** Não hardcode caminhos, credenciais
  ou nomes específicos deste repositório dentro de uma skill — ela deve
  funcionar em qualquer projeto que a reaproveite.
- **Leia antes de escrever.** Se a skill envolve ferramentas com efeito
  colateral (criar, editar, deletar), o workflow deve sempre inspecionar o
  estado atual antes de aplicar qualquer mudança.
- **Revise skills de terceiros antes de usar.** Uma skill baixada do
  [skillsmp.com](https://skillsmp.com/) ou de qualquer fonte externa é,
  na prática, instruções que o agente vai seguir — trate como revisaria
  código de terceiros antes de rodar.
- **Documente armadilhas reais**, não hipotéticas. A seção "Armadilhas
  Conhecidas" só vale a pena se vier de um problema que já aconteceu.
- **Versione as skills com o código.** Commitá-las no repositório garante
  que todo o time (e toda sessão futura do agente) parta do mesmo
  conhecimento, em vez de cada pessoa reconstruir a mesma skill do zero.
