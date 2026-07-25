# Jalon 1 – Détection des URLs malveillantes

## Description

Ce projet constitue le premier jalon du stage PFA portant sur le développement d'un système de détection et d'alerte précoce des cybermenaces ciblant les PME.

L'objectif de ce premier jalon est de :

- Comprendre les notions de phishing et d'URL malveillante.
- Installer l'environnement de développement Python.
- Développer un premier script permettant de télécharger des URLs malveillantes depuis URLhaus.

---

## Structure du projet

```
Jalon1/
│
├── README.md
├── Note_phishing.pdf
├── Note_phishing.odt
│
├── scripts/
│   ├── download_urlhaus.py
│   ├── requirements.txt
│   └── data/
│       └── urlhaus_urls_20260718_160840.csv
│
└── venv/        (ou .venv)
```

---

## Prérequis

- Python 3.x
- pip

---

## Installation

Créer un environnement virtuel :

```bash
python -m venv venv
```

Activer l'environnement :

### Windows

```bash
venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## Exécution

Lancer le script :

```bash
python download_urlhaus.py
```

Le script :

- télécharge les URLs malveillantes depuis URLhaus ;
- charge les données avec pandas ;
- affiche un résumé des données ;
- sauvegarde les résultats dans un fichier CSV.

---

## Ressources

- URLhaus (abuse.ch) : https://urlhaus.abuse.ch

---

## Auteur

Projet réalisé dans le cadre du stage PFA 2026.