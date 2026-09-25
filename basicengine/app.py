import json
from pathlib import Path

from pyspark.sql import SparkSession

from basicengine.utils.funciones import crear_cubo_clientes


def cargar_configuracion(config_path: Path) -> dict:
    """Carga las rutas de entrada y salida del engine."""
    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def ejecutar_engine(config_path: Path | None = None) -> None:
    """Lee los datos, ejecuta las transformaciones y guarda el resultado."""
    project_path = Path(__file__).resolve().parent.parent

    if config_path is None:
        config_path = project_path / "resources" / "application.conf"

    config = cargar_configuracion(config_path)

    input_path = project_path / config["INPUT_PATH"]
    output_path = project_path / config["OUTPUT_PATH"]

    try:
        print("1. Leyendo datos de entrada")

        df_productos = spark.read.csv(
            str(input_path / "productos.csv"),
            header=True,
            inferSchema=True,
        )

        df_plan_uno = spark.read.csv(
            str(input_path / "plan_uno.csv"),
            header=True,
            inferSchema=True,
        )

        df_transac = spark.read.csv(
            str(input_path / "transac.csv"),
            header=True,
            inferSchema=True,
        )

        df_fich = spark.read.csv(
            str(input_path / "fich.csv"),
            header=True,
            inferSchema=True,
        )

        print("2. Creando cubo de clientes")

        df_cubo = crear_cubo_clientes(
            df_productos,
            df_plan_uno,
            df_transac,
            df_fich,
        )

        print("3. Guardando resultado")

        df_cubo.write.mode("overwrite").parquet(
            str(output_path / "cubo_final"),
        )

        print("Proceso terminado correctamente")
    finally:
        spark.stop()


if __name__ == "__main__":
    ejecutar_engine()
