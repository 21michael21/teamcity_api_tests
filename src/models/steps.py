from pydantic import BaseModel

class Step(BaseModel):
    """Модель для Step."""
    id: str | None = None
    name: str | None = None
    type: str = "simpleRunner"
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True