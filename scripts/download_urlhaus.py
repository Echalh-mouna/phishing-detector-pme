"""
Jalon 1 - Telechargement des URLs malveillantes depuis URLhaus (abuse.ch)
--------------------------------------------------------------------------
Ce script telecharge le flux CSV public d'URLhaus (URLs malveillantes
recentes) et l'enregistre localement pour pouvoir l'explorer avec pandas.

Source : https://urlhaus.abuse.ch/downloads/csv_recent/
Aucune cle API n'est necessaire pour ce flux.
"""

import io
from datetime import datetime

import pandas as pd
import requests

# URL du flux CSV "recent" d'URLhaus (URLs ajoutees dans les 30 derniers jours)
URLHAUS_CSV_URL = "https://urlhaus.abuse.ch/downloads/csv_recent/"

# Noms des colonnes du CSV (le fichier commence par des lignes de commentaire
# qui debutent par '#', on les ignore avec comment="#")
COLUMN_NAMES = [
    "id",
    "dateadded",
    "url",
    "url_status",
    "last_online",
    "threat",
    "tags",
    "urlhaus_link",
    "reporter",
]


def telecharger_urls_urlhaus() -> pd.DataFrame:
    """Telecharge le CSV URLhaus et le retourne sous forme de DataFrame pandas."""
    print(f"Telechargement depuis {URLHAUS_CSV_URL} ...")
    reponse = requests.get(URLHAUS_CSV_URL, timeout=30)
    reponse.raise_for_status()  # leve une erreur si le telechargement echoue

    # Le fichier contient des lignes d'en-tete commencant par '#' a ignorer
    df = pd.read_csv(
        io.StringIO(reponse.text),
        comment="#",
        names=COLUMN_NAMES,
        quotechar='"',
    )
    return df


def resumer(df: pd.DataFrame) -> None:
    """Affiche un petit resume des donnees telechargees."""
    print(f"\nNombre total d'URLs recuperees : {len(df)}")
    print(f"Colonnes disponibles : {list(df.columns)}")

    print("\nRepartition par type de menace (threat) :")
    print(df["threat"].value_counts())

    print("\nRepartition par statut (en ligne / hors ligne) :")
    print(df["url_status"].value_counts())

    print("\nExemple des 5 premieres lignes :")
    print(df[["dateadded", "url", "threat", "url_status"]].head())


def sauvegarder(df: pd.DataFrame) -> str:
    """Sauvegarde les donnees dans un fichier CSV local horodate."""
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"urlhaus_urls_{horodatage}.csv"
    df.to_csv(nom_fichier, index=False)
    return nom_fichier


if __name__ == "__main__":
    donnees = telecharger_urls_urlhaus()
    resumer(donnees)
    fichier = sauvegarder(donnees)
    print(f"\nDonnees sauvegardees dans : {fichier}")