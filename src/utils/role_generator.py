import string
import random
from pydantic import BaseModel
from typing import Optional, Type


def generate_random_string(length=8):
    """Генерирует случайную строку из букв."""
    letters = string.ascii_letters
    return "".join(random.choice(letters) for i in range(length))


def generate_instance(model_class: Type[BaseModel]):
    """Генерирует экземпляр модели на основе её полей."""
    field_values = {}
    for field_name, field_type in model_class.__annotations__.items():
        if "id" in field_name:
            field_values[field_name] = generate_random_string()
        elif field_name == "name":
            field_values[field_name] = "default_name"
        elif issubclass(field_type, BaseModel):
            field_values[field_name] = generate_instance(field_type)
        else:
            field_values[field_name] = None
    return model_class(**field_values)


class RoleGenerator:
    """Класс для генерации ролей и связанных данных."""

    @staticmethod
    def generate_project_admin_role(
        project_id: str, role_id: str = "PROJECT_ADMIN"
    ) -> dict:
        """Генерирует payload для роли PROJECT_ADMIN в указанном проекте."""
        return {"role": [{"roleId": role_id, "scope": f"p:{project_id}"}]}
