import requests
import time
from tests.base_api_test import BaseApiTest
import pytest
import requests_mock

class TestBuildConfig(BaseApiTest):
    def test_user_should_be_able_to_get_all_projects(self):
        response = requests.get(
            f"{self.auth_spec['base_url']}/projects",
            headers=self.auth_spec["headers"],
            auth=self.auth_spec["auth"],
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        projects = response.json()
        assert "project" in projects, "Response does not contain 'project' key"
        print(f"Found {len(projects['project'])} projects: {projects['project']}")

    def test_run_build_with_hello_world(self):
        project_id = f"test_project_{int(time.time())}"
        build_type_id = f"test_build_{int(time.time())}"

        self.create_project(project_id)
        self.create_build_type(build_type_id, project_id)
        build_id = self.queue_build(build_type_id)
        status = self.wait_for_build(build_id)
        
        assert status == "SUCCESS", f"Build failed with status: {status}"
        print("Build completed successfully with 'Hello, world!'")

    def test_run_build_with_hello_world_mocked(self):
        project_id = "mocked_project"
        build_type_id = "mocked_build"
        build_id = 123

        with requests_mock.Mocker() as m:
            m.post(f"{self.auth_spec['base_url']}/projects", json={"id": project_id}, status_code=200)
            m.post(f"{self.auth_spec['base_url']}/buildTypes", json={"id": build_type_id}, status_code=200)
            m.post(f"{self.auth_spec['base_url']}/buildQueue", json={"id": build_id}, status_code=200)
            m.get(f"{self.auth_spec['base_url']}/builds/id:{build_id}", json={"id": build_id, "state": "finished", "status": "SUCCESS"}, status_code=200)

            self.create_project(project_id)
            self.create_build_type(build_type_id, project_id)
            build_id = self.queue_build(build_type_id)
            status = self.wait_for_build(build_id)

            assert status == "SUCCESS", f"Mocked build failed with status: {status}"
            print("Mocked build completed successfully")

    def test_find_project_by_name(self):
        project_id = f"searchable_project_{int(time.time())}"
        self.create_project(project_id)

        response = requests.get(
            f"{self.auth_spec['base_url']}/projects/name:{project_id}",
            headers=self.auth_spec["headers"],
            auth=self.auth_spec["auth"],
        )
        assert response.status_code == 200, f"Project search failed: {response.text}"
        project_data = response.json()
        assert project_data["id"] == project_id, f"Expected project ID {project_id}, got {project_data['id']}"
        print(f"Project '{project_id}' found successfully")