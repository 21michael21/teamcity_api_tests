from pydantic import BaseModel

class Step(BaseModel):
    """DTO для шага билда."""
    id: str | None = None
    name: str
    type: str = "simpleRunner"