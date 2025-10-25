# Product - Gestion des produits

## Intro

L'app **Product** gère le catalogue de produits disponibles à l'achat.

Chaque produit a :
- Nom, description, prix, stock
- Catégorie (FK → Category)
- SKU optionnel (identifiant unique)
- Plusieurs images possibles (via ProductImage)

## Logique métier

### Gestion du stock

**`is_in_stock`** (property)
- Retourne `True` si `stock > 0` ET `is_active = True`

**`reduce_stock(quantity)`**
- Réduit le stock (utilisé lors de la création de commandes)
- Lève une erreur si quantité > stock disponible

**`increase_stock(quantity)`**
- Augmente le stock (utilisé lors de remboursements)

### Slug auto-généré
Le slug est automatiquement généré depuis le nom lors de la création.

## Endpoints

### Liste et création

**`GET /api/products/`** - Liste des produits avec filtres
- Permission : AllowAny

**Filtres disponibles** :
- `?category=<uuid>` - Filtrer par catégorie
- `?min_price=100` - Prix minimum
- `?max_price=500` - Prix maximum
- `?in_stock=true` - Produits en stock uniquement
- `?search=macbook` - Recherche dans nom, description, SKU
- `?ordering=price` - Tri par prix croissant
- `?ordering=-price` - Tri par prix décroissant
- `?ordering=name` - Tri alphabétique
- `?ordering=-created_at` - Plus récents d'abord (défaut)

**Exemple** :
```
GET /api/products/?category=uuid&min_price=1000&max_price=2000&in_stock=true&ordering=price
```

**`POST /api/products/`** - Créer un produit
- Permission : IsAdminUser
- Body :
```json
{
    "name": "MacBook Pro 14",
    "description": "Apple MacBook Pro with M3 chip",
    "price": "1999.99",
    "stock": 15,
    "category": "<category_uuid>",
    "sku": "MBP-M3-14"
}
```

### Détail, modification, suppression

**`GET /api/products/{slug}/`** - Détail d'un produit
- Permission : AllowAny
- Retourne : Product complet avec nested category et images

**`PATCH /api/products/{slug}/`** - Modifier un produit
- Permission : IsAdminUser
- Body :
```json
{
    "price": "1899.99",
    "stock": 20
}
```

**`DELETE /api/products/{slug}/`** - Supprimer un produit
- Permission : IsAdminUser
- Note : Soft delete (is_active = False)

## Exemples de requêtes

### Rechercher "macbook"
```
GET /api/products/?search=macbook
```

### Produits en stock entre 1000€ et 2000€
```
GET /api/products/?in_stock=true&min_price=1000&max_price=2000&ordering=price
```

### Produits d'une catégorie spécifique
```
GET /api/products/?category=<uuid_category>
```

