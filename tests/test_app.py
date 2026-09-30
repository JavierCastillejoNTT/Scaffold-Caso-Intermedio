import os
import sys

import pytest
import pandas as pd

from basicengine.utils.funciones import (
    crear_cubo_clientes,
    crear_rangos_edad,
    unir_productos_planuno,
    unir_transacciones_ficha,
)


@pytest.fixture(scope="session")

def test_unir_productos_planuno():
    productos = pd.DataFrame(
        [
            (1, "0182", "ES", 10),
            (2, "0182", "ES", 20),
        ],
        [
            "customer_id",
            "entity_id",
            "country_id",
            "document_cr_movement_number",
        ],
    )

    plan_uno = pd.DataFrame(
        [
            (1, "0182", "ES", 25),
            (3, "0182", "ES", 40),
        ],
        [
            "customer_id",
            "entity_id",
            "country_id",
            "age_number",
        ],
    )

    resultado = unir_productos_planuno(productos, plan_uno).collect()

    assert len(resultado) == 1
    assert resultado[0].customer_id == 1
    assert resultado[0].age_number == 25


def test_unir_transacciones_ficha():
    transacciones = pd.DataFrame(
        [
            (1, "0001", "0182", "ES", "BASICO", "0100", "2529"),
            (2, "0002", "0182", "ES", "PREMIUM", "0200", "2530"),
        ],
        columns=[
            "customer_id",
            "main_office_id",
            "entity_id",
            "country_id",
            "segment_global_group_desc",
            "main_branch_id",
            "level50_territorial_id",
        ],
    )

    fichas = pd.DataFrame(
        [
            (1, "0001"),
        ],
        columns=[
            "customer_id",
            "main_office_id",
        ],
    )

    resultado = unir_transacciones_ficha(
        transacciones,
        fichas,
    )

    filas = list(resultado.itertuples(index=False))

    assert len(filas) == 1
    assert filas[0].customer_id == 1
    assert "segment_global_group_desc" not in resultado.columns
    assert "main_branch_id" not in resultado.columns


@pytest.mark.parametrize(
    ("edad", "categoria"),
    [
        (10, "menor de edad"),
        (20, "joven"),
        (30, "joven adulto"),
        (40, "adulto"),
        (60, "comienzo vejez"),
        (75, "jubilado"),
        (100, "fuera de rango"),
    ],
)
def test_crear_rangos_edad(edad, categoria):
    datos = pd.DataFrame(
        [(1, edad)],
        columns=["customer_id", "age_number"],
    )

    resultado = list(crear_rangos_edad(datos).itertuples(index=False))

    assert resultado[0].age_group == categoria


def test_crear_cubo_clientes():
    productos = pd.DataFrame(
        [(1, "0182", "ES", 10)],
        columns=[
            "customer_id",
            "entity_id",
            "country_id",
            "document_cr_movement_number",
        ],
    )

    plan_uno = pd.DataFrame(
        [(1, "0182", "ES", 40, "A", "8", "BASICO", "0100")],
        columns=[
            "customer_id",
            "entity_id",
            "country_id",
            "age_number",
            "status_type",
            "global_segment_id",
            "segment_global_group_desc",
            "main_branch_id",
        ],
    )

    transacciones = pd.DataFrame(
        [(1, "0001", "0182", "ES", "OTRO", "9999", "2529")],
        columns=[
            "customer_id",
            "main_office_id",
            "entity_id",
            "country_id",
            "segment_global_group_desc",
            "main_branch_id",
            "level50_territorial_id",
        ],
    )

    fichas = pd.DataFrame(
        [(1, "0001")],
        columns=["customer_id", "main_office_id"],
    )

    resultado = crear_cubo_clientes(
        productos,
        plan_uno,
        transacciones,
        fichas,
    )

    filas = list(resultado.itertuples(index=False))
    fila = filas[0]

    assert fila.customer_id == 1
    assert fila.age_group == "adulto"
    assert fila.level50_territorial_id == "2529"
    assert fila.segment_global_group_desc == "BASICO"
