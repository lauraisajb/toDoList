from dataclasses import dataclass


@dataclass
class Todo:
    title: str
    description: str
    completed: bool


def todo_factory(title: str, description: str, completed: bool = False) -> Todo:
    # data validation should happen here
    return Todo(title=title, description=description, completed=completed)
