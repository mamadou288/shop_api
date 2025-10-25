# ProductImage - Images des produits

## Intro

Le modèle **ProductImage** permet d'associer **plusieurs images** à un produit.

**Pourquoi séparé ?**
- Un produit peut avoir 1, 5, 10+ images (illimité)
- Pas de colonnes vides (optimisation DB)
- Métadonnées par image (alt_text, order)

## Logique métier

### Ordre d'affichage
Le champ `order` contrôle l'ordre d'affichage des images :
- `order = 0` : Première image (thumbnail/principale)
- `order = 1` : Deuxième image
- `order = 2` : Troisième image, etc.

### Alt text pour accessibilité
Le champ `alt_text` :
- Décrit l'image pour les personnes aveugles (screen readers)
- Améliore le SEO (Google Images)
- Auto-généré si vide : `"{product.name} - Image"`

**Exemple** :
```html
<img src="macbook.jpg" alt="MacBook Pro 14 pouces - Vue de face">
```

### Relation avec Product
- Relation : **One-to-Many** (Un produit → Plusieurs images)
- ForeignKey : `product` → Product
- Related name : `product.images.all()`

## Gestion

### Via Admin Django (ProductImageInline)

Les images sont gérées directement dans l'admin du produit via un **inline**.

**Workflow** :
1. Se connecter à `/admin/`
2. Aller dans Products
3. Cliquer sur un produit
4. Ajouter des images via l'inline en bas
5. Définir `alt_text` et `order` pour chaque image

### Pas d'endpoints API directs

Pour le moment, ProductImage n'a **pas d'endpoints API dédiés**. Les images sont :
- Gérées via l'admin Django
- Récupérées automatiquement dans la réponse de `GET /api/products/{slug}/`

**Response example** :
```json
{
    "id": "uuid",
    "name": "MacBook Pro 14",
    "images": [
        {
            "id": "uuid",
            "image": "https://api.com/media/products/2024/10/macbook-front.jpg",
            "alt_text": "MacBook Pro 14 - Vue de face",
            "order": 0
        },
        {
            "id": "uuid",
            "image": "https://api.com/media/products/2024/10/macbook-side.jpg",
            "alt_text": "MacBook Pro 14 - Vue de côté",
            "order": 1
        }
    ]
}
```

## À venir (Phase 2)

- Endpoint pour upload d'image via API
- Gestion des images depuis le frontend
- AWS S3 pour le stockage des images

