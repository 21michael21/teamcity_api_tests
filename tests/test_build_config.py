# tests/test_build_config.py
import pytest
import allure
from tests.base_api_test import BaseApiTest
from src.models import User
import time
import random

@allure.epic("Build Configuration")
@allure.feature("Create Build Type")
class TestBuildConfig(BaseApiTest):

    @allure.story("User can create Build Type")
    @allure.description("User should be able to create build type")
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.crud
    def test_create_build_type(self):
        unique_time = int(time.time() * 1000) + random.randint(1, 1000)
        with allure.step("Create user"):
            user_response = self.create_user(f"user_{unique_time}", "pass123")
            assert user_response.status_code == 200, f"User creation failed: {user_response.text}"
            user_id = user_response.json()["id"]
            user_auth = self.specs.auth_spec(User(username=user_response.json()["username"], password="pass123"))

        with allure.step("Create project by admin"):
            project_id = f"project_{unique_time}"
            project_response = self.create_project(project_id, self.auth_spec)
            assert project_response.status_code == 200, f"Project creation failed: {project_response.text}"

        with allure.step("Grant user PROJECT_ADMIN role in project"):
            role_response = self.grant_role(user_id, project_id, "PROJECT_ADMIN")
            assert role_response.status_code == 200, f"Role assignment failed: {role_response.text}"

        with allure.step("Create build type for project by user"):
            build_type_id = f"build_{unique_time}"
            build_response = self.create_build_type(build_type_id, project_id, user_auth)
            assert build_response.status_code == 200, f"Build type creation failed: {build_response.text}"

        with allure.step("Check build type was created successfully"):
            assert build_response.json()["id"] == build_type_id, "Build type ID mismatch"

    @allure.story("User cannot create duplicate Build Type IDs")
    @allure.description("User should not be able to create two build types with the same id")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.crud
    def test_duplicate_build_type(self):
        unique_time = int(time.time() * 1000) + random.randint(1, 1000)
        with allure.step("Create user"):
            user_response = self.create_user(f"user_{unique_time}", "pass123")
            assert user_response.status_code == 200, f"User creation failed: {user_response.text}"
            user_id = user_response.json()["id"]
            user_auth = self.specs.auth_spec(User(username=user_response.json()["username"], password="pass123"))

        with allure.step("Create project by admin"):
            project_id = f"project_{unique_time}"
            project_response = self.create_project(project_id, self.auth_spec)
            assert project_response.status_code == 200, f"Project creation failed: {project_response.text}"

        with allure.step("Grant user PROJECT_ADMIN role in project"):
            role_response = self.grant_role(user_id, project_id, "PROJECT_ADMIN")
            assert role_response.status_code == 200, f"Role assignment failed: {role_response.text}"

        with allure.step("Create first build type"):
            build_type_id = f"duplicate_build_{unique_time}"
            first_build_response = self.create_build_type(build_type_id, project_id, user_auth)
            assert first_build_response.status_code == 200, f"First build type creation failed: {first_build_response.text}"

        with allure.step("Create second build type with the same ID"):
            second_build_response = self.create_build_type(build_type_id, project_id, user_auth)
            assert second_build_response.status_code == 400, f"Expected 400, got {second_build_response.status_code}: {second_build_response.text}"

    @allure.story("Project Admin can create Build Type")
    @allure.description("Project admin should be able to create build type for their project")
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.roles
    def test_admin_create_build_type(self):
        unique_time = int(time.time() * 1000) + random.randint(1, 1000)
        with allure.step("Create user"):
            admin_response = self.create_user(f"admin_{unique_time}", "admin123", role="")
            assert admin_response.status_code == 200, f"Admin creation failed: {admin_response.text}"
            admin_id = admin_response.json()["id"]
            admin_auth = self.specs.auth_spec(User(username=admin_response.json()["username"], password="admin123"))

        with allure.step("Create project by admin"):
            project_id = f"project_{unique_time}"
            project_response = self.create_project(project_id, self.auth_spec)
            assert project_response.status_code == 200, f"Project creation failed: {project_response.text}"

        with allure.step("Grant user PROJECT_ADMIN role in project"):
            role_response = self.grant_role(admin_id, project_id, "PROJECT_ADMIN")
            assert role_response.status_code == 200, f"Role assignment failed: {role_response.text}"

        with allure.step("Create build type for project by admin"):
            build_type_id = f"build_{unique_time}"
            build_response = self.create_build_type(build_type_id, project_id, admin_auth)
            assert build_response.status_code == 200, f"Build type creation failed: {build_response.text}"

    @allure.story("Project Admin cannot create Build Type in another project")
    @allure.description("Project admin should not be able to create build type for not their project")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.roles
    def test_admin_create_build_type_in_foreign_project(self):
        unique_time = int(time.time() * 1000) + random.randint(1, 1000)
        with allure.step("Create user1 (admin)"):
            admin1_response = self.create_user(f"admin1_{unique_time}", "admin123", role="")
            assert admin1_response.status_code == 200, f"Admin1 creation failed: {admin1_response.text}"
            admin1_id = admin1_response.json()["id"]
            admin1_auth = self.specs.auth_spec(User(username=admin1_response.json()["username"], password="admin123"))

        with allure.step("Create project1 by admin"):
            project1_id = f"project1_{unique_time}"
            project1_response = self.create_project(project1_id, self.auth_spec)
            assert project1_response.status_code == 200, f"Project1 creation failed: {project1_response.text}"

        with allure.step("Grant user1 PROJECT_ADMIN role in project1"):
            role1_response = self.grant_role(admin1_id, project1_id, "PROJECT_ADMIN")
            assert role1_response.status_code == 200, f"Role assignment for user1 failed: {role1_response.text}"

        with allure.step("Create user2"):
            admin2_response = self.create_user(f"admin2_{unique_time + 1}", "admin456", role="")
            assert admin2_response.status_code == 200, f"Admin2 creation failed: {admin2_response.text}"
            admin2_id = admin2_response.json()["id"]
            admin2_auth = self.specs.auth_spec(User(username=admin2_response.json()["username"], password="admin456"))

        with allure.step("Clear user2 roles to ensure no default permissions"):
            clear_response = self.clear_user_roles(admin2_id)
            # Проверяем, что очистка либо успешна, либо ничего не требовалось (None)
            if clear_response is not None:
                assert clear_response.status_code in [200, 204], f"Failed to clear user2 roles: {clear_response.text}"

        with allure.step("Create project2 by admin"):
            project2_id = f"project2_{unique_time + 1}"
            project2_response = self.create_project(project2_id, self.auth_spec)
            assert project2_response.status_code == 200, f"Project2 creation failed: {project2_response.text}"

        with allure.step("Grant user2 PROJECT_ADMIN role in project2"):
            role2_response = self.grant_role(admin2_id, project2_id, "PROJECT_ADMIN")
            assert role2_response.status_code == 200, f"Role assignment for user2 failed: {role2_response.text}"

        with allure.step("Check user2 roles before creating build type"):
            roles_response = self.get_user_roles(admin2_id)
            assert roles_response.status_code == 200, f"Failed to get user2 roles: {roles_response.text}"

        with allure.step("Try to create build type in project1 by user2"):
            build_type_id = f"build_{unique_time + 2}"
            build_response = self.create_build_type(build_type_id, project1_id, admin2_auth)
            assert build_response.status_code == 403, f"Expected 403, got {build_response.status_code}: {build_response.text}"