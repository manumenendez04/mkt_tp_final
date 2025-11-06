import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
DW = BASE_DIR / "DW"

# --- LECTURA DE TABLAS ---
fact = pd.read_csv(DW / "fact_nps_response.csv", parse_dates=["responded_at"])
dim_customer = pd.read_csv(DW / "dim_customer.csv")
dim_channel = pd.read_csv(DW / "dim_channel.csv")
dim_calendar = pd.read_csv(DW / "dim_calendar.csv", parse_dates=["date"])

# --- MAPEO CUSTOMER ---
fact = fact.merge(
    dim_customer[["customer_id", "customer_sk"]],
    how="left",
    on="customer_id"
)

# --- MAPEO CHANNEL ---
fact = fact.merge(
    dim_channel[["channel_id", "channel_sk"]],
    how="left",
    on="channel_id"
)

# --- MAPEO FECHA (responded_at → date_sk) ---
# Normalizamos las fechas al día para hacer match con dim_calendar.date
fact["responded_date"] = fact["responded_at"].dt.normalize()
fact = fact.merge(
    dim_calendar[["date", "date_sk"]],
    how="left",
    left_on="responded_date",
    right_on="date"
)
fact = fact.rename(columns={"date_sk": "responded_date_sk"})

# --- REEMPLAZAR NULOS POR 0 (si falta algún match) ---
for col in ["customer_sk", "channel_sk", "responded_date_sk"]:
    fact[col] = fact[col].fillna(0).astype(int)

# --- SELECCIÓN FINAL DE COLUMNAS ---
cols = [
    "nps_sk", "nps_id",
    "customer_sk", "channel_sk", "responded_date_sk",
    "score", "comment", "comment_length"
]
fact = fact[cols]

# --- EXPORTAR ---
fact.to_csv(DW / "fact_nps_response_enriched.csv", index=False)
print("✅ fact_nps_response_enriched creada en /DW/fact_nps_response_enriched.csv")
