# tests/base_api_test.py
import random
import logging
import requests

from src.models import User
from src.api.models.user import User
from tests.base_test import BaseTest
from src.enums.endpoint import Endpoint
from src.specifications import Specifications
from src.api.models.project import Project
from src.api.models.build_type import BuildType, Step, Steps
from src.api.specs.specifications import Specifications
from src.api.requests.crud_requests import CrudRequests
from src.utils.role_generator import generate_random_string, generate_instance, RoleGenerator
from src.utils.validation_response_specs import ValidationResponseSpecifications
from src.api.requests.checked.checked_base import CheckedBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseApiTest(BaseTest):
    def setup_method(self):
        super().setup_method()
        self.specs = Specifications()
        self.user = User(username="admin", password="admin")
        self.auth_spec = self.specs.auth_spec(self.user)

    def create_user(
        self, username="test_user", password="test_pass", role="PROJECT_DEVELOPER"
    ):
        """Создание пользователя."""
        payload = {
            "username": username,
            "password": password,
            "name": username,
            "email": f"{username}@example.com",
        }
        if role:
            payload["roles"] = {"role": [{"roleId": role, "scope": "g"}]}
        logger.info(f"Creating user with payload: {payload}")
        print(f"Creating user with payload: {payload}")
        response = requests.post(
            f"{self.auth_spec['base_url']}/users",
            headers=self.auth_spec["headers"],
            auth=self.auth_spec["auth"],
            json=payload,
        )
        logger.info(f"User creation response: {response.status_code} - {response.text}")
        print(f"User creation response: {response.status_code} - {response.text}")
        return response

    def create_project(self, project_id, user_auth):
        """Создание проекта."""
        payload = {
            "id": project_id,
            "name": project_id,
            "parentProject": {"locator": "_Root"},
        }
        logger.info(f"Creating project with payload: {payload}")
        print(f"Creating project with payload: {payload}")
        response = requests.post(
            f"{self.auth_spec['base_url']}/projects",
            headers=user_auth["headers"],
            auth=user_auth["auth"],
            json=payload,
        )
        logger.info(
            f"Project creation response: {response.status_code} - {response.text}"
        )
        print(f"Project creation response: {response.status_code} - {response.text}")
        return response

    def create_build_type(self, build_type_id, project_id, user_auth):
        """Создание билд-конфигурации."""
        payload = {
            "id": build_type_id,
            "name": f"Build {build_type_id}",
            "project": {"id": project_id},
        }
        logger.info(f"Creating build type with payload: {payload}")
        print(f"Creating build type with payload: {payload}")
        response = requests.post(
            f"{self.auth_spec['base_url']}/buildTypes",
            headers=user_auth["headers"],
            auth=user_auth["auth"],
            json=payload,
        )
        logger.info(
            f"Build type creation response: {response.status_code} - {response.text}"
        )
        print(f"Build type creation response: {response.status_code} - {response.text}")
        return response

    def grant_role(self, user_id, project_id, role="PROJECT_ADMIN"):
        """Назначение роли пользователю в проекте."""
        payload = {"role": [{"roleId": role, "scope": f"p:{project_id}"}]}
        logger.info(
            f"Granting role {role} to user {user_id} in project {project_id}: {payload}"
        )
        print(
            f"Granting role {role} to user {user_id} in project {project_id}: {payload}"
        )
        response = requests.put(
            f"{self.auth_spec['base_url']}/users/id:{user_id}/roles",
            headers=self.auth_spec["headers"],
            auth=self.auth_spec["auth"],
            json=payload,
        )
        logger.info(
            f"Role assignment response: {response.status_code} - {response.text}"
        )
        print(f"Role assignment response: {response.status_code} - {response.text}")
        return response

    def get_user_roles(self, user_id):
        """Получение текущих ролей пользователя."""
        response = requests.get(
            f"{self.auth_spec['base_url']}/users/id:{user_id}/roles",
            headers=self.auth_spec["headers"],
            auth=self.auth_spec["auth"],
        )
        logger.info(
            f"User {user_id} roles response: {response.status_code} - {response.text}"
        )
        print(
            f"User {user_id} roles response: {response.status_code} - {response.text}"
        )
        return response

    def clear_user_roles(self, user_id):
        """Очистка всех ролей пользователя."""
        # Сначала получаем текущие роли
        roles_response = self.get_user_roles(user_id)
        if roles_response.status_code != 200:
            logger.error(
                f"Failed to get roles for user {user_id}: {roles_response.text}"
            )
            return roles_response

        roles = roles_response.json().get("role", [])
        if not roles:
            logger.info(f"No roles to clear for user {user_id}")
            print(f"No roles to clear for user {user_id}")
            return None

        # Удаляем каждую роль индивидуально
        for role in roles:
            role_id = role["roleId"]
            scope = role["scope"]
            logger.info(
                f"Removing role {role_id} with scope {scope} for user {user_id}"
            )
            print(f"Removing role {role_id} with scope {scope} for user {user_id}")
            response = requests.delete(
                f"{self.auth_spec['base_url']}/users/id:{user_id}/roles/{role_id}/{scope}",
                headers=self.auth_spec["headers"],
                auth=self.auth_spec["auth"],
            )
            logger.info(
                f"Remove role response: {response.status_code} - {response.text}"
            )
            print(f"Remove role response: {response.status_code} - {response.text}")
            if response.status_code not in [200, 204]:
                return response
        return None
