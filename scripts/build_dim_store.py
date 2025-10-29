import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
RAW = BASE_DIR / "RAW"
DW = BASE_DIR / "DW"
DW.mkdir(exist_ok=True)

# --- LECTURA ---
df = pd.read_csv(RAW / "store.csv")

# --- LIMPIEZA BÁSICA ---
for col in ["name"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# --- CLAVE SURROGATE ---
df.insert(0, "store_sk", range(1, len(df) + 1))

# --- ORDEN FINAL DE COLUMNAS ---
cols = ["store_sk", "store_id", "name", "address_id"]
df = df[cols]

# --- EXPORTAR ---
df.to_csv(DW / "dim_store.csv", index=False)
print("✅ dim_store creada en /DW/dim_store.csv")
