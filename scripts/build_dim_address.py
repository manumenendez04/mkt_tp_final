import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
RAW = BASE_DIR / "RAW"
DW = BASE_DIR / "DW"
DW.mkdir(exist_ok=True)

# --- LECTURA ---
df = pd.read_csv(RAW / "address.csv", parse_dates=["created_at"])

# --- LIMPIEZA BÁSICA ---
for col in ["line1", "line2", "city", "postal_code", "country_code"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# --- CLAVE SURROGATE ---
df.insert(0, "address_sk", range(1, len(df) + 1))

# --- ORDEN FINAL DE COLUMNAS ---
cols = [
    "address_sk", "address_id", "line1", "line2", "city",
    "province_id", "postal_code", "country_code", "created_at"
]
df = df[cols]

# --- EXPORTAR ---
df.to_csv(DW / "dim_address.csv", index=False)
print("✅ dim_address creada en /DW/dim_address.csv")
