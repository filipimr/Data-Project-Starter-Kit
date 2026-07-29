# Bloco 2 — Escrevendo o código de forma profissional

Com o ambiente pronto, o código em si muda de qualidade quando você o
escreve de forma modular, documentada e reutilizável.

## Passo 5 — Modularize em funções pequenas

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

## Passo 6 — Docstrings e type hints

**O que é.** Uma docstring é a documentação embutida logo abaixo da
definição da função. [Type hints](https://docs.python.org/3/library/typing.html)
(`input_folder: str`, `-> list[pd.DataFrame]`) declaram os tipos de entrada
e saída.

**Por que importa.** Documentar antes de escrever ajuda a pensar: quais
argumentos a função recebe? O que retorna? O que ela faz? Quando outra
pessoa (ou uma IA) for usar sua função, ela lê a docstring e sabe o que
passar, sem abrir o código. Mais para a frente, a documentação do projeto é
gerada automaticamente a partir dessas docstrings (Passo 11, em
[Documentação viva](documentacao.md)).

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

Você pode cobrar docstrings automaticamente: o Ruff (Passo 9, em
[Garantia de qualidade](qualidade.md)) tem as regras `D` (equivalentes ao
pydocstyle) que apontam funções sem documentação e fora da convenção.

!!! tip "Com o Claude Code"
    Peça: «adicione docstrings (estilo Google) e type hints em todas as
    funções públicas deste módulo». Docstrings bem escritas viram
    documentação automática no Passo 11 — vale caprichar.

## Passo 7 — Pacotes e o `if __name__ == "__main__"`

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
