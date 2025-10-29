from pathlib import Path
import pandas as pd
import numpy as np

DATA_RAW = Path(__file__).resolve().parents[1] / "RAW"
DATA_DW  = Path(__file__).resolve().parents[1] / "DW"
DATA_DW.mkdir(exist_ok=True)

def read_csv(name, parse_dates=None, dtype=None):
    df = pd.read_csv(DATA_RAW / name, dtype=dtype, parse_dates=parse_dates, keep_default_na=True, na_values=["", "null", "None"])
    # limpieza simple
    for c in df.select_dtypes(include="object"):
        df[c] = df[c].astype("string").str.strip()
    return df

def make_surrogate_keys(df, natural_col, sk_name):
    # Orden estable para reproducibilidad
    uniq = df.drop_duplicates(subset=[natural_col]).copy()
    uniq[sk_name] = np.arange(1, len(uniq) + 1, dtype="int64")
    return uniq[[natural_col, sk_name]]

def safe_join_sk(fact, dim_map, on, sk_name):
    out = fact.merge(dim_map, how="left", left_on=on, right_on=on)
    out[sk_name] = out[sk_name].fillna(0).astype("int64")  # 0 = desconocido
    return out

def write_parquet(df, name):
    df.to_parquet(DATA_DW / f"{name}.parquet", index=False)
