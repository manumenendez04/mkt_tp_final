import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
RAW = BASE_DIR / "RAW"
DW = BASE_DIR / "DW"
DW.mkdir(exist_ok=True)

# --- LECTURA ---
df = pd.read_csv(RAW / "web_session.csv", parse_dates=["started_at", "ended_at"])

# --- LIMPIEZA BÁSICA ---
for col in ["source", "device"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# --- CLAVE SURROGATE ---
df.insert(0, "session_sk", range(1, len(df) + 1))

# --- CÁLCULOS DE MÉTRICAS ---
# Duración de la sesión en minutos
df["session_duration_min"] = (
    (df["ended_at"] - df["started_at"]).dt.total_seconds() / 60
).round(2)

# --- ORDEN FINAL DE COLUMNAS ---
cols = [
    "session_sk", "session_id", "customer_id",
    "started_at", "ended_at", "source", "device", "session_duration_min"
]
df = df[cols]

# --- EXPORTAR ---
df.to_csv(DW / "fact_web_session.csv", index=False)
print("✅ fact_web_session creada en /DW/fact_web_session.csv")
