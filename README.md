# Trabajo Práctico Final: Dashboard Comercial para EcoBottle

Repositorio del trabajo práctico final para la materia "Introducción al Marketing Online y los Negocios Digitales". El proyecto consiste en el análisis de datos de la empresa EcoBottle, la transformación de estos con Python y la creación de un dashboard interactivo en Looker Studio.

## Caso de Uso: EcoBottle 💧

EcoBottle AR es una empresa que vende dos modelos de botellas reutilizables y opera a través de una tienda online y cuatro tiendas físicas. El objetivo de este proyecto es analizar sus datos para monitorear KPIs clave y apoyar la toma de decisiones estratégicas.

### Recursos del Proyecto 📄
* **[Consigna y documento principal](https://docs.google.com/document/d/15RMP3FvqLj04jzh80AAk6mURS00LpXLj0xqvdzrYg/edit?usp=sharing)**
* **[Diagrama Entidad Relación (DER)](./assets/DER.png)**

## Instrucciones de Ejecución ⚙️

Para replicar este proyecto y generar los archivos del Data Warehouse (`DW`), sigue estos pasos en tu terminal:

1.  **Clonar el repositorio** (usa la URL de tu propio fork):
    ```bash
    git clone https://github.com/manumenendez04/mkt_tp_final.git
    ```

2.  **Navegar a la carpeta del proyecto**:
    ```bash
    cd mkt_tp_final
    ```

3.  **Crear el entorno virtual**:
    ```bash
    python -m venv venv
    ```

4.  **Activar el entorno virtual** (en Windows con PowerShell):
    * **Paso 4.1: Permitir la ejecución de scripts.** Es posible que PowerShell bloquee la activación por seguridad. Ejecuta este comando una sola vez para permitirlo en esta sesión:
        ```powershell
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
        ```
    * **Paso 4.2: Activar el entorno.** Ahora sí, ejecuta el comando de activación:
        ```powershell
        .\venv\Scripts\activate
        ```
    * Tu terminal debería mostrar `(venv)` al principio de la línea.

5.  **Instalar las dependencias necesarias**:
    ```bash
    pip install -r requirements.txt
    ```

6.  **Ejecutar los scripts de transformación**: Ejecuta los siguientes scripts en orden para procesar los datos crudos (`RAW`) y generar los archivos finales en la carpeta `DW`.
    ```bash
    python scripts/1_calcular_ventas.py
    python scripts/2_calcular_usuarios_activos.py
    python scripts/3_calcular_ticket_promedio.py
    python scripts/4_calcular_nps.py
    python scripts/5_calcular_ventas_provincia.py
    python scripts/6_calcular_ranking_productos.py
    ```

## Dashboard Final en Looker Studio 📊

El resultado final es un tablero interactivo que permite visualizar todos los KPIs calculados. Puedes acceder al dashboard a través del siguiente enlace:

** https://lookerstudio.google.com/reporting/7418dce8-4df3-4d61-a0f1-62700e00dda9
## KPIs Calculados 📈

El dashboard presenta los siguientes Indicadores Clave de Rendimiento:

* **Ventas Totales (\$M)**: Suma del `total_amount` para todos los pedidos con estado `PAID` o `FULFILLED`.
* **Usuarios Activos (nK)**: Conteo de `customer_id` únicos por día en la tabla `web_session`.
* **Ticket Promedio (\$K)**: Resultado de dividir las ventas totales por el número total de pedidos válidos.
* **NPS (Net Promoter Score)**: Calculado como `(% de Promotores - % de Detractores)`.
* **Ventas por Provincia**: Ventas totales agrupadas por provincia.
* **Ranking de Productos**: Ventas totales por producto (`line_total`) agrupadas mensualmente.