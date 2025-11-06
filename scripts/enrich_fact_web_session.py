import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
DW = BASE_DIR / "DW"

# --- LECTURA ---
fact = pd.read_csv(DW / "fact_web_session.csv", parse_dates=["started_at", "ended_at"])
dim_customer = pd.read_csv(DW / "dim_customer.csv")
dim_calendar = pd.read_csv(DW / "dim_calendar.csv", parse_dates=["date"])

# --- MAPEO CUSTOMER ---
fact = fact.merge(
    dim_customer[["customer_id", "customer_sk"]],
    how="left",
    on="customer_id"
)

# --- MAPEO FECHAS (inicio y fin de sesión) ---
fact["start_date_norm"] = fact["started_at"].dt.normalize()
fact["end_date_norm"] = fact["ended_at"].dt.normalize()

# Join con calendario para obtener surrogate keys
fact = fact.merge(
    dim_calendar[["date", "date_sk"]].rename(columns={"date_sk": "start_date_sk"}),
    how="left", left_on="start_date_norm", right_on="date"
).drop(columns=["date"])

fact = fact.merge(
    dim_calendar[["date", "date_sk"]].rename(columns={"date_sk": "end_date_sk"}),
    how="left", left_on="end_date_norm", right_on="date"
).drop(columns=["date"])

# --- COMPLETAR NULOS (late-arriving) ---
for col in ["customer_sk", "start_date_sk", "end_date_sk"]:
    fact[col] = fact[col].fillna(0).astype(int)

# --- SELECCIÓN FINAL ---
cols = [
    "session_sk", "session_id",
    "customer_sk", "start_date_sk", "end_date_sk",
    "source", "device", "session_duration_min"
]
fact = fact[cols]

# --- EXPORTAR ---
fact.to_csv(DW / "fact_web_session_enriched.csv", index=False)
print("✅ fact_web_session_enriched creada en /DW/fact_web_session_enriched.csv")
