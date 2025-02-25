from pydantic import BaseModel as PydanticBaseModel

class BaseModel(PydanticBaseModel):
    """Базовая модель для всех моделей API."""
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True