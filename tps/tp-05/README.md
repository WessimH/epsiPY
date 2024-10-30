# TP 5

Le but du TP est de créer les routes suivantes:

GET / -> retourne un code 200 et un objet json vide -> Ce code est fourni
GET /calc/addition -> prend, via des [query parameter](https://fastapi.tiangolo.com/tutorial/query-params/#query-parameters), les paramètres a et b, qui doivent être des nombres 
POST /users -> prend l'objet suivant en paramètre

## Structure

```
├── api
│  ├── __init__.py
│  ├── business
│  │  └── __init__.py
│  └── model
│      └── __init__.py
```

Conseil: Pour les utilisateurs de produits Jetbrains, définissez le dossier tp-05 comme le dossier "
Source Root", comme indiqué ici:

![Source Root](res/img.png)