from typing import Any


class Message:
    def __init__(self, message: str, data: Any) -> None:
        self.message = message
        self.data = data

    def get_msg(self):
        return self.__dict__


class SuccessMessage(Message):
    def __init__(
        self, subject: str, name: str, operation: str, data: Any
    ) -> None:
        super().__init__(
            f"{subject.capitalize()} '{name}' {operation}: success", data
        )