import pytest
import allure
import time
import random
from src.api.models.project import Project
from src.api.models.build_type import BuildType, Step, Steps
from src.api.models.user import User
from src.api.specs.specifications import Specifications
from src.api.requests.crud_requests import CrudRequests
from src.enums.endpoint import Endpoint
from src.api.requests.checked.checked_base import CheckedBase
from src.utils.role_generator import generate_random_string, RoleGenerator
from src.utils.validation_response_specs import ValidationResponseSpecifications

@allure.epic("Build Configuration")
@allure.feature("Create Build Type")
class TestBuildConfig:
    def setup_method(self):
        self.user = User(username="admin", password="admin")
        self.specs = Specifications()
        self.auth_spec = self.specs.auth_spec(self.user)
        self.crud = CrudRequests(self.auth_spec["base_url"], self.user.username, self.user.password)
    
    @allure.story("User can create Build Type")
    @allure.description("User should be able to create build type")
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.crud
    def test_create_build_type(self):
        project_id = generate_random_string()
        build_type_id = generate_random_string()
        
        with allure.step("Create project by admin"):
            project = Project(id=project_id, name=project_id, parentProjectLocator={"locator": "_Root"})
            response = self.crud.checked(Endpoint.PROJECTS).create(project.dict(exclude_none=True))
            assert response.id == project_id, f"Project ID mismatch: expected {project_id}, got {response.id}"
            ValidationResponseSpecifications.validate_body(response, project_id, "name")
        
        with allure.step("Create build type for project by user"):
            project = Project(id=project_id, name=project_id)
            step = Step(name="Echo Hello World", type="simpleRunner")
            steps = Steps(count=1, steps=[step])
            build_type = BuildType(id=build_type_id, name="Build " + build_type_id, project=project, steps=steps)
            response = self.crud.checked(Endpoint.BUILD_TYPES).create(build_type.dict(exclude_none=True))
            assert response.id == build_type_id, f"Build type ID mismatch: expected {build_type_id}, got {response.id}"
            assert response.name == "Build " + build_type_id, f"Build type name mismatch"
            ValidationResponseSpecifications.validate_body(response, build_type_id, "name")
        
        with allure.step("Check build type was created successfully"):
            print(f"Build type '{build_type_id}' created successfully")
    
    @allure.story("User cannot create duplicate Build Type IDs")
    @allure.description("User should not be able to create two build types with the same id")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.crud
    def test_duplicate_build_type(self):
        project_id = generate_random_string()
        build_type_id = generate_random_string()
        
        with allure.step("Create project by admin"):
            project = Project(id=project_id, name=project_id, parentProjectLocator={"locator": "_Root"})
            self.crud.checked(Endpoint.PROJECTS).create(project.dict(exclude_none=True))
        
        with allure.step("Create first build type"):
            project = Project(id=project_id, name=project_id)
            step = Step(name="Echo Hello World", type="simpleRunner")
            steps = Steps(count=1, steps=[step])
            build_type = BuildType(id=build_type_id, name="Build " + build_type_id, project=project, steps=steps)
            self.crud.checked(Endpoint.BUILD_TYPES).create(build_type.dict(exclude_none=True))
        
        with allure.step("Create second build type with the same ID"):
            response = self.crud.unchecked(Endpoint.BUILD_TYPES).create(build_type.dict(exclude_none=True))
            ValidationResponseSpecifications.validate_error(
                response,
                expected_status=400,
                expected_error_message="Build type with id"
            )
            print("Duplicate build type creation blocked successfully")
    
    @allure.story("Project Admin can create Build Type")
    @allure.description("Project admin should be able to create build type for their project")
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.roles
    def test_admin_create_build_type(self):
        project_id = generate_random_string()
        user_id = generate_random_string()
        
        with allure.step("Create project by admin"):
            project = Project(id=project_id, name=project_id, parentProjectLocator={"locator": "_Root"})
            self.crud.checked(Endpoint.PROJECTS).create(project.dict(exclude_none=True))
        
        with allure.step("Create user without global roles"):
            user = User(username=user_id, password="admin123", email=f"{user_id}@example.com")
            response = self.crud.checked(Endpoint.PROJECTS).create(user.dict(exclude_none=True))
            assert response.username == user_id, f"User creation failed: expected {user_id}, got {response.username}"
        
        with allure.step("Grant user PROJECT_ADMIN role in project"):
            self.crud.checked(Endpoint.PROJECTS).update(f"id:{response.id}/roles", RoleGenerator.generate_project_admin_role(project_id))
        
        with allure.step("Create build type for project by admin"):
            project = Project(id=project_id, name=project_id)
            step = Step(name="Echo Hello World", type="simpleRunner")
            steps = Steps(count=1, steps=[step])
            build_type_id = generate_random_string()
            build_type = BuildType(id=build_type_id, name="Build " + build_type_id, project=project, steps=steps)
            admin_auth = Specifications().auth_spec(User(username=user_id, password="admin123"))
            crud = CrudRequests(admin_auth["base_url"], user_id, "admin123")
            response = crud.checked(Endpoint.BUILD_TYPES).create(build_type.dict(exclude_none=True))
            assert response.id == build_type_id, f"Build type creation failed: expected {build_type_id}, got {response.id}"
            ValidationResponseSpecifications.validate_body(response, build_type_id, "name")
            print("Build type created successfully by project admin")
    
    @allure.story("Project Admin cannot create Build Type in another project")
    @allure.description("Project admin should not be able to create build type for not their project")
    @pytest.mark.regression
    @pytest.mark.negative
    @pytest.mark.roles
    def test_admin_create_build_type_in_foreign_project(self):
        project1_id = generate_random_string()
        project2_id = generate_random_string()
        user1_id = generate_random_string()
        user2_id = generate_random_string()
        
        with allure.step("Create project1 by admin"):
            project1 = Project(id=project1_id, name=project1_id, parentProjectLocator={"locator": "_Root"})
            self.crud.checked(Endpoint.PROJECTS).create(project1.dict(exclude_none=True))
        
        with allure.step("Create user1 (admin)"):
            user1 = User(username=user1_id, password="admin123", email=f"{user1_id}@example.com")
            response1 = self.crud.checked(Endpoint.PROJECTS).create(user1.dict(exclude_none=True))
            assert response1.username == user1_id, f"User1 creation failed: expected {user1_id}, got {response1.username}"
        
        with allure.step("Grant user1 PROJECT_ADMIN role in project1"):
            self.crud.checked(Endpoint.PROJECTS).update(f"id:{response1.id}/roles", RoleGenerator.generate_project_admin_role(project1_id))
        
        with allure.step("Create user2"):
            user2 = User(username=user2_id, password="admin456", email=f"{user2_id}@example.com")
            response2 = self.crud.checked(Endpoint.PROJECTS).create(user2.dict(exclude_none=True))
            assert response2.username == user2_id, f"User2 creation failed: expected {user2_id}, got {response2.username}"
        
        with allure.step("Clear user2 roles to ensure no default permissions"):
            self.crud.unchecked(Endpoint.PROJECTS).delete(f"id:{response2.id}/roles")
        
        with allure.step("Create project2 by admin"):
            project2 = Project(id=project2_id, name=project2_id, parentProjectLocator={"locator": "_Root"})
            self.crud.checked(Endpoint.PROJECTS).create(project2.dict(exclude_none=True))
        
        with allure.step("Grant user2 PROJECT_ADMIN role in project2"):
            self.crud.checked(Endpoint.PROJECTS).update(f"id:{response2.id}/roles", RoleGenerator.generate_project_admin_role(project2_id))
        
        with allure.step("Check user2 roles before creating build type"):
            roles_response = self.crud.unchecked(Endpoint.PROJECTS).read(f"id:{response2.id}/roles")
            ValidationResponseSpecifications.validate_success(roles_response)
            print(f"User {user2_id} roles: {roles_response.text}")
        
        with allure.step("Try to create build type in project1 by user2"):
            project = Project(id=project1_id, name=project1_id)
            step = Step(name="Echo Hello World", type="simpleRunner")
            steps = Steps(count=1, steps=[step])
            build_type_id = generate_random_string()
            build_type = BuildType(id=build_type_id, name="Build " + build_type_id, project=project, steps=steps)
            admin2_auth = Specifications().auth_spec(User(username=user2_id, password="admin456"))
            crud2 = CrudRequests(admin2_auth["base_url"], user2_id, "admin456")
            response = crud2.unchecked(Endpoint.BUILD_TYPES).create(build_type.dict(exclude_none=True))
            ValidationResponseSpecifications.validate_error(
                response,
                expected_status=403,
                expected_error_message="Access denied"
            )
            print("Build type creation in foreign project blocked successfully")