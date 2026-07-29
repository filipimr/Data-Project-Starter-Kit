"""Etapa de extração (Extract) do pipeline.

Ponto de partida genérico: adapte para a fonte real do seu projeto
(arquivos locais, banco de dados, API, data lake, etc.).
"""

from pathlib import Path

import pandas as pd


def extract(input_folder: str) -> list[pd.DataFrame]:
    """Lê os dados de origem e retorna uma lista de DataFrames.

    Args:
        input_folder: caminho da pasta contendo os arquivos de origem.

    Returns:
        Uma lista de DataFrames, um por arquivo/fonte lida.
    """
    # TODO: substitua pela extração real do seu projeto, por exemplo:
    #   files = Path(input_folder).glob("*.xlsx")
    #   return [pd.read_excel(file) for file in files]
    raise NotImplementedError(
        f"Implemente a extração de dados a partir de '{Path(input_folder)}'."
    )
