from src.enums.endpoint import Endpoint
from pydantic import BaseModel
import requests

class Request:
    """Класс, описывающий меняющиеся параметры запроса (спецификация, эндпоинт)."""
    
    def __init__(self, spec: requests.Request, endpoint: Endpoint):
        """
        Инициализация запроса.
        
        Args:
            spec (requests.Request): Спецификация запроса (например, объект requests).
            endpoint (Endpoint): Эндпоинт для запроса.
        """
        self.spec = spec
        self.endpoint = endpoint
    
    def get_url(self) -> str:
        """Возвращает URL эндпоинта."""
        return self.endpoint.url
    
    def get_model_class(self):
        """Возвращает класс модели для сериализации/десериализации."""
        return self.endpoint.model_class