from fastapi import APIRouter
from fastapi import HTTPException, Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from config.database import Session
from models.movies import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get('/movies', tags=['movies'], response_model=list[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> list[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        raise JSONResponse(status_code=404, detail='Movie Not found')
    return result

@movie_router.get('/movies/', tags=['movies'], response_model=list[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        raise JSONResponse(status_code=404, detail='Movie Not found')
    return result

#    Usamdo lambda:
# def get_movies_by_category(category: str,year:int):
#     return list(filter(lambda x: x['category'] == category, movies))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    
    return {"message": "Movie registered"}

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
         raise HTTPException(status_code=404, detail='Movie Not found')
    
    MovieService(db).update_movie(id, movie)
    return {"message": f"Movie with ID {id} updated"}

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) ->dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
         raise HTTPException(status_code=404, detail='Movie Not found')
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": f"Movie with ID {id} deleted"})
