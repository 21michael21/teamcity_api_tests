from pydantic import BaseModel
from typing import List, Optional
from .step import Step

class Steps(BaseModel):
    """DTO для списка шагов билда."""
    count: Optional[int] = None
    steps: Optional[List[Step]] = None