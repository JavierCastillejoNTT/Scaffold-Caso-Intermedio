#Scaffold intermedio

Proyecto PySpark basado en el Caso de Uso 4 del laboratorio.

El engine:

1. Lee información de productos, Plan Uno, transacciones y fichas.
2. Une los datos mediante identificadores de cliente.
3. Clasifica a los clientes por rango de edad.
4. Genera un cubo final en formato Parquet.

## Estructura

- `scafoldintermedio/app.py`: punto de entrada.
- `scafoldintermedio/utils/funciones.py`: transformaciones PySpark.
- `tests/test_app.py`: tests unitarios.
- `resources/application.conf`: configuración de rutas.
- `data/input`: datos de entrada locales.
- `data/output`: resultados generados.
