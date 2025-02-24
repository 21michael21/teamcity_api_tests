from tests.base_test import BaseTest
from src.specifications import Specifications
from src.models import User


class BaseApiTest(BaseTest):
    def setup_method(self):
        super().setup_method()
        self.specs = Specifications()
        self.user = User(username="admin", password="admin")
        self.auth_spec = self.specs.auth_spec(self.user)
