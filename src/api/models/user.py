from pydantic import BaseModel
from typing import Optional
from .roles import Roles

class User(BaseModel):
    """DTO для пользователя."""
    username: str
    password: str
    email: Optional[str] = None
    roles: Optional[Roles] = None