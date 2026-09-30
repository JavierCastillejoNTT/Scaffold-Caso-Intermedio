import pandas as pd
import numpy as np

JOIN_KEYS = ["customer_id", "entity_id", "country_id"]

OUTPUT_COLUMNS = [
    "customer_id",
    "entity_id",
    "country_id",
    "age_group",
    "level50_territorial_id",
    "status_type",
    "global_segment_id",
    "segment_global_group_desc",
    "main_branch_id",
]


def unir_productos_planuno(
    df_productos: pd.DataFrame,
    df_plan_uno: pd.DataFrame,
) -> pd.DataFrame:
    """Une la información de productos con la información de Plan Uno."""
    return df_productos.merge(
        df_plan_uno,
        on=JOIN_KEYS,
        how="inner",
    )


def unir_transacciones_ficha(
    df_transac: pd.DataFrame,
    df_fich: pd.DataFrame,
) -> pd.DataFrame:
    """Conserva las transacciones que tienen correspondencia en la ficha."""
    df_transac_fich = df_transac.merge(
        df_fich,
        on=["customer_id", "main_office_id"],
        how="inner",
    )

    return df_transac_fich.drop(
        columns=["segment_global_group_desc", "main_branch_id"]
    )


def crear_rangos_edad(df: pd.DataFrame) -> pd.DataFrame:
    """Clasifica a cada cliente según su edad."""

    conditions = [
        df["age_number"].between(0, 17),
        df["age_number"].between(18, 25),
        df["age_number"].between(26, 35),
        df["age_number"].between(36, 50),
        df["age_number"].between(51, 65),
        df["age_number"].between(66, 90),
    ]

    values = [
        "menor de edad",
        "joven",
        "joven adulto",
        "adulto",
        "comienzo vejez",
        "jubilado",
    ]

    df["age_group"] = np.select(
        conditions,
        values,
        default="fuera de rango",
    )

    return df


def crear_cubo_clientes(
    df_productos: pd.DataFrame,
    df_plan_uno: pd.DataFrame,
    df_transac: pd.DataFrame,
    df_fich: pd.DataFrame,
) -> pd.DataFrame:
    """Ejecuta las transformaciones y genera el cubo final de clientes."""
    df_producto_plan_uno = unir_productos_planuno(
        df_productos,
        df_plan_uno,
    )

    df_transac_fich = unir_transacciones_ficha(
        df_transac,
        df_fich,
    )

    df_final = df_producto_plan_uno.merge(
        df_transac_fich,
        on=JOIN_KEYS,
        how="inner",
    )

    df_final = crear_rangos_edad(df_final)

    return df_final[OUTPUT_COLUMNS]
