# Category - Gestion des catégories

## Intro

L'app **Category** permet de gérer les catégories de produits avec support de hiérarchie (catégories parentes/enfantes).

**Exemples** :
- Electronics > Laptops > Gaming Laptops
- Clothing > Men > Shirts

## Logique métier

### Hiérarchie parent/enfant
- Une catégorie peut avoir une **catégorie parente** (field `parent`)
- Une catégorie peut avoir plusieurs **enfants** (relation inverse `children`)
- Les catégories racines ont `parent = NULL`

### `get_full_path()`
Retourne le chemin complet de la catégorie :
```python
category.get_full_path()  # "Electronics > Laptops > Gaming Laptops"
```

### Slug auto-généré
Le slug est automatiquement généré depuis le nom lors de la création.

## Endpoints

### Liste et création
**`GET /api/categories/`** - Liste toutes les catégories actives
- Permission : AllowAny (tout le monde peut voir)

**`POST /api/categories/`** - Créer une catégorie
- Permission : IsAdminUser (admin uniquement)
- Body :
```json
{
    "name": "Electronics",
    "description": "Electronic devices and gadgets",
    "parent": null
}
```

### Détail, modification, suppression
**`GET /api/categories/{slug}/`** - Détail d'une catégorie
- Permission : AllowAny

**`PATCH /api/categories/{slug}/`** - Modifier une catégorie
- Permission : IsAdminUser
- Body :
```json
{
    "description": "Updated description"
}
```

**`DELETE /api/categories/{slug}/`** - Supprimer une catégorie
- Permission : IsAdminUser
- Note : Soft delete (is_active = False)

