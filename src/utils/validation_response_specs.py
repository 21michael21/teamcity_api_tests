import pytest
import requests


class ValidationResponseSpecifications:
    """Класс для переиспользуемых спецификаций проверки HTTP-ответов."""

    @staticmethod
    def validate_success(response: requests.Response):
        """Проверяет успешный ответ (status_code == 200)."""
        pytest.assume(
            response.status_code == 200,
            f"Expected status 200, got {response.status_code}: {response.text}",
        )

    @staticmethod
    def validate_body(
        response: requests.Response, expected_id: str, expected_field: str = "id"
    ):
        """Проверяет тело ответа на наличие ожидаемого ID."""
        data = response.json()
        pytest.assume(
            expected_field in data, f"Response does not contain '{expected_field}' key"
        )
        pytest.assume(
            data[expected_field] == expected_id,
            f"Expected {expected_field} {expected_id}, got {data[expected_field]}",
        )
