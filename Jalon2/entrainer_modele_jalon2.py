import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import matplotlib.pyplot as plt 

CSV_PATH = "webpage_phishing_detection_dataset.csv"

COLONNES_EXTERNES = [
    "domain_in_title",
    "domain_with_copyright",
    "whois_registered_domain",
    "domain_registration_length",
    "domain_age",
    "web_traffic",
    "dns_record",
    "google_index",
    "page_rank",
]

COLONNE_CIBLE = "status"
COLONNE_URL = "url"

def charger_donnees() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    print(f"Dataset charge : {df.shape[0]} lignes, {df.shape[1]}  Colonnes")
    return df

def preparer_donnees(df: pd.DataFrame):
    y = df[COLONNE_CIBLE].map({"legitimate":0,"phishing":1 })
    colonnes_a_exclure = COLONNES_EXTERNES + [COLONNE_CIBLE,COLONNE_URL]
    colonnes_features = [c for c in df.columns if c not in colonnes_a_exclure]

    X = df[colonnes_features]

    print(f"\nCaracteristiques conservees ({len(colonnes_features)}) :")
    print(colonnes_features)
    print(f"\nCaracteristiques exclues (necessitent une source externe) :")
    print(COLONNES_EXTERNES)

    return X, y

def entrainer_et_evaluer(X,y):
    X_train, X_test, y_train, y_test = train_test_split(
        X,y,test_size=0.2, random_state=42, shuffle = True, stratify=y
    )

    modele = DecisionTreeClassifier(max_depth=5, random_state=42)
    modele.fit(X_train, y_train)

    y_pred_train = modele.predict(X_train)
    print("\n=== Resultats sur les donnees d'ENTRAINEMENT ===")
    print(f"Accuracy : {accuracy_score(y_train, y_pred_train):.4f}")
    print("Matrice de confusion :")
    print(confusion_matrix(y_train, y_pred_train))

    y_pred_test = modele.predict(X_test)
    print("\n=== Resultats sur les donnees de TEST ===")
    print(f"Accuracy : {accuracy_score(y_test, y_pred_test):.4f}")
    print("Matrice de confusion :")
    print(confusion_matrix(y_test, y_pred_test))
    print("\nRapport de classification detaille :")
    print(classification_report(y_test, y_pred_test, target_names=["legitime", "phishing"]))

    return modele, X_train, X_test, y_train, y_test

def afficher_importance_features(modele, X):
    importances = pd.Series(modele.feature_importances_, index=X.columns)
    importances = importances.sort_values(ascending=False)
    print("\n=== Caracteristiques les plus importantes pour le modele ===")
    print(importances.head(10))


def sauvegarder_arbre(modele, X):
    plt.figure(figsize=(20, 10))
    plot_tree(
        modele,
        feature_names=X.columns,
        class_names=["legitime", "phishing"],
        filled=True,
        max_depth=3,
        fontsize=8,
    )

    plt.savefig("arbre_decision_phishing.png", dpi=150, bbox_inches="tight")
    print("\nImage de l'arbre sauvegardee dans : arbre_decision_phishing.png")

def tester_sur_quelques_urls(modele, df, X, y, X_test, n=3):
    print("\n=== Test manuel sur quelques URLs reelles (jeu de test) ===")
 
    # on recupere les URLs correspondant aux lignes de X_test
    urls_test = df.loc[X_test.index, COLONNE_URL]
    vraies_classes = y.loc[X_test.index]
 
    labels = {0: "legitime", 1: "phishing"}
    index_legitimes = vraies_classes[vraies_classes == 0].index[:n]
    index_phishing = vraies_classes[vraies_classes == 1].index[:n]
 
    for idx in list(index_legitimes) + list(index_phishing):
        url = urls_test.loc[idx]
        vraie_classe = labels[y.loc[idx]]
        prediction = labels[modele.predict(X.loc[[idx]])[0]]
        statut = "OK" if vraie_classe == prediction else "ERREUR"
        print(f"[{statut}] URL: {url}")
        print(f"        Vraie classe: {vraie_classe} | Predite: {prediction}\n")


if __name__ == "__main__":
    df = charger_donnees()
    X, y = preparer_donnees(df)
    modele, X_train, X_test, y_train, y_test = entrainer_et_evaluer(X, y)
    afficher_importance_features(modele, X)
    tester_sur_quelques_urls(modele, df, X, y, X_test, n=3)
    sauvegarder_arbre(modele, X)
