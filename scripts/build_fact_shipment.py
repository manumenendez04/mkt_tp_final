import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
RAW = BASE_DIR / "RAW"
DW = BASE_DIR / "DW"
DW.mkdir(exist_ok=True)

# --- LECTURA ---
df = pd.read_csv(RAW / "shipment.csv", parse_dates=["shipped_at", "delivered_at"])

# --- LIMPIEZA BÁSICA ---
for col in ["carrier", "tracking_number", "status"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# --- CLAVE SURROGATE ---
df.insert(0, "shipment_sk", range(1, len(df) + 1))

# --- CÁLCULOS DE MÉTRICAS ---
# Tiempo de entrega (en días)
df["delivery_time_days"] = (df["delivered_at"] - df["shipped_at"]).dt.days

# --- ORDEN FINAL DE COLUMNAS ---
cols = [
    "shipment_sk", "shipment_id", "order_id",
    "carrier", "tracking_number", "status",
    "shipped_at", "delivered_at", "delivery_time_days"
]
df = df[cols]

# --- EXPORTAR ---
df.to_csv(DW / "fact_shipment.csv", index=False)
print("✅ fact_shipment creada en /DW/fact_shipment.csv")
