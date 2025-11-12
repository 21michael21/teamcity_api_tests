import requests
import pytest

class ValidationResponseSpecifications:
    """Класс для переиспользуемых спецификаций проверки HTTP-ответов."""
    
    @staticmethod
    def validate_success(response: requests.Response):
        """Проверяет успешный ответ (status_code == 200)."""
        pytest.assume(response.status_code == 200, f"Expected status 200, got {response.status_code}: {response.text}")
    
    @staticmethod
    def validate_body(response: requests.Response, expected_id: str, expected_field: str = "id"):
        """Проверяет тело ответа на наличие ожидаемого ID."""
        data = response.json()
        pytest.assume(expected_field in data, f"Response does not contain '{expected_field}' key")
        pytest.assume(data[expected_field] == expected_id, f"Expected {expected_field} {expected_id}, got {data[expected_field]}")

    @staticmethod
    def validate_error(response: requests.Response, expected_status: int, expected_error_message: str = None):
        """Проверяет ошибочный ответ (например, 400, 403) и текст ошибки в теле, если указан."""
        pytest.assume(response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}: {response.text}")
        if expected_error_message:
            data = response.json()
            error_field = "message" if "message" in data else "error"
            pytest.assume(error_field in data, f"Response does not contain '{error_field}' key")
            pytest.assume(expected_error_message in data[error_field], f"Expected error message '{expected_error_message}', got '{data[error_field]}'")