"""Template de teste para app.pipeline.load.

Ative este teste assim que a carga real for implementada.
"""

import pytest


def test_load_salva_arquivo_de_saida():
    """Deve salvar o DataFrame consolidado na pasta de destino."""
    # Arrange: df = pd.DataFrame({"col": [1]}); output_folder = tmp_path
    # Act: load(df, str(output_folder), "saida.xlsx")
    # Assert: assert (output_folder / "saida.xlsx").exists()
    pytest.skip("TODO: implemente load() e habilite este teste.")
