from pydantic import BaseModel
from typing import Optional
from .project import Project
from .steps import Steps

class BuildType(BaseModel):
    """DTO для типа билда."""
    id: str
    name: str
    project: Project
    steps: Optional[Steps] = None