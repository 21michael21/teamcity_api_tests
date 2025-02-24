import requests
from tests.base_api_test import BaseApiTest
import pytest


class TestBuildConfig(BaseApiTest):
    def test_user_should_be_able_to_get_all_projects(self):
        response = requests.get(
            f"{self.auth_spec['base_url']}/projects",
            headers=self.auth_spec["headers"],
            auth=self.auth_spec["auth"],
        )
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"
        projects = response.json()
        assert "project" in projects, "Response does not contain 'project' key"
        print(f"Found {len(projects['project'])} projects: {projects['project']}")
        
    def test_create_project(self):
        payload = {
            "parentProject": {"locator": "_Root"},
            "name": "test_project",
            "id": "test_project",
            "copyAllAssociatedSettings": True
    }
        response = requests.post(
            f"{self.auth_spec['base_url']}/projects",
            headers=self.auth_spec["headers"],
            auth=self.auth_spec["auth"],
            json=payload
    )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
