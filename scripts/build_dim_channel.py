import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
RAW = BASE_DIR / "RAW"
DW = BASE_DIR / "DW"
DW.mkdir(exist_ok=True)

# --- LECTURA ---
df = pd.read_csv(RAW / "channel.csv")

# --- LIMPIEZA BÁSICA ---
for col in ["code", "name"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# --- CLAVE SURROGATE ---
df.insert(0, "channel_sk", range(1, len(df) + 1))

# --- ORDEN FINAL DE COLUMNAS ---
cols = ["channel_sk", "channel_id", "code", "name"]
df = df[cols]

# --- EXPORTAR ---
df.to_csv(DW / "dim_channel.csv", index=False)
print("✅ dim_channel creada en /DW/dim_channel.csv")
