# Authentication

Système d'authentification JWT avec inscription et gestion de profil.

## Endpoints

### Register
`POST /api/auth/register/`

```json
{
    "email": "user@example.com",
    "username": "username",
    "password": "StrongPass123!",
    "password2": "StrongPass123!",
    "first_name": "John",
    "last_name": "Doe"
}
```

Response (201 Created):
```json
{
    "id": "uuid-string",
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    ...
}
```

### Login
`POST /api/auth/login/`

```json
{
    "email": "user@example.com",
    "password": "StrongPass123!"
}
```

Response:
```json
{
    "refresh": "eyJ...",
    "access": "eyJ..."
}
```

### Refresh Token
`POST /api/auth/token/refresh/`

```json
{
    "refresh": "eyJ..."
}
```

### Profile
`GET /api/auth/profile/`  
Header: `Authorization: Bearer {access_token}`

`PATCH /api/auth/profile/`  
Header: `Authorization: Bearer {access_token}`

```json
{
    "first_name": "Updated",
    "phone": "+33612345678"
}
```

