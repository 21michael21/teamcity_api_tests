from pydantic import BaseModel

class Project(BaseModel):
    """Модель для Project."""
    id: str | None = None
    name: str
    locator: str = "_Root"
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True