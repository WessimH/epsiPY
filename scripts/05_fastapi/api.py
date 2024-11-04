from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED

app = FastAPI()

class UserForm(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/user")
async def signup(user_form: UserForm, response: Response):
    print("Creating ", user_form)
    response.status_code = HTTP_201_CREATED
    return UserResponse(username=user_form.username)