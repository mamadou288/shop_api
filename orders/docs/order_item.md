# OrderItem - Articles d'une commande

## Introduction

Le modèle `OrderItem` représente un article individuel dans une commande. Il stocke une référence au produit ainsi qu'un snapshot des informations du produit au moment de la commande (nom, prix).

## Logique métier

### Snapshots

Pour préserver l'historique et l'intégrité des factures, `OrderItem` sauvegarde :
- `product_name` : Le nom du produit au moment de la commande
- `product_price` : Le prix du produit au moment de la commande
- `quantity` : La quantité commandée
- `subtotal` : Calculé automatiquement (price × quantity)

Cela garantit que même si le produit est modifié ou supprimé, la commande conserve les bonnes informations.

### Création

Les `OrderItems` sont créés automatiquement lors de la création d'une commande. Ils ne peuvent pas être créés ou modifiés séparément.

### Calcul du sous-total

Le sous-total est calculé automatiquement lors de la sauvegarde :
```
subtotal = product_price × quantity
```

## Gestion

Les `OrderItems` sont gérés uniquement via :

1. **Création de commande** : Nested dans `POST /api/orders/`
2. **Affichage** : Nested dans `GET /api/orders/{uuid}/`
3. **Admin Django** : Inline dans l'interface OrderAdmin

Il n'existe pas d'endpoints directs pour gérer les `OrderItems` car ils font partie intégrante de la commande (immutabilité).

