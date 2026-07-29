<!--
TEMPLATE DE SKILL — copie esta pasta inteira para criar uma skill nova:

  cp -r .agents/skills/_template .agents/skills/<categoria>/<nome-da-skill>

Depois edite o SKILL.md copiado (não este). Regras rápidas antes de preencher:
- `name` no frontmatter = nome da pasta (kebab-case), sem espaços.
- `description` é o texto mais importante do arquivo: é a partir dele que
  o agente decide SE e QUANDO carregar a skill. Inclua o que a skill faz
  E quando usá-la (frases-gatilho, tipo de tarefa, palavras-chave). Uma
  description vaga = skill que nunca é ativada ou é ativada errado.
- Apague as seções que não fizerem sentido para a sua skill. Nem toda
  skill precisa de Pré-requisitos, Troubleshooting ou Checklist.
- Se o conteúdo de uma seção passar de ~50 linhas, mova para um arquivo
  em `references/` e linke daqui (mantém o SKILL.md principal escaneável).
- Apague todo este bloco de comentário antes de commitar a skill.
-->

---
name: nome-da-skill
description: 'Uma frase densa cobrindo O QUE a skill faz e QUANDO usá-la — inclua frases-gatilho, tipo de tarefa e palavras-chave que devem ativar esta skill. Ex.: "Assistente para X. Use quando o usuário pedir Y, mencionar Z, ou trabalhar com <tecnologia>. Aciona em: <gatilho 1>, <gatilho 2>."'
---

# Título Legível da Skill

Uma ou duas frases: o que esta skill entrega e por que ela existe.

## Quando Usar Esta Skill

Use esta skill quando o usuário pedir:
- ...
- ...
- ...

**Frases-gatilho:** "...", "...", "..."

## Pré-requisitos

### Ferramentas necessárias
- **Nome da ferramenta/MCP**: para que serve, o que ela habilita.

### Dependências opcionais
- **Nome da ferramenta**: quando vale a pena usar além do essencial.

## Workflow

### 1. Primeiro passo (ex.: entender o estado atual antes de agir)

Descreva a sequência exata de ações/comandos. Se a skill envolve
ferramentas com efeito (criar, editar, deletar), a primeira etapa quase
sempre deveria ser "leia antes de escrever".

```
comando_ou_chamada(operation: "...")
```

### 2. Segundo passo

...

### 3. Terceiro passo (aplicar a mudança)

...

## Referência Rápida

| Área | Boa prática |
|------|-------------|
| ...  | ...         |

## Tarefas Comuns

### Nome da tarefa recorrente

```
exemplo mínimo e copiável
```

## Armadilhas Conhecidas

### Nome da armadilha

O que dá errado e por quê.

**Como detectar:** sinal concreto de que o problema está acontecendo.
**Solução:** o que fazer a respeito.

## Troubleshooting

| Sintoma | Causa mais comum | O que fazer |
|---------|-------------------|-------------|
| ...     | ...               | ...         |

## Checklist Antes de Concluir

- [ ] ...
- [ ] ...
