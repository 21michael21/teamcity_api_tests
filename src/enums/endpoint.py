from enum import Enum
from src.api.models.build_type import BuildType
from src.api.models.project import Project

class Endpoint(Enum):
    """Перечисление эндпоинтов с URL и моделью для сериализации/десериализации."""
    
    BUILD_TYPES = ("/app/rest/buildTypes", BuildType)
    PROJECTS = ("/app/rest/projects", Project)
    
    def __init__(self, url: str, model_class):
        self.url = url
        self.model_class = model_class