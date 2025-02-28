from src.api.requests.crud_interface import CrudInterface
from src.api.requests.request import Request
from src.requests.unchecked.unchecked_base import UncheckedBase
from src.enums.endpoint import Endpoint
from src.api.models.base_model import BaseModel
import requests
import pytest

class CheckedBase(Request, CrudInterface):
    """Шаблон для проверяемых запросов CRUD эндпоинтов."""
    
    def __init__(self, spec: requests.Session, endpoint: Endpoint):
        super().__init__(spec, endpoint)
        self.unchecked_base = UncheckedBase(spec, endpoint)
    
    def create(self, model: dict) -> BaseModel:
        response = self.unchecked_base.create(model)
        ValidationResponseSpecifications.validate_success(response)
        return self.endpoint.model_class(**response.json())
    
    def read(self, id: str) -> BaseModel:
        response = self.unchecked_base.read(id)
        ValidationResponseSpecifications.validate_success(response)
        return self.endpoint.model_class(**response.json())
    
    def update(self, id: str, model: dict) -> BaseModel:
        response = self.unchecked_base.update(id, model)
        ValidationResponseSpecifications.validate_success(response)
        return self.endpoint.model_class(**response.json())
    
    def delete(self, id: str) -> str:
        response = self.unchecked_base.delete(id)
        ValidationResponseSpecifications.validate_success(response)
        return response.text