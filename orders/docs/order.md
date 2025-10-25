# Order - Gestion des commandes

## Introduction

Le modèle `Order` représente une commande passée par un utilisateur. Il contient les informations de livraison, le statut de la commande, le montant total, et les dates importantes du cycle de vie de la commande.

## Logique métier

### Statuts de commande

- **PENDING** : En attente (état initial)
- **CONFIRMED** : Confirmée par l'administrateur
- **SHIPPED** : Expédiée
- **DELIVERED** : Livrée
- **CANCELLED** : Annulée

### Gestion du stock

- Lors de la création d'une commande, le stock des produits est automatiquement réduit
- Lors de l'annulation d'une commande, le stock est restauré
- Une commande ne peut être annulée que si elle est en statut `PENDING` ou `CONFIRMED`

### Snapshots

Les informations des produits (nom, prix) sont sauvegardées au moment de la commande pour conserver l'historique même si le produit est modifié ultérieurement.

## Endpoints

### Liste et création

**GET** `/api/orders/`
- Liste des commandes
- Utilisateur : voit ses commandes
- Admin : voit toutes les commandes
- Filtres : `status`
- Tri : `created_at`, `total_amount`

**POST** `/api/orders/`
- Créer une commande avec articles
- Authentification requise
- Validation du stock automatique
- Réduction du stock automatique

### Détail

**GET** `/api/orders/{uuid}/`
- Détails d'une commande
- Utilisateur : voit sa commande uniquement
- Admin : voit toutes les commandes

### Actions

**POST** `/api/orders/{uuid}/cancel/`
- Annuler une commande
- Utilisateur : peut annuler ses commandes
- Admin : peut annuler toutes les commandes
- Restaure le stock

**POST** `/api/orders/{uuid}/confirm/`
- Confirmer une commande
- Admin uniquement
- Transition : PENDING → CONFIRMED

**POST** `/api/orders/{uuid}/ship/`
- Expédier une commande
- Admin uniquement
- Transition : CONFIRMED → SHIPPED

**POST** `/api/orders/{uuid}/deliver/`
- Livrer une commande
- Admin uniquement
- Transition : SHIPPED → DELIVERED

