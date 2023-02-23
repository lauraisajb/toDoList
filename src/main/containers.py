from dependency_injector import containers, providers

from src.main.config import get_db
from src.main.todo_containers import TodoContainer


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src.adapters.app.routes"])
    db_connection = get_db()

    todo_package = providers.Container(TodoContainer, db_conn=db_connection)
