# Trabajo Práctico Final: Data Warehouse y Dashboard Comercial para EcoBottle 💧

Repositorio del **trabajo práctico final** de la materia **“Introducción al Marketing Online y los Negocios Digitales”**.  
El proyecto desarrolla un proceso de **ETL con Python** para transformar datos crudos en un **Data Warehouse (DW)** estructurado y generar indicadores de desempeño comercial visualizados en un **dashboard interactivo**.

📦 **Repositorio en GitHub:**  
👉 [https://github.com/manumenendez04/mkt_tp_final](https://github.com/manumenendez04/mkt_tp_final)

---

## Caso de Uso: EcoBottle 💼

**EcoBottle AR** es una empresa dedicada a la venta de botellas reutilizables que opera mediante **una tienda online** y **cuatro tiendas físicas**.  
El objetivo principal del proyecto es **analizar las ventas y el comportamiento de los clientes** para apoyar la toma de decisiones estratégicas.

El trabajo abarca:
- Integración y limpieza de datos crudos (`RAW`).
- Generación de tablas **dimensionales y de hechos** en la carpeta `/DW`.
- Modelado de **diagramas estrella** (`Diagramas_Estrella`).
- Creación de **scripts Python** automatizados para enriquecer las tablas del DW.
- Construcción del **dashboard final en Looker Studio**.


---

## Estructura del Proyecto 📂

mkt_tp_final/
│
├── DW/ # Data Warehouse final (CSV enriquecidos)
│ ├── fact_order_item_enriched.csv
│ ├── fact_payment_enriched.csv
│ ├── fact_shipment_enriched.csv
│ ├── fact_web_session_enriched.csv
│ ├── fact_nps_response_enriched.csv
│ └── dim_calendar.csv
│
├── Diagramas_Estrella/ # Diagramas PNG del modelo estrella
│ ├── Enrich-fact_web_session.png
│ ├── NPS_Response_Fact.png
│ ├── Order_Item_Fact.png
│ ├── Payment_Fact.png
│ └── Shipment_Fact.png
│
├── scripts/ # Scripts Python de transformación (ETL)
│ ├── build_dim_calendar.py
│ ├── enrich_fact_order_item.py
│ ├── enrich_fact_payment.py
│ ├── enrich_fact_shipment.py
│ ├── enrich_fact_web_session.py
│ └── enrich_fact_nps_response.py
│
├── raw/ # Datos crudos originales
│
├── assets/ # Recursos gráficos o auxiliares
│
├── requirements.txt # Librerías necesarias
├── LICENSE # Licencia MIT
└── README.md # Este archivo