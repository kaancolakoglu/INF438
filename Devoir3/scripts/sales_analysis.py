#!/usr/bin/env python3
"""Analyse et visualisation des ventes depuis un bucket S3.

Étapes prises en charge :
1. Connexion S3 et téléchargement du fichier JSON.
2. Chargement et préparation des données dans un DataFrame pandas.
3. Analyses statistiques (résumé, agrégations, distributions).
4. Création d'un dashboard (4 graphiques) enregistré dans sales_analysis.png.

Variables d'environnement requises :
- S3_BUCKET_NAME : Nom du bucket S3
- S3_OBJECT_KEY : Clé objet dans le bucket S3
- AWS_REGION : Région AWS (optionnel)
- OUTPUT_PATH : Chemin de sortie du dashboard PNG (défaut: plots/sales_analysis.png)
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
from io import BytesIO
from typing import Iterable, List, Tuple

import boto3
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv


def download_json_bytes(bucket: str, key: str, region: str | None) -> bytes:
    session = (
        boto3.session.Session(region_name=region)
        if region
        else boto3.session.Session()
    )
    s3_client = session.client("s3")
    buffer = BytesIO()
    s3_client.download_fileobj(bucket, key, buffer)
    buffer.seek(0)
    return buffer.read()


def load_records(raw_bytes: bytes) -> List[dict]:
    records: List[dict] = []
    for line in raw_bytes.decode("utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))
    if not records:
        raise ValueError("Le fichier JSON ne contient aucune donnée exploitable.")
    return records


def prepare_dataframe(records: Iterable[dict]) -> pd.DataFrame:
    df = pd.DataFrame(records)

    if "price" not in df.columns and "unitPrice" in df.columns:
        df["price"] = df["unitPrice"]

    if "totalPrice" not in df.columns:
        df["totalPrice"] = df["price"] * df["quantity"]
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], downcast="integer", errors="coerce")
    df["totalPrice"] = pd.to_numeric(df["totalPrice"], errors="coerce")
    df.dropna(subset=["price", "quantity", "totalPrice"], inplace=True)
    df["quantity"] = df["quantity"].astype(int)
    df["price"] = df["price"].astype(float)
    df["totalPrice"] = df["totalPrice"].astype(float)
    return df


def run_statistical_analyses(
    df: pd.DataFrame,
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    print("\n=== Résumé statistique ===")
    summary = df[["price", "quantity", "totalPrice"]].describe(percentiles=[0.5])
    print(summary)

    city_sales = df.groupby("city")["totalPrice"].sum().sort_values(ascending=False)
    print("\n=== Ventes totales par ville ===")
    print(city_sales.to_frame(name="totalPrice"))

    top_products = df["productName"].value_counts().head(5)
    print("\n=== Top 5 des produits les plus vendus (nombre de commandes) ===")
    print(top_products.to_frame(name="count"))

    status_distribution = df["status"].value_counts()
    print("\n=== Distribution des statuts de commande ===")
    print(status_distribution.to_frame(name="count"))

    country_sales = df.groupby("country")["totalPrice"].sum().sort_values(ascending=False)
    print("\n=== Ventes totales par pays ===")
    print(country_sales.to_frame(name="totalPrice"))

    return city_sales, top_products, status_distribution, country_sales


def build_dashboard(
    city_sales: pd.Series,
    top_products: pd.Series,
    status_distribution: pd.Series,
    country_sales: pd.Series,
    output_path: pathlib.Path,
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Sales Analysis Dashboard", fontsize=16, fontweight="bold")

    city_sales.head(10).plot(
        kind="bar",
        ax=axes[0, 0],
        color="#1f77b4",
    )
    axes[0, 0].set_title("Top 10 des villes par ventes")
    axes[0, 0].set_ylabel("Ventes totales")

    top_products.head(5).plot(kind="bar", ax=axes[0, 1], color="#ff7f0e")
    axes[0, 1].set_title("Top 5 produits (commandes)")
    axes[0, 1].set_ylabel("Nombre de commandes")

    axes[1, 0].pie(
        status_distribution,
        labels=status_distribution.index,
        autopct="%1.1f%%",
        startangle=140,
    )
    axes[1, 0].set_title("Distribution des statuts")

    country_sales.plot(kind="bar", ax=axes[1, 1], color="#2ca02c")
    axes[1, 1].set_title("Ventes par pays")
    axes[1, 1].set_ylabel("Ventes totales")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    print(f"\nDashboard enregistré dans {output_path.resolve()}")


def main() -> None:
    load_dotenv()

    bucket = os.getenv("S3_BUCKET_NAME")
    key = os.getenv("S3_OBJECT_KEY")
    region = os.getenv("AWS_REGION")

    if not bucket or not key:
        raise ValueError(
            "Bucket et clé S3 requis. Configurez S3_BUCKET_NAME et S3_OBJECT_KEY dans les variables d'environnement."
        )

    raw_bytes = download_json_bytes(bucket, key, region)

    records = load_records(raw_bytes)
    df = prepare_dataframe(records)
    stats = run_statistical_analyses(df)

    default_output = os.path.join("Devoir3/plots", "sales_analysis.png")
    output_path = pathlib.Path(os.getenv("OUTPUT_PATH", default_output))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    build_dashboard(*stats, output_path)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        sys.exit(1)
