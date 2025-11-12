from src.api.requests.crud_interface import CrudInterface
from src.api.requests.request import Request
from src.enums.endpoint import Endpoint
import requests

class UncheckedBase(Request, CrudInterface):
    """Шаблон для непроверяемых запросов CRUD эндпоинтов."""
    
    def __init__(self, spec: requests.Session, endpoint: Endpoint):
        super().__init__(spec, endpoint)
    
    def create(self, model: dict) -> requests.Response:
        return self.spec.post(
            self.endpoint.url,
            json=model
        )
    
    def read(self, id: str) -> requests.Response:
        return self.spec.get(
            f"{self.endpoint.url}/id:{id}"
        )
    
    def update(self, id: str, model: dict) -> requests.Response:
        return self.spec.put(
            f"{self.endpoint.url}/id:{id}",
            json=model
        )
    
    def delete(self, id: str) -> requests.Response:
        return self.spec.delete(
            f"{self.endpoint.url}/id:{id}"
        )