import requests

class Specifications:
    """Класс для создания спецификаций запросов к TeamCity API."""
    
    def auth_spec(self, user: dict) -> dict:
        """Создаёт спецификацию с авторизацией."""
        return {
            "base_url": "http://localhost:8111",
            "headers": {"Content-Type": "application/json"},
            "auth": (user["username"], user["password"])
        }