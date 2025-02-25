from pydantic import BaseModel
from .project import Project
from .steps import Steps

class BuildType(BaseModel):
    """Модель для BuildType."""
    id: str | None = None
    name: str
    project: Project
    steps: Steps | None = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True