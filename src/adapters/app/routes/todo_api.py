import logging
from dependency_injector.wiring import Provide, inject
from flask import Blueprint, abort, jsonify, request

from src.domain.ports import (create_todo_factory, delete_todo_factory,
                              update_todo_factory)
from src.domain.ports.todo_service import TodoDBOperationError, TodoService
from src.main.containers import Container


TODO_API = Blueprint("todo_api", __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return TODO_API


@TODO_API.route("/api/v1/todo", methods=["GET"])
@inject
async def get_todos(
    todos_service: TodoService = Provide[Container.todo_package.todo_service],
):
    """Return all todo tasks
    @return: 200: an array of all known TODO_REQUESTS as a \
    flask/response object with application/json mimetype.
    """
    todos = todos_service.get_all_todo()
    return jsonify(todos)


@TODO_API.route("/api/v1/todo/completed", methods=["GET"])
@inject
async def get_completed_todos(
    todos_service: TodoService = Provide[Container.todo_package.todo_service],
):
    """Return all todo tasks
    @return: 200: an array of all known TODO_REQUESTS as a \
    flask/response object with application/json mimetype.
    """
    todos = todos_service.get_all_todo_completed()
    return jsonify(todos)


@TODO_API.route("/api/v1/todo/<int:_id>", methods=["GET"])
@inject
async def get_record_by_id(
    _id, todo_service: TodoService = Provide[Container.todo_package.todo_service]
):
    """Get todo task details by it's id
    @param _id: the id
    @return: 200: a TODO_REQUESTS as a flask/response object \
    with application/json mimetype.
    @raise 404: if todo request not found
    """
    todo = todo_service.get_todo_by_id(_id)
    if todo is None:
        abort(404)

    return jsonify(dict(todo))


@TODO_API.route("/api/v1/todo", methods=["POST"])
@inject
async def create_record(
    todo_service: TodoService = Provide[Container.todo_package.todo_service],
):
    """Create a todo task record
    @param description: post : the requesters task description
    @param title: post : the title of the todo task
    @return: 201: a new task as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """

    if not request.get_json():
        abort(400)

    data = request.get_json(force=True)

    if not data.get("description"):
        abort(400)
    if not data.get("title"):
        abort(400)

    todo = create_todo_factory(title=data["title"], description=data["description"])
    try:
        todo_service.create(todo)
    except TodoDBOperationError as err:
        logging.error(f"Something went wrong with database operation {err}")

    return jsonify(todo.to_dict()), 201


@TODO_API.route("/api/v1/todo/<int:_id>", methods=["PUT"])
@inject
async def edit_record(
    _id, todo_service: TodoService = Provide[Container.todo_package.todo_service]
):
    """
    Edit a todo task record
    @param description: post : the requesters todo description
    @param title: post : the title of the todo task
    @return: 200: a todo_request as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """

    if not request.get_json():
        abort(400)

    data = request.get_json(force=True)

    if _id is None:
        abort(400)

    if not data.get("description"):
        abort(400)

    if not data.get("title"):
        abort(400)

    if not data.get("completed"):
        abort(400)

    todo = update_todo_factory(
        id=_id,
        title=data["title"],
        description=data["description"],
        completed=data["completed"],
    )

    try:
        status = todo_service.update(todo)
    except TodoDBOperationError as err:
        logging.error(f"Something went wrong with database operation {err}")
    if status is None:
        abort(404)

    return jsonify(todo.to_dict())


@TODO_API.route("/api/v1/todo/<int:_id>", methods=["DELETE"])
@inject
async def delete_record(
    _id, todo_service: TodoService = Provide[Container.todo_package.todo_service]
):
    """
    Delete a todo task
    @param id: the todo task id
    @return: 204: an empty payload.
    @raise 404: if task request not found
    """
    todo = delete_todo_factory(id=_id)
    try:
        status = todo_service.delete(todo)
    except TodoDBOperationError as err:
        logging.error(f"Something went wrong with database operation {err}")

    if status is None:
        abort(404)

    return jsonify({}), status
