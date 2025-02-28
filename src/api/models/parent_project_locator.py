from pydantic import BaseModel

class ParentProjectLocator(BaseModel):
    """DTO для локатора родительского проекта."""
    locator: str