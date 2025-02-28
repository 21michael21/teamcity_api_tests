from src.api.requests.unchecked.unchecked_base import UncheckedBase
from src.api.requests.checked.checked_base import CheckedBase
from src.enums.endpoint import Endpoint
import requests

class CrudRequests:
    """Класс для работы с CRUD запросами к TeamCity API."""
    
    def __init__(self, base_url: str, username: str, password: str):
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.base_url = base_url
    
    def unchecked(self, endpoint: Endpoint) -> UncheckedBase:
        """Возвращает экземпляр непроверяемого запроса."""
        return UncheckedBase(self.session, endpoint)
    
    def checked(self, endpoint: Endpoint) -> CheckedBase:
        """Возвращает экземпляр проверяемого запроса."""
        return CheckedBase(self.session, endpoint)