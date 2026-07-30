# Bloco 1 — Fundação do ambiente

Estes quatro passos são o que você configura antes de escrever qualquer
lógica. São eles que resolvem 40–50% do clássico "na minha máquina
funciona". No primeiro dia em uma empresa, esse costuma ser o seu trabalho:
colocar o ambiente de pé.

## Passo 1 — Fixe a versão do Python

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

## Passo 2 — Ambiente virtual e gestão de dependências

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

## Passo 3 — Controle de versão com Git

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

## Passo 4 — Estrutura de pastas

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
    data lake, S3, banco de dados, etc. A pasta `data/` costuma servir só para
    exemplos/testes e quase sempre entra no `.gitignore` (não versione
    dados pesados ou sensíveis).

!!! tip "Com o Claude Code"
    Peça: «monte o esqueleto app/ tests/ docs/ data/ com os `__init__.py`».
    Ele cria a estrutura inteira em segundos; revise o diff antes de
    aceitar.

## Passo 5 — Integração e Configuração da IDE

**O que é.** Configurar sua IDE (como VS Code, Antigravity, Cursor, PyCharm, etc.) para utilizar o interpretador Python correto localizado dentro do ambiente virtual criado pelo `uv` (`.venv`).

**Por que importa.** Por padrão, as IDEs tentam usar o Python global instalado na máquina. Quando isso ocorre:
1. A IDE exibe avisos falsos de erro (como `"Import could not be resolved"` em vermelho) sob as bibliotecas importadas (ex: `pandas`, `pytest`), pois ela não as encontra no Python global.
2. O preenchimento automático (autocompletion), inspeção de tipos (type hints) e o recurso de "Ir para a Definição" (Go to Definition) deixam de funcionar para os pacotes do projeto.
3. Ferramentas integradas como testes automáticos e formatadores rodam no ambiente errado ou falham.

**Como fazer.**

### 1. VS Code / Antigravity / Cursor
Como essas IDEs compartilham a mesma base e extensões, o processo é idêntico:
1. Abra a pasta raiz do projeto na IDE (`File` -> `Open Folder...`).
2. Pressione `Ctrl + Shift + P` (no Windows/Linux) ou `Cmd + Shift + P` (no macOS) para abrir a **Paleta de Comandos**.
3. Digite e selecione: **`Python: Select Interpreter`** (Selecionar Interpretador).
4. A IDE listará os interpretadores encontrados. Escolha a opção recomendada que aponta para o ambiente virtual do projeto, geralmente exibindo algo como `'venv' (./.venv/Scripts/python.exe)` no Windows ou `'venv' (./.venv/bin/python)` no macOS/Linux.
5. *(Opcional)* Para o Ruff funcionar automaticamente na IDE, instale a extensão oficial **Ruff** (da Astral Software). Configure o VS Code para formatar ao salvar adicionando a seguinte linha no seu `settings.json`:
   ```json
   "editor.formatOnSave": true,
   "editor.defaultFormatter": "charliermarsh.ruff"
   ```

### 2. PyCharm
1. Abra o projeto no PyCharm.
2. Acesse as configurações da IDE (`Settings` no Windows ou `Preferences` no macOS).
3. Navegue até **`Project: <nome-do-projeto>`** -> **`Python Interpreter`**.
4. Clique em **`Add Interpreter`** (canto superior direito da tela de seleção) -> **`Add Local Interpreter...`**.
5. Selecione **`Virtualenv Environment`** na barra lateral.
6. Escolha a opção **`Existing`** (Ambiente Existente).
7. No campo *Interpreter*, clique nos três pontos `...` e aponte para o executável do Python dentro da pasta `.venv` do projeto (ex: `.venv/Scripts/python.exe` no Windows ou `.venv/bin/python` no macOS/Linux).
8. Clique em **`OK`** e aplique as configurações.

!!! tip "Com o Claude Code"
    Peça: «me explique como configurar o VS Code para usar o ambiente virtual do uv e ativar o Ruff no salvamento». O Claude Code pode até criar ou editar o arquivo de configurações do VS Code (`.vscode/settings.json`) na raiz do seu projeto se você preferir automatizar isso.
