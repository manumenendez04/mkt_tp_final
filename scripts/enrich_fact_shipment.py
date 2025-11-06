import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
DW = BASE_DIR / "DW"

# --- LECTURA ---
fact_ship = pd.read_csv(DW / "fact_shipment.csv", parse_dates=["shipped_at", "delivered_at"])
fact_order = pd.read_csv(DW / "fact_order_item_enriched.csv")  # ya tiene customer_sk, channel_sk, store_sk
dim_calendar = pd.read_csv(DW / "dim_calendar.csv", parse_dates=["date"])

# --- LOOKUP POR order_id (contexto cliente/canal/tienda) ---
order_lookup = fact_order.drop_duplicates(subset=["order_id"])[
    ["order_id", "customer_sk", "channel_sk", "store_sk"]
]
fact_ship = fact_ship.merge(order_lookup, how="left", on="order_id")

# --- MAPEO FECHAS A dim_calendar ---
fact_ship["shipped_date_norm"]   = fact_ship["shipped_at"].dt.normalize()
fact_ship["delivered_date_norm"] = fact_ship["delivered_at"].dt.normalize()

fact_ship = fact_ship.merge(
    dim_calendar[["date", "date_sk"]].rename(columns={"date_sk": "shipped_date_sk"}),
    how="left", left_on="shipped_date_norm", right_on="date"
).drop(columns=["date"])

fact_ship = fact_ship.merge(
    dim_calendar[["date", "date_sk"]].rename(columns={"date_sk": "delivered_date_sk"}),
    how="left", left_on="delivered_date_norm", right_on="date"
).drop(columns=["date"])

# --- COMPLETAR NULOS (late-arriving) ---
for c in ["customer_sk", "channel_sk", "store_sk", "shipped_date_sk", "delivered_date_sk"]:
    fact_ship[c] = fact_ship[c].fillna(0).astype(int)

# --- SELECCIÓN FINAL ---
cols = [
    "shipment_sk", "shipment_id", "order_id",
    "customer_sk", "channel_sk", "store_sk",
    "shipped_date_sk", "delivered_date_sk",
    "carrier", "tracking_number", "status",
    "shipped_at", "delivered_at", "delivery_time_days"
]
fact_ship = fact_ship[cols]

# --- EXPORTAR ---
fact_ship.to_csv(DW / "fact_shipment_enriched.csv", index=False)
print("✅ fact_shipment_enriched creada en /DW/fact_shipment_enriched.csv")
