from abc import ABC, abstractmethod
from src.models.base_model import BaseModel

class CrudInterface(ABC):
    """Интерфейс для поддержки CRUD-операций."""
    
    @abstractmethod
    def create(self, model: BaseModel):
        """Создание нового объекта."""
        pass
    
    @abstractmethod
    def read(self, id: str):
        """Чтение объекта по ID."""
        pass
    
    @abstractmethod
    def update(self, id: str, model: BaseModel):
        """Обновление объекта по ID."""
        pass
    
    @abstractmethod
    def delete(self, id: str):
        """Удаление объекта по ID."""
        pass