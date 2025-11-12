from pydantic import BaseModel
from typing import List, Optional
from .property import Property

class Properties(BaseModel):
    """DTO для списка свойств."""
    property: Optional[List[Property]] = None