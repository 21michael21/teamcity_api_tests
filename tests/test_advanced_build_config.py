import sys
import os
import random
import time
from faker import Faker
import pytest
import requests_mock
from src.api.models.project import Project
from src.api.models.build_type import BuildType, Step, Steps
from src.api.models.user import User
from src.api.specs.specifications import Specifications
from src.api.requests.crud_requests import CrudRequests
from src.api.requests.unchecked.unchecked_base import UncheckedBase
from src.api.requests.checked.checked_base import CheckedBase
from src.enums.endpoint import Endpoint

# Добавляем путь к модулям в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

fake = Faker()

def generate_test_user(role_id="PROJECT_ADMIN", scope_type="g"):
    """Генерирует тестового пользователя с ролью и областью."""
    return User(
        username=fake.user_name(),
        password=fake.password(),
        email=fake.email(),
        roles=None  # Роли можно добавить позже, если нужно
    )

class TestAdvancedBuildConfig:
    def setup_method(self):
        self.user = generate_test_user()
        self.specs = Specifications()
        self.auth_spec = self.specs.auth_spec(self.user)
        self.crud = CrudRequests(self.auth_spec["base_url"], self.user.username, self.user.password)
    
    def create_project(self, project_id):
        """Создание проекта с использованием DTO."""
        project = Project(id=project_id, name=project_id, parentProjectLocator={"locator": "_Root"})
        response = self.crud.unchecked(Endpoint.BUILD_TYPES).create(project.dict(exclude_none=True))
        assert response.status_code == 200, f"Project creation failed: {response.text}"
        project_data = response.json()
        assert project_data["id"] == project_id, f"Expected project ID {project_id}, got {project_data['id']}"
        assert project_data["name"] == project_id, f"Expected project name {project_id}, got {project_data['name']}"
        print(f"Project '{project_id}' created")
        return project_id
    
    def create_build_type(self, build_type_id, project_id):
        """Создание типа билда с echo 'Hello, world!'."""
        project = Project(id=project_id, name=project_id)
        step = Step(name="Echo Hello World", type="simpleRunner")
        steps = Steps(count=1, steps=[step])
        build_type = BuildType(
            id=build_type_id,
            name="Print Hello World",
            project=project,
            steps=steps
        )
        response = self.crud.unchecked(Endpoint.BUILD_TYPES).create(build_type.dict(exclude_none=True))
        assert response.status_code == 200, f"Build type creation failed: {response.text}"
        build_type_data = response.json()
        assert build_type_data["id"] == build_type_id, f"Expected build type ID {build_type_id}, got {build_type_data['id']}"
        assert build_type_data["name"] == "Print Hello World", f"Expected build type name 'Print Hello World', got {build_type_data['name']}"
        print(f"Build type '{build_type_id}' created")
        return build_type_id
    
    def queue_build(self, build_type_id):
        """Запуск билда в очереди."""
        payload = {"buildType": {"id": build_type_id}}
        response = self.crud.unchecked(Endpoint.BUILD_TYPES).create(payload)
        assert response.status_code == 200, f"Build queue failed: {response.text}"
        build_id = response.json()["id"]
        assert isinstance(build_id, int), f"Expected build ID to be an integer, got {build_id}"
        print(f"Build queued with ID: {build_id}")
        return build_id
    
    def wait_for_build(self, build_id, timeout=60):
        """Ожидание завершения билда."""
        for attempt in range(timeout):
            response = self.crud.unchecked(Endpoint.BUILD_TYPES).read(str(build_id))
            if response.status_code == 200:
                build_data = response.json()
                state = build_data.get("state")
                status = build_data.get("status")
                print(f"Attempt {attempt + 1}: State={state}, Status={status}")
                if state == "finished":
                    assert status in ["SUCCESS", "FAILURE"], f"Unexpected build status: {status}"
                    return status
            time.sleep(1)
        raise TimeoutError(f"Build {build_id} did not finish in {timeout} seconds")
    
    @pytest.mark.advanced
    def test_run_build_with_hello_world(self):
        """Тест на запуск билда и успешную сборку с echo 'Hello, world!'."""
        project_id = f"test_project_{int(time.time())}"
        build_type_id = f"test_build_{int(time.time())}"
        
        self.create_project(project_id)
        self.create_build_type(build_type_id, project_id)
        build_id = self.queue_build(build_type_id)
        status = self.wait_for_build(build_id)
        
        assert status == "SUCCESS", f"Build failed with status: {status}"
        print("Build completed successfully with 'Hello, world!'")
    
    @pytest.mark.advanced
    def test_run_build_with_hello_world_mocked(self):
        """Тест на запуск билда с замокированным ответом."""
        project_id = f"mocked_project_{int(time.time())}"
        build_type_id = f"mocked_build_{int(time.time())}"
        build_id = 123
        
        with requests_mock.Mocker() as m:
            m.post(f"{self.auth_spec['base_url']}/app/rest/buildTypes", json={"id": project_id}, status_code=200)
            m.post(f"{self.auth_spec['base_url']}/app/rest/buildTypes", json={"id": build_type_id}, status_code=200)
            m.post(f"{self.auth_spec['base_url']}/app/rest/buildQueue", json={"id": build_id}, status_code=200)
            m.get(f"{self.auth_spec['base_url']}/app/rest/builds/id:{build_id}", json={"id": build_id, "state": "finished", "status": "SUCCESS"}, status_code=200)
            
            self.create_project(project_id)
            self.create_build_type(build_type_id, project_id)
            build_id = self.queue_build(build_type_id)
            status = self.wait_for_build(build_id)
            
            assert status == "SUCCESS", f"Mocked build failed with status: {status}"
            print("Mocked build completed successfully")
    
    @pytest.mark.advanced
    def test_find_project_by_name(self):
        """Тест на поиск проекта по имени с проверкой тела ответа."""
        project_id = f"searchable_project_{int(time.time())}"
        self.create_project(project_id)
        
        response = self.crud.unchecked(Endpoint.BUILD_TYPES).read(f"name:{project_id}")
        assert response.status_code == 200, f"Project search failed: {response.text}"
        project_data = response.json()
        assert project_data["id"] == project_id, f"Expected project ID {project_id}, got {project_data['id']}"
        assert project_data["name"] == project_id, f"Expected project name {project_id}, got {project_data['name']}"
        assert "locator" in project_data, "Response does not contain 'locator' key"
        assert project_data["locator"] == "_Root", f"Expected locator '_Root', got {project_data['locator']}"
        print(f"Project '{project_id}' found successfully")