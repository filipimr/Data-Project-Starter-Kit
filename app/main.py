"""Ponto de entrada do pipeline: orquestra extract -> transform -> load."""

from app.pipeline.extract import extract
from app.pipeline.transform import transform
from app.pipeline.load import load

if __name__ == "__main__":
    dataframes = extract("data/input")
    df = transform(dataframes)
    load(df, "data/output", "consolidado.xlsx")
