"""Etapa de carga (Load) do pipeline.

Ponto de partida genérico: adapte para o destino real do seu projeto
(arquivo local, banco de dados, data lake, API, etc.).
"""

from pathlib import Path

import pandas as pd


def load(df: pd.DataFrame, output_folder: str, filename: str) -> None:
    """Salva o DataFrame consolidado no destino de saída.

    Args:
        df: DataFrame consolidado, vindo da etapa de transformação.
        output_folder: pasta de destino (criada automaticamente se não existir).
        filename: nome do arquivo de saída (ex.: "consolidado.xlsx").
    """
    # TODO: substitua pela carga real do seu projeto, por exemplo:
    #   Path(output_folder).mkdir(parents=True, exist_ok=True)
    #   df.to_excel(Path(output_folder) / filename, index=False)
    raise NotImplementedError(
        f"Implemente a carga dos dados para '{Path(output_folder) / filename}'."
    )
