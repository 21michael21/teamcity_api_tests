from src.requests.crud_interface import CrudInterface
from src.requests.request import Request
from src.enums.endpoint import Endpoint
import requests

class UncheckedBase(Request, CrudInterface):
    """Шаблон для непроверяемых запросов CRUD эндпоинтов."""
    
    def __init__(self, spec: requests.Session, endpoint: Endpoint):
        """
        Инициализация непроверяемого запроса.
        
        Args:
            spec (requests.Session): Спецификация запроса (объект сессии requests).
            endpoint (Endpoint): Эндпоинт для запроса.
        """
        super().__init__(spec, endpoint)
    
    def create(self, model: dict) -> requests.Response:
        """Создание нового объекта."""
        return self.spec.post(
            self.endpoint.url,
            json=model
        )
    
    def read(self, id: str) -> requests.Response:
        """Чтение объекта по ID."""
        return self.spec.get(
            f"{self.endpoint.url}/id:{id}"
        )
    
    def update(self, id: str, model: dict) -> requests.Response:
        """Обновление объекта по ID."""
        return self.spec.put(
            f"{self.endpoint.url}/id:{id}",
            json=model
        )
    
    def delete(self, id: str) -> requests.Response:
        """Удаление объекта по ID."""
        return self.spec.delete(
            f"{self.endpoint.url}/id:{id}"
        )