# 📊 Shop E-commerce Analytics Dashboard

Dashboard interactif Streamlit pour visualiser les KPIs e-commerce de l'API Django Analytics.

## 🎯 Features

### 4 Pages d'analyse

1. **📊 Overview** - Vue d'ensemble des KPIs principaux
   - Revenue total, Orders, AOV, CLV
   - Graphique évolution revenue
   - Top 5 produits
   - Commandes par statut

2. **💰 Business** - Analyse revenue & croissance
   - Revenue avec MoM Growth
   - CLV et Repeat Purchase Rate
   - Charts revenue trends
   - Insights automatiques

3. **📦 Products** - Inventory & top produits
   - Valeur inventory totale
   - Top 10 produits (revenue & quantité)
   - Alertes stock faible
   - Performance par catégorie

4. **👥 Users** - Clients & rétention
   - Utilisateurs actifs vs total
   - Croissance mensuelle
   - Segmentation (new, one-time, repeat, loyal)
   - Top 10 customers

### Design Features

- ✅ Charts interactifs (Plotly)
- ✅ Filtres de dates (7d, 30d, 90d, 1y)
- ✅ Refresh button pour actualiser les données
- ✅ Metrics cards avec growth indicators
- ✅ Tables triables
- ✅ Cache 15min (performance)
- ✅ Responsive layout

## 🚀 Installation

### Prérequis

- Python 3.11+
- API Django lancée sur `http://localhost:8000`
- Compte admin (`admin@shop.com` / `TestPass123!`)

### Étape 1 : Installer les dépendances

```bash
cd dashboard
pip install -r requirements.txt
```

### Étape 2 : Vérifier l'API

Assurez-vous que l'API Django est lancée :

```bash
# Dans un autre terminal, à la racine du projet
docker-compose up
```

L'API doit être accessible sur `http://localhost:8000`.

### Étape 3 : Lancer le dashboard

```bash
streamlit run app.py
```

Le dashboard s'ouvre automatiquement dans votre navigateur sur `http://localhost:8501`.

## 📖 Utilisation

### Navigation

Utilisez le **menu latéral** pour naviguer entre les pages :
- Overview
- Business
- Products
- Users

### Filtres

- **Période** : Sélectionnez 7d, 30d, 90d ou 1y
- **Dates personnalisées** : Disponible dans la page Business (dans l'expander)

### Actualisation

Cliquez sur le bouton **🔄 Actualiser** dans la sidebar pour forcer le rechargement des données (vide le cache).

## 🔧 Configuration

### Changer l'URL de l'API

Si votre API est sur un autre port/domaine, modifiez dans `utils/api_client.py` :

```python
API_BASE_URL = "http://localhost:8000"  # Modifiez ici
```

### Changer le timeout

```python
API_TIMEOUT = 30  # Secondes
```

### Changer les credentials admin

Dans `utils/api_client.py`, fonction `get_admin_token()` :

```python
def get_admin_token(email="admin@shop.com", password="TestPass123!"):
```

## 📊 Technologies

- **Streamlit 1.29** - Framework dashboard
- **Plotly 5.18** - Charts interactifs
- **Pandas 2.1** - Data manipulation
- **Requests 2.31** - API calls

## 📁 Structure

```
dashboard/
├── app.py                      # Page d'accueil
├── pages/
│   ├── overview.py             # Vue d'ensemble
│   ├── business.py             # KPIs business
│   ├── products.py             # KPIs produits
│   └── users.py                # KPIs utilisateurs
├── utils/
│   ├── api_client.py           # Connexion API Django
│   ├── charts.py               # Fonctions charts Plotly
│   ├── metrics.py              # Formatage métriques
│   └── styles.py               # CSS custom
├── .streamlit/
│   └── config.toml             # Configuration Streamlit
├── requirements.txt
└── README.md
```

## 🐛 Troubleshooting

### "❌ Erreur de connexion à l'API"

**Cause** : L'API Django n'est pas lancée ou n'est pas accessible.

**Solution** :
```bash
# Vérifier que Docker tourne
docker-compose ps

# Relancer si nécessaire
docker-compose up
```

### "❌ Authentication expired"

**Cause** : Le token JWT a expiré (15 min par défaut).

**Solution** : Cliquez sur **🔄 Actualiser** ou rafraîchissez la page (F5).

### "Impossible de récupérer les données"

**Cause** : L'API retourne une erreur 500 ou timeout.

**Solution** : 
- Vérifiez les logs Django : `docker-compose logs web`
- Vérifiez que la DB contient des données : `docker-compose exec web python manage.py shell`

### Charts ne s'affichent pas

**Cause** : Données manquantes ou format incorrect.

**Solution** : Vérifiez que l'API retourne bien des données en testant directement :
```bash
curl http://localhost:8000/api/analytics/dashboard/ -H "Authorization: Bearer YOUR_TOKEN"
```

## 🚀 Déploiement (Optionnel)

### Streamlit Cloud (Gratuit)

1. Push le dossier `dashboard/` sur GitHub
2. Aller sur [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connecter le repo
4. Configurer l'`API_BASE_URL` vers votre API en production

**Note** : Votre API Django doit être accessible publiquement (Heroku, AWS, etc.)

## 📝 Notes

- **Cache** : Les données sont mises en cache 15 minutes (@st.cache_data)
- **Performance** : Le dashboard est optimisé pour des datasets de 1000+ commandes
- **Sécurité** : Le token JWT est stocké en mémoire (pas de persistence)

## 🎓 Pour aller plus loin

### Ajouter une nouvelle page

1. Créer `pages/ma_page.py`
2. Importer les utils nécessaires
3. Fetcher les données avec `api_client`
4. Créer les charts avec `charts.py`
5. La page apparaît automatiquement dans la sidebar !

### Personnaliser le th
ème

Modifier `.streamlit/config.toml` :

```toml
[theme]
primaryColor = "#1f77b4"       # Couleur principale
backgroundColor = "#ffffff"     # Fond
secondaryBackgroundColor = "#f0f2f6"  # Fond secondaire
```

---

**Dashboard créé pour le projet E-commerce API** 🚀

