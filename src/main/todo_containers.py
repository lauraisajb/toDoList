from dependency_injector import containers, providers

from src.adapters.db.todo_repository import TodoRepository
from src.domain.ports.todo_service import TodoService


class TodoContainer(containers.DeclarativeContainer):
    db_conn = providers.Dependency()

    todo_repository = providers.Singleton(TodoRepository, db_conn=db_conn)

    todo_service = providers.Factory(TodoService, todo_repo=todo_repository)
