from fastapi import APIRouter, Depends
from pydantic import BaseModel
from application.services.user_service import UserService
from adapters.api.dependencies import get_user_service

router = APIRouter(prefix="/api", tags=["Users"])


class UserCreate(BaseModel):
    nombre: str
    email: str


@router.post("/users")
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    result = service.create_user(user.nombre, user.email)
    if result is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail="El email ya está registrado")
    return result


@router.get("/users")
def list_users(service: UserService = Depends(get_user_service)):
    return service.list_users()
