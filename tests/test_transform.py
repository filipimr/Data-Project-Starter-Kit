"""Template de teste para app.pipeline.transform.

Ative este teste assim que a transformação real for implementada.
"""

import pytest


def test_transform_concatena_dataframes():
    """Deve consolidar a lista de DataFrames em um único DataFrame."""
    # Arrange: df1 = pd.DataFrame({"col": [1, 2]}); df2 = pd.DataFrame({"col": [3]})
    # Act: resultado = transform([df1, df2])
    # Assert: assert resultado.shape[0] == 3
    pytest.skip("TODO: implemente transform() e habilite este teste.")
