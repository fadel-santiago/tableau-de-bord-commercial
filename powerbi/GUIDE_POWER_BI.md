# Construire le rapport dans Power BI Desktop

> Le dépôt fournit les données prêtes à importer, les mesures DAX et la maquette. Un fichier natif `.pbix` doit être enregistré depuis Power BI Desktop ; il n'est pas simulé dans ce dépôt.

1. Installer **Power BI Desktop** (Windows). Cliquer **Obtenir les données → Texte/CSV**, sélectionner `data/processed/ventes_nettoyees.csv`, puis **Transformer les données**.
2. Vérifier les types : `order_date` = Date (ISO `YYYY-MM-DD`, locale adaptée si nécessaire), `year` et `quantity` = Nombre entier, `revenue_eur` = Nombre décimal. Renommer la table en **Ventes** et **Fermer et appliquer**.
3. Dans **Modélisation → Nouvelle mesure**, créer une mesure à la fois à partir de `mesures.dax`. Le fichier est un catalogue de mesures, pas un script DAX à coller intégralement.
4. Page **Vue d'ensemble** (16:9) : cartes « Chiffre d'affaires », « Commandes réalisées », « Panier moyen », « Clients actifs » ; courbe du CA par `month` ; barres du CA par `region` ; barres par `product` ; segments `year`, `segment`, `channel`, `category`.
5. Page **Analyse détaillée** : matrice `region × category`, barres du CA par canal, tableau de détails transactionnels ; mise en forme conditionnelle du CA.
6. Trier les mois texte `YYYY-MM` dans l'ordre croissant. Formater les montants en euros et les taux en pourcentage. Ajouter une info-bulle pour expliquer que le CA ne comprend que les commandes **Completed** et est **net des remises**.
7. Pour la comparaison YoY, filtrer à **une seule année** et afficher « Croissance CA annuelle % ». Sans année unique sélectionnée, la mesure affiche vide. Pour une version avancée de la comparaison temporelle, créer une table calendrier et employer les fonctions de time intelligence.
8. Sauvegarder votre rapport en `powerbi/Tableau_de_bord_commercial.pbix`, puis capturer une image dans `assets/` pour le README. Ne pas publier de données clients réelles.

## Maquette

```text
┌───────────────────────────────────────────────────────────────────────┐
│ TABLEAU DE BORD COMMERCIAL            Année · Segment · Canal         │
├─────────────────┬─────────────────┬─────────────────┬─────────────────┤
│ Chiffre affaires│ Commandes       │ Panier moyen    │ Clients actifs  │
├───────────────────────────────────┬───────────────────────────────────┤
│ Évolution mensuelle du CA         │ CA par région                     │
├───────────────────────────────────┼───────────────────────────────────┤
│ Top produits                      │ Répartition par canal            │
└───────────────────────────────────┴───────────────────────────────────┘
```
