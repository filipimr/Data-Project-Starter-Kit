"""Etapa de transformação (Transform) do pipeline.

Ponto de partida genérico: adapte para as regras de negócio reais do seu
projeto (limpeza, junção, agregação, validação, etc.).
"""

import pandas as pd


def transform(dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    """Aplica as regras de transformação e consolida os dados recebidos.

    Args:
        dataframes: lista de DataFrames vindos da etapa de extração.

    Returns:
        Um único DataFrame consolidado, pronto para a etapa de carga.
    """
    # TODO: substitua pela transformação real do seu projeto, por exemplo:
    #   return pd.concat(dataframes, ignore_index=True)
    raise NotImplementedError(
        f"Implemente a transformação para os {len(dataframes)} DataFrame(s) recebidos."
    )
