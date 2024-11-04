# main.py

from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional, List, Dict
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Clé secrète pour JWT (à garder secrète en production)
SECRET_KEY = "votre_clé_secrète"  # Remplacez par une clé aléatoire et sécurisée
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Contexte de hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Schéma OAuth2 pour l'authentification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# "Base de données" en mémoire
users_db = {}
todo_id_counter = 1

# Modèles Pydantic

class AdditionParams(BaseModel):
    a: float
    b: float

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TodoCreate(BaseModel):
    name: str
    description: Optional[str] = None
    priority: int

class TodoUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None

class TodoItem(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    priority: int

# Fonctions utilitaires pour les mots de passe

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Fonction d'authentification de l'utilisateur

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

# Fonction pour créer un jeton d'accès JWT

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dépendance pour obtenir l'utilisateur actuel

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'authentification",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

# Routes

# Route principale
@app.get("/")
async def root():
    return {}

# Route d'addition
@app.get("/miscellaneous/addition")
async def addition(a: float = Query(...), b: float = Query(...)):
    return {"result": a + b}

# Création d'un utilisateur
@app.post("/users", status_code=201)
async def create_user(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Le nom d'utilisateur existe déjà")
    hashed_password = get_password_hash(user.password)
    users_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed_password,
        "todos": []
    }
    return {"username": user.username, "todo_count": 0}

# Authentification et obtention du jeton
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Récupération des informations de l'utilisateur actuel
@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    todo_count = len(current_user["todos"])
    return {"username": current_user["username"], "todo_count": todo_count}

# Création d'un nouveau TODO
@app.post("/users/me/todo", status_code=201, response_model=TodoItem)
async def create_todo(todo: TodoCreate, current_user: dict = Depends(get_current_user)):
    global todo_id_counter
    todo_item = TodoItem(
        id=todo_id_counter,
        name=todo.name,
        description=todo.description,
        priority=todo.priority
    )
    todo_id_counter += 1
    current_user["todos"].append(todo_item)
    return todo_item

# Récupération de la liste des TODOs
@app.get("/users/me/todo", response_model=List[TodoItem])
async def get_todos(current_user: dict = Depends(get_current_user)):
    return sorted(current_user["todos"], key=lambda x: x.priority)

# Mise à jour d'un TODO
@app.patch("/users/me/todo/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, todo_update: TodoUpdate, current_user: dict = Depends(get_current_user)):
    for todo in current_user["todos"]:
        if todo.id == todo_id:
            if todo_update.name is not None:
                todo.name = todo_update.name
            if todo_update.description is not None:
                todo.description = todo_update.description
            if todo_update.priority is not None:
                todo.priority = todo_update.priority
            return todo
    raise HTTPException(status_code=404, detail="TODO introuvable")

# Suppression d'un TODO
@app.delete("/users/me/todo/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, current_user: dict = Depends(get_current_user)):
    for idx, todo in enumerate(current_user["todos"]):
        if todo.id == todo_id:
            del current_user["todos"][idx]
            return
    raise HTTPException(status_code=404, detail="TODO introuvable")
