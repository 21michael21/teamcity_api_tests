from pydantic import BaseModel
from typing import List, Optional

class Role(BaseModel):
    """DTO для роли пользователя."""
    roleId: str
    scope: str

class Roles(BaseModel):
    """DTO для списка ролей пользователя."""
    role: Optional[List[Role]] = None