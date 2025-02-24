import requests
from src.config import Config
from src.models import User

class Specifications:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Specifications, cls).__new__(cls)
        return cls._instance

    def _base_spec(self):
        return {
            "base_url": f"http://{Config.get_property('host')}/app/rest",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        }

    def unauth_spec(self):
        return self._base_spec()

    def auth_spec(self, user: User):
        spec = self._base_spec()
        spec["auth"] = (user.username, user.password)
        return spec

# Пример использования
if __name__ == "__main__":
    spec = Specifications()
    user = User("admin", "admin")
    auth_spec = spec.auth_spec(user)
    print(auth_spec)