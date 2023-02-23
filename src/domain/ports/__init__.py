from dataclasses import asdict, dataclass


@dataclass
class CreateTodoInputDto:
    title: str
    description: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_)


def create_todo_factory(title: str, description: str) -> CreateTodoInputDto:
    return CreateTodoInputDto(title=title, description=description)


@dataclass
class UpdateTodoInputDto:
    id: int
    title: str
    description: str
    completed: bool

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_)


def update_todo_factory(
    id: int, title: str, description: str, completed: bool
) -> UpdateTodoInputDto:
    return UpdateTodoInputDto(
        id=id, title=title, description=description, completed=completed
    )


@dataclass
class DeleteTodoInputDto:
    id: int

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_)


def delete_todo_factory(id: int) -> DeleteTodoInputDto:
    return DeleteTodoInputDto(id=id)
