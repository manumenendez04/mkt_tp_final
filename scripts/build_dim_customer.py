import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
RAW = BASE_DIR / "RAW"
DW = BASE_DIR / "DW"
DW.mkdir(exist_ok=True)

# --- LECTURA ---
df = pd.read_csv(RAW / "customer.csv", parse_dates=["created_at"])

# --- LIMPIEZA BÁSICA ---
# Quitar espacios y normalizar textos
for col in ["email", "first_name", "last_name", "phone", "status"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# --- CREAR CLAVE SURROGATE ---
df.insert(0, "customer_sk", range(1, len(df) + 1))

# --- ORDEN FINAL DE COLUMNAS ---
cols = ["customer_sk", "customer_id", "email", "first_name", "last_name",
        "phone", "status", "created_at"]
df = df[cols]

# --- EXPORTAR ---
df.to_csv(DW / "dim_customer.csv", index=False)
print("✅ dim_customer creada en /DW/dim_customer.csv")