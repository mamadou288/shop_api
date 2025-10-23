# Shop E-commerce API

> API REST professionnelle pour plateforme e-commerce avec Django, PostgreSQL, authentification JWT et intégration de paiements.

**En cours de développement** - Développement actif

---

## Vue d'ensemble du projet

Construction d'une API backend e-commerce complète avec :
- Catalogue de produits avec catégories et variantes
- Gestion du panier d'achat
- Système de traitement des commandes
- Authentification JWT sécurisée
- Intégration de paiement Stripe
- Permissions admin et client
- Gestion d'images avec AWS S3

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
│   ├── services/        # Logique métier
│   └── docs/            # Documentation technique
├── core/                 # App utilitaires réutilisables
│   ├── models/          # Models abstraits (AuditedModel)
│   └── utils/           # Utilitaires (UUID, permissions)
├── requirements.txt      # Dépendances Python
├── docker-compose.yml    # Configuration Docker
└── README.md

Note: Les apps products, cart, orders seront créées au fur et à mesure du développement
```

---

## Endpoints API

### Authentification
- `POST /api/auth/register/` - Inscription utilisateur
- `POST /api/auth/login/` - Connexion (obtenir tokens JWT)
- `POST /api/auth/token/refresh/` - Rafraîchir access token
- `GET /api/auth/profile/` - Récupérer profil utilisateur
- `PATCH /api/auth/profile/` - Mettre à jour profil

---

---

## Documentation technique

Chaque app contient sa propre documentation dans le dossier `docs/` :

- `accounts/docs/` - Documentation authentification et utilisateurs

---

---

## Auteur

**Mamadou Diakhate**
- GitHub : [@mamadou288](https://github.com/mamadou288)
- LinkedIn : [Mamadou Diakhate](https://linkedin.com/in/mamadou-diakhate-7406561b4)
- Email : mamadou.data.dev@gmail.com

---


