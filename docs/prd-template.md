# Template de PRD (Product Requirement Document) para Desenvolvimento com IA

*Este documento serve como especificação para um agente de IA (como Claude Code, Cursor, Windsurf, etc.) realizar uma tarefa ou implementar uma funcionalidade no repositório. Preencha os campos abaixo com o máximo de especificidade técnica possível para evitar alucinações e desvios de escopo.*

---

## 1. Identificação da Funcionalidade

- **Nome da Funcionalidade:** [Ex: Pipeline de Extração de API de Faturamento]
- **Data:** [AAAA-MM-DD]
- **Autor/Responsável:** [Seu Nome ou Usuário]
- **Status:** [Rascunho / Pronto para IA / Em Execução / Concluído]

---

## 2. Contexto & Visão Geral (O "Porquê")

*Explique brevemente o problema de negócio ou a necessidade técnica. A IA precisa entender a motivação por trás do código para tomar decisões de design condizentes.*

> **Exemplo:** "Precisamos extrair os dados de faturamento diário da API externa da XPTO para substituir a planilha manual que o time de finanças usa hoje. O objetivo é carregar esses dados no nosso banco local para relatórios de fechamento mensal."

- **Objetivo Principal:** [O que a funcionalidade deve resolver]
- **Usuário/Sistema Consumidor:** [Quem ou o que vai usar o resultado]
- **Métricas de Sucesso (opcional):** [Ex: Tempo de execução < 5 min, zero perda de registros]

---

## 3. Escopo Funcional (O "O quê")

*Descreva em detalhes as regras de negócio de forma sequencial e lógica. Evite ambiguidades. Use listas imperativas.*

### Requisitos Funcionais:
1. [ ] **[Requisito 1]:** Descreva o que deve acontecer.
   - *Detalhe:* Regra específica, formato de entrada, comportamento esperado.
2. [ ] **[Requisito 2]:** Outro passo do fluxo.
3. [ ] **[Requisito 3]:** Fluxo de saída ou salvamento.

> **Dica para IA:** Descreva cenários no formato "Dado que [contexto], quando [evento], então [resultado]".

---

## 4. Escopo Técnico & Arquitetura (O "Como")

*Indique onde a IA deve atuar. Isso economiza tokens, evita que o agente vasculhe arquivos desnecessários e previne edições fora do lugar correto.*

### Arquivos de Impacto:
- **Novos Arquivos [NEW]:**
  - `[caminho/do/novo_arquivo.py](file:///path/to/file)`: Descreva a responsabilidade do arquivo.
- **Arquivos a Modificar [MODIFY]:**
  - `[caminho/do/arquivo_existente.py](file:///path/to/file)`: O que deve ser alterado ou adicionado aqui.
- **Arquivos a Deletar [DELETE] (se houver):**
  - `[caminho/do/arquivo_deletado.py](file:///path/to/file)`

### Especificações de Código & Assinaturas:
*Defina tipos, classes, funções e schemas de dados esperados.*

```python
# Exemplo de assinatura esperada para o entrypoint
def extract_billing_data(start_date: datetime.date, end_date: datetime.date) -> list[dict]:
    """Extrai os dados da API de faturamento e retorna uma lista de dicionários formatados.

    Args:
        start_date: Data de início do período.
        end_date: Data de fim do período.

    Returns:
        Lista de dicionários contendo os dados brutos validados.
    """
    pass
```

### Integrações & Dependências:
- **APIs Externas:** [Endpoints, autenticação necessária, limites de taxa (rate limits)]
- **Dependências Novas:** [Bibliotecas que a IA deve instalar via `uv add`]
- **Estruturas de Dados / Bancos de Dados:** [Schemas de tabelas SQL, colunas do Dataframe do Pandas, etc.]

---

## 5. Casos de Borda & Tratamento de Erros

*Agentes de IA frequentemente ignoram cenários de erro ou criam tratamentos genéricos (ex: `except Exception: pass`). Especifique como falhas devem ser tratadas.*

- **Inputs Inválidos:** [Ex: Se a data de fim for menor que a de início, lançar `ValueError`]
- **Falhas de Rede/API:** [Ex: Implementar retry exponencial (máx 3 tentativas) para erros 5xx na API]
- **Dados Ausentes/Nulos:** [Ex: Se o campo 'valor' for nulo, descartar a linha e registrar um log de aviso (`logger.warning`)]
- **Segurança de Credenciais:** [IMPORTANTE: Nunca colocar chaves/tokens hardcoded no código. Usar variáveis de ambiente/dotenv.]

---

## 6. Fora de Escopo (O que NÃO fazer)

*Essencial para conter a tendência da IA de "adivinhar" e codificar funcionalidades futuras não solicitadas.*

- [ ] **NÃO** crie nenhuma interface visual ou dashboard para esta etapa.
- [ ] **NÃO** adicione dependências pesadas adicionais a menos que explicitamente solicitado.
- [ ] **NÃO** altere a lógica de outros pipelines que compartilham funções utilitárias sem testes de regressão.

---

## 7. Plano de Testes & Validação

*Como o agente de IA deve provar que a alteração funciona. A IA executará os comandos fornecidos aqui.*

### Testes Automatizados (pytest):
- O agente deve criar testes cobrindo:
  - Caminho feliz (sucesso com inputs válidos).
  - Casos de erro (tratamento de exceção de API offline).
  - Dados ausentes (linhas com nulos sendo tratadas).
- **Comando de Execução:**
  ```bash
  uv run pytest tests/test_nome_do_modulo.py -v
  ```

### Validação Manual (se aplicável):
1. Execute o script com dados mockados em `data/input/mock_data.json`.
2. Verifique se o arquivo de saída foi gerado em `data/output/resultado.json`.
3. Valide se a estrutura das colunas de saída bate com o esperado.

---

## 8. Definição de Pronto (DoD) & Diretrizes para a IA

*Instruções finais e restrições de comportamento que o agente deve validar antes de marcar a tarefa como concluída.*

> [!IMPORTANT]
> **Checklist de Conformidade do Agente de IA:**
> - [ ] O código cumpre 100% dos requisitos funcionais especificados na Seção 3.
> - [ ] Todos os novos métodos e funções possuem **Type Hints** explícitos e docstrings no estilo Google.
> - [ ] Nenhum código mockado ou placeholder restou nos arquivos finais.
> - [ ] A suite de testes foi executada e passou com 100% de sucesso.
> - [ ] A formatação e linting foram corrigidos e validados via `uv run task lint` e `uv run task format`.
> - [ ] Os hooks do pre-commit rodam localmente com sucesso sem erros.
> - [ ] As convenções do arquivo `CLAUDE.md` foram rigorosamente seguidas.
