import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
RAW = BASE_DIR / "RAW"
DW = BASE_DIR / "DW"
DW.mkdir(exist_ok=True)

# --- LECTURA ---
df = pd.read_csv(RAW / "nps_response.csv", parse_dates=["responded_at"])

# --- LIMPIEZA BÁSICA ---
for col in ["comment"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# --- CLAVE SURROGATE ---
df.insert(0, "nps_sk", range(1, len(df) + 1))

# --- VALIDACIONES Y CÁLCULOS ---
df["score"] = df["score"].astype(float).fillna(0)
df["comment_length"] = df["comment"].apply(lambda x: len(str(x)) if pd.notna(x) else 0)

# --- ORDEN FINAL DE COLUMNAS ---
cols = [
    "nps_sk", "nps_id", "customer_id", "channel_id",
    "score", "comment", "comment_length", "responded_at"
]
df = df[cols]

# --- EXPORTAR ---
df.to_csv(DW / "fact_nps_response.csv", index=False)
print("✅ fact_nps_response creada en /DW/fact_nps_response.csv")
