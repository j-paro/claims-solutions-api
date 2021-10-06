from typing import Any


class SuccessMessage:
    def __init__(
        self, subject: str, name: str, operation: str, data: Any
    ) -> None:
        self.message = f"{subject.capitalize()} '{name}' {operation}: success"
        self.data = data