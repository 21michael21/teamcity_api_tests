from pydantic import BaseModel

class Property(BaseModel):
    """DTO для свойства."""
    name: str
    value: str