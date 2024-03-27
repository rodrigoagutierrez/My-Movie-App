from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from schemas.user import User

auth_router = APIRouter()


@auth_router.post('/', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'password':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)