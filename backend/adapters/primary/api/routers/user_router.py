from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from application.services.user_service import UserService
from adapters.primary.api.dependencies import get_user_service
from domain.exceptions import UserAlreadyExistsError

router = APIRouter(prefix="/api", tags=["Users"])


class UserCreate(BaseModel):
    nombre: str
    email: str


@router.post("/users")
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.create_user(user.nombre, user.email)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/users")
def list_users(service: UserService = Depends(get_user_service)):
    return service.list_users()
