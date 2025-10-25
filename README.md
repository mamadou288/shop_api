# Shop E-commerce API

> API REST professionnelle pour plateforme e-commerce avec Django, PostgreSQL, authentification JWT et intégration de paiements.

**En cours de développement** - Développement actif

---

## Vue d'ensemble du projet

Construction d'une API backend e-commerce complète avec :
- ✅ Catalogue de produits avec catégories hiérarchiques
- ✅ Gestion des images produits
- ✅ Système de traitement des commandes
- ✅ Authentification JWT sécurisée
- ✅ Permissions admin et client
- ✅ Business Intelligence & KPIs (Analytics)
- ✅ Management command pour générer données de test
- 🚧 Gestion du panier d'achat (à venir)
- 🚧 Intégration de paiement Stripe (à venir)
- 🚧 Gestion d'images avec AWS S3 (à venir)

---

## Stack technique

- **Backend** : Django 4.2, Django REST Framework
- **Base de données** : PostgreSQL 15
- **Authentification** : JWT (djangorestframework-simplejwt)
- **Conteneurisation** : Docker, Docker Compose

---

## Installation rapide

### Prérequis
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (via Docker)

### Installation

#### Avec Docker

```bash
# Cloner le repository
git clone https://github.com/mamadou288/shop-ecommerce-api.git
cd shop-ecommerce-api

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# Lancer tous les services (PostgreSQL + Django)
docker-compose up -d --build

# Appliquer les migrations
docker-compose exec web python manage.py migrate

# Créer un superuser
docker-compose exec web python manage.py createsuperuser

# Générer des données de test (optionnel)
docker-compose exec web python manage.py generate_sample_data --users 300 --products 200 --orders 1000

# L'API est accessible sur http://localhost:8000
```

---

## Structure du projet

```
E-commerce/
├── app/                  # Projet Django principal (settings, urls)
├── accounts/             # App authentification utilisateurs
│   ├── models/          # Modèles User
│   ├── serializers/     # Serializers DRF
│   ├── views/           # Views API
│   └── docs/            # Documentation technique
├── core/                # App utilitaires réutilisables
│   ├── models/          # Models abstraits (AuditedModel)
│   └── utils/           # Utilitaires (UUID, permissions)
├── products/             # App catalogue produits
│   ├── models/          # Category, Product, ProductImage
│   ├── serializers/     # Serializers DRF
│   ├── views/           # Views API (Generic views)
│   ├── admin.py         # Admin Django
│   └── docs/            # Documentation technique
├── orders/               # App gestion commandes
│   ├── models/          # Order, OrderItem, OrderStatus
│   ├── serializers/     # Serializers DRF
│   ├── views/           # Views API (CRUD + Actions)
│   ├── admin.py         # Admin avec badges colorés
│   └── docs/            # Documentation technique
├── analytics/            # App business intelligence & KPIs
│   ├── services/        # Business, Product, User KPIs
│   ├── views/           # API endpoints avec cache
│   ├── urls.py          # Routes API
│   └── docs/            # Documentation KPIs
├── requirements.txt      # Dépendances Python
├── docker-compose.yml    # Configuration Docker
└── README.md
```

---

## Endpoints API

### Authentification
- `POST /api/auth/register/` - Inscription utilisateur
- `POST /api/auth/login/` - Connexion (obtenir tokens JWT)
- `POST /api/auth/token/refresh/` - Rafraîchir access token
- `GET /api/auth/profile/` - Récupérer profil utilisateur
- `PATCH /api/auth/profile/` - Mettre à jour profil

### Produits
- `GET /api/categories/` - Liste des catégories
- `POST /api/categories/` - Créer une catégorie (admin)
- `GET /api/categories/{slug}/` - Détail d'une catégorie
- `GET /api/products/` - Liste des produits (filtres, recherche, tri)
- `POST /api/products/` - Créer un produit (admin)
- `GET /api/products/{slug}/` - Détail d'un produit

### Commandes
- `GET /api/orders/` - Liste des commandes (utilisateur : ses commandes, admin : toutes)
- `POST /api/orders/` - Créer une commande
- `GET /api/orders/{uuid}/` - Détail d'une commande
- `POST /api/orders/{uuid}/cancel/` - Annuler (owner/admin)
- `POST /api/orders/{uuid}/confirm/` - Confirmer (admin)
- `POST /api/orders/{uuid}/ship/` - Expédier (admin)
- `POST /api/orders/{uuid}/deliver/` - Livrer (admin)

### Analytics (Admin uniquement)
- `GET /api/analytics/dashboard/` - Tous les KPIs (business, products, users)
- `GET /api/analytics/business/` - KPIs business (revenue, AOV, growth, CLV)
- `GET /api/analytics/products/` - KPIs produits (top products, stock alerts)
- `GET /api/analytics/users/` - KPIs utilisateurs (active, retention, segments)

---

---

## Documentation technique

Chaque app contient sa propre documentation dans le dossier `docs/` :

- `accounts/docs/` - Documentation authentification et utilisateurs
- `products/docs/` - Documentation catalogue produits
- `orders/docs/` - Documentation gestion commandes
- `analytics/docs/` - Documentation KPIs et business intelligence

**Tests API :**
- Voir `orders/TESTING.md` pour les exemples de requêtes
- Voir `analytics/TESTING.md` pour tester les KPIs

---

---

## Auteur

**Mamadou Diakhate**
- GitHub : [@mamadou288](https://github.com/mamadou288)
- LinkedIn : [Mamadou Diakhate](https://linkedin.com/in/mamadou-diakhate-7406561b4)
- Email : mamadou.data.dev@gmail.com

---


