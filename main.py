from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from models.movies import Movie
from routers.movie import movie_router
from routers.auth import auth_router


app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)



movies: list[Movie] = [
    {
    "id": 1,
    "title": "Avatar",
    "overview": "En una exuberante planeta llamado Pandora viven los Na'vi",
    "year": "2009",
    "rating": 7.8,
    "category": "Acción"
    },
    {
    "id": 2,
    "title": "Avatar",
    "overview": "En una exuberante planeta llamado Pandora viven los Na'vi",
    "year": "2010",
    "rating": 7.8,
    "category": "Acción"
    },
    {
    "id": 3,
    "title": "Avatar",
    "overview": "En una exuberante planeta llamado Pandora viven los Na'vi",
    "year": "2015",
    "rating": 7.8,
    "category": "Acción"
    }
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')


    
