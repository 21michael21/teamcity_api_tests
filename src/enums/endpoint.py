from enum import Enum
from src.models.build_type import BuildType

class Endpoint(Enum):
    """Перечисление эндпоинтов с URL и моделью для сериализации/десериализации."""
    
    BUILD_TYPES = ("/app/rest/buildTypes", BuildType)
    
    def __init__(self, url: str, model_class):
        self.url = url
        self.model_class = model_class