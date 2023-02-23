from typing import Any, Optional

from ..model.todo import Todo, todo_factory
from . import CreateTodoInputDto, DeleteTodoInputDto, UpdateTodoInputDto
from .repository import RepositoryInterface


class TodoDBOperationError(Exception):
    ...


class TodoService:
    def __init__(self, todo_repo: RepositoryInterface) -> None:
        self.todo_repo = todo_repo

    def create(self, todo: CreateTodoInputDto) -> Todo:
        todo = todo_factory(title=todo.title, description=todo.description)
        data = (todo.title, todo.description, todo.completed)
        query = "INSERT INTO todo (title, description, completed) VALUES (?, ?, ?)"
        try:
            self.todo_repo.execute(query, data, commit=True)
        except Exception as err:
            raise TodoDBOperationError(err) from err
        return todo

    def update(self, todo: UpdateTodoInputDto):
        data = (todo.title, todo.description, todo.completed, todo.id)
        query = (
            """UPDATE todo SET title = ?, description = ?, completed = ? WHERE id = ?"""
        )
        if self.get_todo_by_id(todo.id) is None:
            return None
        try:
            return self.todo_repo.execute(query, data, commit=True)
        except Exception as err:
            raise TodoDBOperationError(err) from err

    def delete(self, todo: DeleteTodoInputDto):
        data = (todo.id,)
        query = "DELETE FROM todo WHERE id = ?"
        if self.get_todo_by_id(todo.id) is None:
            return None
        try:
            self.todo_repo.execute(query, data, commit=True)
            return 204
        except Exception as err:
            raise TodoDBOperationError(err) from err

    def get_todo_by_id(self, id_: int) -> Optional[tuple[Any, ...]]:
        data = (id_,)
        query = "SELECT * FROM todo WHERE id = ?"
        try:
            return self.todo_repo.execute(query, data).fetchone()
        except Exception as err:
            raise TodoDBOperationError() from err

    def get_all_todo(self) -> Optional[list[Any]]:
        data = ()
        query = """SELECT *
         FROM todo t
         WHERE t.completed = false
         """
        try:
            rows = self.todo_repo.execute(query, data).fetchall()
            return [dict(row) for row in rows]
        except Exception as err:
            raise TodoDBOperationError() from err

    def get_all_todo_completed(self) -> Optional[list[Any]]:
        data = ()
        query = """SELECT *
         FROM todo t
         WHERE t.completed = true
         """
        try:
            rows = self.todo_repo.execute(query, data).fetchall()
            return [dict(row) for row in rows]
        except Exception as err:
            raise TodoDBOperationError() from err
