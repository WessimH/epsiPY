# TP 5

## Objectif

Le but du TP est de créer les routes suivantes:

GET / → retourne un code 200 et un objet json vide -> Ce code est fourni
GET /calc/addition → prend, via des [query parameter](https://fastapi.tiangolo.com/tutorial/query-params/#query-parameters), les paramètres a et b, qui doivent être des nombres 
POST /users → Permet de créer un user, prend l'objet suivant en paramètre [(via le body)](https://fastapi.tiangolo.com/tutorial/body/)
```json
{"username": "", "password":  ""}
```
Vous pouvez utiliser la base de donnée que vous souhaitez (sqlite, postgres, fichiers json), mais vous devez fournir un script permettant l'initialisation de la bdd, si nécessaire.
Néanmoins, il n'est pas nécessaire que l'application soit persistente, donc vous pouvez tout garder en mémoire si vous le souhaitez.

POST /token 
et
GET /users/me 

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
Source Root", comme indiqué ici :

![Source Root](res/img.png)

Pour les autres, la solution de facilité reste encore d'exporter PYTHONPATH dans votre terminal, de sorte que le dossier TP-P5 soit le source root.

→ vous pourrez ainsi importer tous les sous modules d'api via `from api.business.user import User`

## Test

```shell
pip install pytest httpx
```