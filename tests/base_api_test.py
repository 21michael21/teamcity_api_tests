import requests
import time
from tests.base_test import BaseTest
from src.specifications import Specifications
from src.models import User


class BaseApiTest(BaseTest):
    def setup_method(self):
        super().setup_method()
        self.specs = Specifications()
        self.user = User(username="admin", password="admin")
        self.auth_spec = self.specs.auth_spec(self.user)

    def create_project(self, project_id):
        payload = {
            "parentProject": {"locator": "_Root"},
            "name": project_id,
            "id": project_id,
            "copyAllAssociatedSettings": True,
        }
        response = requests.post(
            f"{self.auth_spec['base_url']}/projects",
            headers=self.auth_spec["headers"],
            auth=self.auth_spec["auth"],
            json=payload,
        )
        assert response.status_code == 200, f"Project creation failed: {response.text}"
        print(f"Project '{project_id}' created")
        return project_id

    def create_build_type(self, build_type_id, project_id):
        payload = {
            "id": build_type_id,
            "name": "Print Hello World",
            "project": {"id": project_id},
            "steps": {
                "step": [
                    {
                        "name": "Echo Hello World",
                        "type": "simpleRunner",
                        "properties": {
                            "property": [
                                {
                                    "name": "script.content",
                                    "value": "echo 'Hello, world!'",
                                },
                                {"name": "teamcity.step.mode", "value": "default"},
                                {"name": "use.custom.script", "value": "true"},
                            ]
                        },
                    }
                ]
            },
        }
        response = requests.post(
            f"{self.auth_spec['base_url']}/buildTypes",
            headers=self.auth_spec["headers"],
            auth=self.auth_spec["auth"],
            json=payload,
        )
        assert (
            response.status_code == 200
        ), f"Build type creation failed: {response.text}"
        print(f"Build type '{build_type_id}' created")
        return build_type_id

    def queue_build(self, build_type_id):
        payload = {"buildType": {"id": build_type_id}}
        response = requests.post(
            f"{self.auth_spec['base_url']}/buildQueue",
            headers=self.auth_spec["headers"],
            auth=self.auth_spec["auth"],
            json=payload,
        )
        assert response.status_code == 200, f"Build queue failed: {response.text}"
        build_id = response.json()["id"]
        print(f"Build queued with ID: {build_id}")
        return build_id

    def wait_for_build(self, build_id, timeout=60):
        for attempt in range(timeout):
            response = requests.get(
                f"{self.auth_spec['base_url']}/builds/id:{build_id}",
                headers=self.auth_spec["headers"],
                auth=self.auth_spec["auth"],
            )
            if response.status_code == 200:
                build_data = response.json()
                state = build_data.get("state")
                status = build_data.get("status")
                print(f"Attempt {attempt + 1}: State={state}, Status={status}")
                if state == "finished":
                    return status
            time.sleep(1)
        raise TimeoutError(f"Build {build_id} did not finish in {timeout} seconds")
