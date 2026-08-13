# Jalon 2 — Construire un premier détecteur de phishing

## Objectif global

Ce jalon vise à entraîner un premier modèle de Machine Learning capable de reconnaître une URL de phishing à partir d'un jeu de données déjà étiqueté. L'objectif n'est pas de produire un modèle optimisé ou complexe, mais de valider une démarche complète et rigoureuse : préparation des données, séparation entraînement/test, entraînement d'un modèle simple, et lecture critique des résultats obtenus.

## Datasets suggérées

Plusieurs jeux de données ont été envisagés pour ce jalon :

| Dataset | Contenu | Taille |
|---|---|---|
| UCI Phishing Websites Data Set | 30 caractéristiques extraites + label | 11 055 échantillons |
| Web Page Phishing Detection Dataset (Kaggle) | 87 caractéristiques + label | ~11 430 URLs |
| Phishing URL Detection (Kaggle) | Caractéristiques d'URL + label | 500 000+ URLs |
| Malicious and Benign URLs Dataset (Kaggle) | URLs et/ou caractéristiques | Variable |
| PhishTank Dataset (communauté) | URLs de phishing uniquement | Variable |

## Dataset retenu

**Web Page Phishing Detection Dataset** (Kaggle, Hannousse & Yahiouche) — 87 caractéristiques, 11 430 URLs, réparti équitablement entre pages légitimes et pages de phishing.

Source : https://www.kaggle.com/datasets/shashwatwork/web-page-phishing-detection-dataset

## Justification du choix

- **Équilibré** : autant d'exemples légitimes que de phishing, ce qui évite un biais du modèle vers une classe majoritaire.
- **Déjà étiqueté** : chaque ligne contient une colonne `status` (legitimate / phishing), indispensable pour un apprentissage supervisé.
- **Format directement exploitable** : les caractéristiques sont déjà calculées (pas besoin de les extraire manuellement à partir des URLs brutes).
- **Taille raisonnable** pour un entraînement rapide avec un modèle simple, sans besoin d'infrastructure lourde.

Un sous-ensemble de PhishTank a également été écarté pour ce jalon : cette source fournit des URLs de phishing réelles et à jour, mais sans caractéristiques pré-calculées ni exemples légitimes, ce qui la rend inadaptée à un entraînement supervisé direct.

## Le flux

1. **Chargement** du fichier CSV (`webpage_phishing_detection_dataset.csv`) avec pandas.
2. **Sélection des caractéristiques** : exclusion des colonnes nécessitant une requête externe (WHOIS, trafic web, PageRank, indexation Google) — ces informations ne seront pas disponibles pour les URLs fraîches issues d'URLhaus au Jalon 3. 78 caractéristiques sont conservées sur les 87 d'origine.
3. **Séparation des données** : 80 % pour l'entraînement, 20 % pour le test (`train_test_split`, `random_state=42` pour la reproductibilité).
4. **Entraînement** d'un arbre de décision (`DecisionTreeClassifier`), volontairement limité en profondeur (`max_depth=5`) pour rester explicable et éviter le sur-apprentissage.
5. **Évaluation** sur les deux jeux (entraînement et test) séparément, via l'accuracy et la matrice de confusion.
6. **Analyse des caractéristiques importantes** pour comprendre ce que le modèle a appris.
7. **Test manuel** sur quelques URLs réelles issues du jeu de test, avec comparaison entre la vraie classe et la prédiction.

## Modèle choisi

Un **arbre de décision** a été préféré à une régression logistique pour sa lisibilité : il est possible de visualiser directement les règles de décision (image `arbre_decision_phishing.png`), ce qui facilite l'explication du fonctionnement du modèle. Le Random Forest utilisé dans le projet source du dataset n'a volontairement pas été repris, car il combine plusieurs dizaines d'arbres et sort du cadre "un seul modèle simple" fixé pour ce jalon.

## Résultats

| | Accuracy | Faux positifs / faux négatifs |
|---|---|---|
| Entraînement | 0.8734 | 483 / 675 |
| Test | 0.8683 | 131 / 170 |

L'accuracy est proche entre l'entraînement et le test (0.87 dans les deux cas), ce qui indique que le modèle **ne sur-apprend pas** : il généralise correctement à des données qu'il n'a jamais vues, plutôt que de simplement mémoriser le jeu d'entraînement.

## Caractéristiques les plus importantes

| Caractéristique | Importance |
|---|---|
| `nb_hyperlinks` | 0.499 |
| `nb_www` | 0.153 |
| `phish_hints` | 0.111 |
| `length_words_raw` | 0.103 |
| `ratio_extHyperlinks` | 0.028 |

`nb_hyperlinks` (nombre de liens hypertexte dans la page) domine largement les décisions du modèle : les pages de phishing ont souvent un nombre de liens atypique par rapport aux pages légitimes, soit parce qu'elles sont minimalistes (juste un formulaire de capture d'identifiants), soit parce qu'elles copient massivement des liens du vrai site imité.

## Test manuel sur des URLs réelles

Six URLs du jeu de test (trois légitimes, trois phishing) ont été vérifiées individuellement : cinq ont été correctement classées. La seule erreur (`assurance-amlfrance.com/id/amelipro/ifram2.html`, une URL de phishing classée à tort comme légitime) illustre une limite connue de l'approche : une attaque bien conçue, qui minimise les signaux structurels détectables (peu de liens, peu de mots-clés suspects), peut échapper à un modèle basé uniquement sur la structure de l'URL et le contenu de la page.

## Limite à clarifier avec l'encadrant

La caractéristique la plus influente du modèle, `nb_hyperlinks`, n'est pas dérivée de l'URL seule : elle nécessite d'avoir téléchargé et analysé le contenu HTML de la page. Cela signifie qu'au Jalon 3, le pipeline de détection ne pourra pas se limiter à analyser le texte brut d'une URL issue d'URLhaus — il faudra prévoir une étape de récupération du contenu de la page pour calculer cette caractéristique, ce qui ajoute une dépendance réseau supplémentaire non prévue dans la pile initialement "volontairement légère" du cadrage.