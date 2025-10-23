# User Model

Modèle utilisateur personnalisé avec email comme identifiant.

## Champs

### Identification
- `id` : UUID
- `email` : Unique, utilisé pour login
- `username` : Requis
- `password` : Hashé (PBKDF2)

### Informations personnelles
- `first_name`, `last_name`
- `phone` : Numéro de téléphone
- `date_of_birth` : Date de naissance (optionnel)

### Permissions
- `is_admin` : Permissions métier (gestion produits)
- `is_staff` : Accès admin Django
- `is_active` : Compte actif

### RGPD
- `newsletter_consent` : Consentement newsletter
- `marketing_consent` : Consentement marketing

### Internationalisation
- `language` : Langue préférée (fr/en)
- `currency` : Devise préférée (EUR/USD)

### Timestamps
- `created_at` : Date de création
- `updated_at` : Dernière modification

## Usage

```python
# Créer un utilisateur
user = User.objects.create_user(
    email='user@example.com',
    username='username',
    password='password',
    first_name='John',
    last_name='Doe'
)

# Login field
USERNAME_FIELD = 'email'
```

