from pydantic import BaseModel
from typing import List, Optional
from .step import Step

class Steps(BaseModel):
    """Модель для Steps."""
    count: Optional[int] = None
    step: Optional[List[Step]] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True