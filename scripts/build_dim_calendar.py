import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
DW = BASE_DIR / "DW"
DW.mkdir(exist_ok=True)

# --- GENERAR RANGO DE FECHAS ---
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
df = pd.DataFrame({"date": dates})

# --- ATRIBUTOS DERIVADOS ---
df["date_sk"] = df["date"].dt.strftime("%Y%m%d").astype(int)
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["month_name"] = df["date"].dt.strftime("%B")
df["day"] = df["date"].dt.day
df["day_of_week"] = df["date"].dt.weekday + 1      # 1=Lunes, 7=Domingo
df["day_name"] = df["date"].dt.strftime("%A")
df["week_of_year"] = df["date"].dt.isocalendar().week
df["quarter"] = df["date"].dt.quarter
df["is_weekend"] = df["day_of_week"].isin([6, 7]).astype(int)

# --- ORDEN FINAL ---
cols = [
    "date_sk", "date", "year", "month", "month_name", "day",
    "day_of_week", "day_name", "week_of_year", "quarter", "is_weekend"
]
df = df[cols]

# --- EXPORTAR ---
df.to_csv(DW / "dim_calendar.csv", index=False)
print("✅ dim_calendar creada en /DW/dim_calendar.csv (2023 completo, granularidad diaria)")
