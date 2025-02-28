from pydantic import BaseModel
from typing import Optional
from .parent_project_locator import ParentProjectLocator

class Project(BaseModel):
    """DTO для проекта."""
    id: str
    name: str
    locator: str = "_Root"
    parentProjectLocator: Optional[ParentProjectLocator] = None