import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
RAW = BASE_DIR / "RAW"
DW = BASE_DIR / "DW"
DW.mkdir(exist_ok=True)

# --- LECTURA DE CSV ---
product = pd.read_csv(RAW / "product.csv", parse_dates=["created_at"])
category = pd.read_csv(RAW / "product_category.csv")

# --- LIMPIEZA BÁSICA ---
for df in [product, category]:
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

# --- JOIN ENTRE PRODUCT Y CATEGORY ---
df = product.merge(category, how="left", on="category_id", suffixes=("", "_category"))

# --- CREAR CLAVE SURROGATE ---
df.insert(0, "product_sk", range(1, len(df) + 1))

# --- ORDEN FINAL DE COLUMNAS ---
cols = [
    "product_sk", "product_id", "sku", "name", "category_id",
    "name_category", "parent_id", "list_price", "status", "created_at"
]
df = df[cols]

# --- EXPORTAR A CSV ---
df.to_csv(DW / "dim_product.csv", index=False)
print("✅ dim_product creada en /DW/dim_product.csv (unifica producto + categoría)")
