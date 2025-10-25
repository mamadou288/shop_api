# App Analytics - Business Intelligence & KPIs

## Vue d'ensemble

L'application `analytics` fournit des API endpoints pour accéder aux **KPIs (Key Performance Indicators)** du business e-commerce. Tous les endpoints sont **protégés par authentification admin** et **cachés pendant 15 minutes** pour des performances optimales.

## Features

### ✅ Business KPIs
- Total revenue (orders DELIVERED)
- Total orders (par statut)
- Average Order Value (AOV)
- **MoM Growth Rate** (Month-over-Month revenue & orders)
- **Customer Lifetime Value (CLV)**
- **Repeat Purchase Rate**
- Revenue by month (line chart data)
- Orders by status (pie chart data)

### ✅ Product KPIs
- Top 10 products (by revenue)
- Top 10 products (by quantity sold)
- Low stock alerts (stock < 10)
- Out of stock products count
- Top categories (by revenue)
- Category distribution
- Inventory value

### ✅ User KPIs
- Total users
- New users (in period)
- Active users (with orders in period)
- Top 10 customers (by total spent)
- Retention rate
- Users by registration month
- User segmentation (new, one-time, repeat, loyal)

## Endpoints

| Méthode | URL | Description | Cache |
|---------|-----|-------------|-------|
| GET | `/api/analytics/dashboard/` | All KPIs combinés | 15 min |
| GET | `/api/analytics/business/` | Business KPIs only | 15 min |
| GET | `/api/analytics/products/` | Product KPIs only | 15 min |
| GET | `/api/analytics/users/` | User KPIs only | 15 min |

## Query Parameters

### Filtres de date

```
?start_date=2024-01-01    # Date de début (format: YYYY-MM-DD)
?end_date=2024-12-31      # Date de fin (format: YYYY-MM-DD)
```

### Shortcuts de période

```
?period=7d    # 7 derniers jours
?period=30d   # 30 derniers jours (défaut)
?period=90d   # 90 derniers jours
?period=1y    # 1 an
```

## Exemples d'utilisation

### Dashboard complet

```bash
GET /api/analytics/dashboard/
Authorization: Bearer {admin_token}
```

Retourne tous les KPIs (business, products, users).

### Business KPIs sur 30 jours

```bash
GET /api/analytics/business/?period=30d
Authorization: Bearer {admin_token}
```

### KPIs produits

```bash
GET /api/analytics/products/
Authorization: Bearer {admin_token}
```

### KPIs utilisateurs avec dates custom

```bash
GET /api/analytics/users/?start_date=2024-01-01&end_date=2024-06-30
Authorization: Bearer {admin_token}
```

## Cache

### Stratégie
- **Durée** : 15 minutes (900 secondes)
- **Backend** : LocMemCache (RAM)
- **Clés** : `analytics:{type}:{start}:{end}`

### Pourquoi le cache ?
- KPIs = requêtes complexes (SUM, COUNT, JOIN)
- Calculs lourds sur 1000+ orders
- Dashboard accédé fréquemment
- **Résultat** : 1.8s → 0.001s après cache ⚡

### Invalidation
Le cache expire automatiquement après 15 minutes. Pour forcer un recalcul, redémarrer Django :
```bash
docker-compose restart web
```

## Permissions

**Admin uniquement** (`IsAdminUser`)
- Staff users ✅
- Superusers ✅
- Regular users ❌

## Architecture

```
analytics/
├── services/
│   ├── business_kpis.py    # Calculs business (revenue, AOV, growth, CLV)
│   ├── product_kpis.py     # Calculs produits (top products, stock)
│   └── user_kpis.py        # Calculs users (active, retention)
├── views/
│   └── kpis.py             # API views avec cache
├── urls.py                 # Routes API
└── README.md
```

## Performance

### Sans cache
- Dashboard : ~1.8s (10+ requêtes DB)
- Business KPIs : ~800ms
- Product KPIs : ~500ms
- User KPIs : ~600ms

### Avec cache (après 1ère visite)
- Tous endpoints : **~1ms** ⚡
- Charge DB : **réduite de 98%**

## Data Source

Les KPIs sont calculés en temps réel depuis :
- **Orders** : Revenue, AOV, growth
- **OrderItems** : Top products, sales
- **Products** : Stock, inventory
- **Users** : Active, retention, segments

**Période par défaut** : 90 derniers jours

## Tests

Voir `analytics/docs/api.md` pour des exemples de requêtes Postman.

## Management Command

Générer des données de test :
```bash
python manage.py generate_sample_data --users 300 --products 200 --orders 1000 --months 3
```

Cela crée suffisamment de données pour des KPIs significatifs !

## À venir

### Phase 2 (optionnel)
- Dashboard admin HTML custom avec Chart.js
- Route : `/admin/analytics/dashboard/`
- Graphiques interactifs (line charts, pie charts)
- Export CSV/PDF

### KPIs avancés supplémentaires
- RFM Segmentation (Recency, Frequency, Monetary)
- Cohort Analysis
- Customer Churn Rate
- Product Performance Score
- Inventory Turnover Rate

---

**Documentation complète** : Voir `analytics/docs/` pour plus de détails.

