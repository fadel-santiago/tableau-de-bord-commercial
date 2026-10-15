# 📊 Tableau de bord commercial | Power BI & Analyse de données

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Power%20BI](https://img.shields.io/badge/Power%20BI-DAX-F2C811) ![SQL](https://img.shields.io/badge/SQL-SQLite-4479A1) ![Data](https://img.shields.io/badge/Données-100%25%20fictives-green)

> **Objectif :** transformer des données brutes de ventes en indicateurs fiables et lisibles pour aider à orienter les décisions commerciales.

**[English summary](#english-summary)** · [Exécution](#démarrage-rapide) · [Power BI](powerbi/GUIDE_POWER_BI.md) · [Requêtes SQL](sql/analyses.sql)

## Contexte métier

Une société fictive vend des logiciels, prestations de conseil et formations dans six régions françaises. Sa direction souhaite suivre la performance du chiffre d'affaires, des produits, des canaux d'acquisition et des segments clients.

## Résultats de démonstration

| Indicateur                | Valeur (2024–2025) |
| ------------------------- | ------------------:|
| Commandes reçues          | 2 400              |
| Commandes réalisées       | 2 171              |
| Clients acheteurs uniques | 478                |
| Chiffre d'affaires net    | **1 307 512,70 €** |
| Chiffre d'affaires 2024   | 657 525,09 €       |
| Chiffre d'affaires 2025   | 649 987,61 €       |

**Attention :** les données sont **entièrement synthétiques**. Les résultats n'illustrent pas une entreprise réelle, ne doivent pas être considérés comme des constats de marché et ne reposent pas sur des données confidentielles.

### Indicateurs et définitions

- **CA net** : somme des lignes `Completed`, calculée comme `quantité × prix unitaire × (1 − remise/100)` ; les commandes annulées ou remboursées contribuent **0 €** au CA.
- **Commandes réalisées** : nombre distinct de commandes `Completed`.
- **Panier moyen** : CA net / commandes réalisées.
- **Clients actifs** : clients distincts ayant au moins une commande `Completed`.
- **Évolution annuelle** : différence relative du CA entre 2025 et 2024.

**Hypothèse simplificatrice :** le dataset ne contient ni TVA, ni coûts, ni frais de livraison, ni dates de remboursement. Le CA net est donc une mesure opérationnelle fictive, **pas** un résultat comptable officiel et **pas** une marge.

## Fonctionnalités

- Génération déterministe de 2 400 commandes de démonstration (2024–2025).
- Validation des colonnes, doublons, dates, valeurs manquantes et seuils numériques.
- Calcul des remises et revenus ; export CSV propre et base SQLite indexée.
- Requêtes SQL pour le CA mensuel, régional, par produit et canal, ainsi que croissance annuelle.
- Dashboard interactif Streamlit avec filtres combinés (année, segment, canal, région, catégorie), 4 KPI, graphiques et export CSV.
- Catalogue de mesures DAX et instructions pas-à-pas pour reconstruire le rapport dans Power BI Desktop.
- Test automatisé du pipeline et workflow GitHub Actions.

## Architecture

```text
.
├── app.py                           # Application interactive Streamlit
├── data/
│   ├── raw/ventes_brutes.csv        # Données synthétiques générées
│   └── processed/
│       ├── ventes_nettoyees.csv     # Import direct Power BI
│       └── commercial.sqlite        # Base pour requêtes SQL
├── scripts/
│   ├── generate_data.py             # Reproduire les données fictives
│   └── prepare_data.py              # Nettoyage, calcul CA, chargement SQL
├── sql/analyses.sql                 # Analyses commerciales
├── powerbi/
│   ├── GUIDE_POWER_BI.md            # Mode d'emploi et maquette
│   └── mesures.dax                  # Catalogue de mesures DAX
├── tests/test_pipeline.py
├── .github/workflows/test.yml
└── requirements.txt
```

## Démarrage rapide

Pré-requis : Python 3.11+ (fonctionne aussi avec des versions modernes compatibles).

```bash
# Créer l'environnement Python
python -m venv .venv
# Windows PowerShell : .venv\Scripts\Activate.ps1
# macOS / Linux : source .venv/bin/activate
pip install -r requirements.txt

# Regénérer les données (les CSV et la base fournis sont déjà utilisables)
python scripts/generate_data.py
python scripts/prepare_data.py

# Ouvrir le tableau de bord dans le navigateur
streamlit run app.py

# Tests automatiques
python -m unittest discover -s tests -v
```

Le dashboard interactif fonctionne **sans Power BI**. Pour le rapport Power BI natif, suivre [le guide](powerbi/GUIDE_POWER_BI.md), importer `data/processed/ventes_nettoyees.csv` et enregistrer son propre fichier `.pbix` depuis Power BI Desktop.

## Pistes d'analyse et recommandations métier

Ce projet illustre les questions qu'un analyste poserait à la direction :

1. Dans quelles régions et catégories le CA est-il le plus élevé ?
2. Le CA évolue-t-il positivement d'une année sur l'autre ?
3. Quels canaux de vente contribuent le plus au CA ?
4. Quels produits ont un poids commercial important ?
5. Quelles baisses méritent une recherche des causes (prix, volumes, mix produit, saisonnalité) ?

Les observations ne prouvent pas la causalité ; elles servent à **prioriser les analyses complémentaires**.

## Étapes techniques

`CSV brut` → `Validation / nettoyage Python` → `CSV analytique + SQLite` → `SQL / KPI` → `Power BI ou Streamlit` → `Décisions commerciales`

## English summary

**Commercial sales analytics portfolio project:** deterministic synthetic order data, Python cleaning and quality checks, SQLite SQL queries, interactive Streamlit KPI dashboard, and Power BI Desktop build guide with DAX measures. Built for decision support; all sales data is fabricated for demonstration purposes.

## Licence

MIT, voir [LICENSE](LICENSE).
