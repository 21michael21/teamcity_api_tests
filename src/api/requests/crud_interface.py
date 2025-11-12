from abc import ABC, abstractmethod
from src.api.models.base_model import BaseModel

class CrudInterface(ABC):
    """Интерфейс для поддержки CRUD-операций."""
    
    @abstractmethod
    def create(self, model: dict) -> BaseModel:
        """Создание нового объекта."""
        pass
    
    @abstractmethod
    def read(self, id: str) -> BaseModel:
        """Чтение объекта по ID."""
        pass
    
    @abstractmethod
    def update(self, id: str, model: dict) -> BaseModel:
        """Обновление объекта по ID."""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> str:
        """Удаление объекта по ID."""
        pass