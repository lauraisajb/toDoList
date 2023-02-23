"""tests the todo api routes src.adapters.app.routes.todo_api.py"""

import json


def test_todo_list_200(test_app, test_database):
    """TodoList.GET"""

    client = test_app.test_client()
    resp = client.get("/api/v1/todo")

    assert resp.status_code == 200
    assert resp.content_type == "application/json"

def test_todo_complete_list_200(test_app, test_database):
    """TodoList.GET"""

    client = test_app.test_client()
    resp = client.get("/api/v1/todo/completed")

    assert resp.status_code == 200
    assert resp.content_type == "application/json"


def test_todo_list_201(test_app, test_database):
    """TodoList.POST"""

    client = test_app.test_client()
    resp = client.post(
        "/api/v1/todo",
        content_type="application/json",
        data=json.dumps({
            "title": "read book",
            "description": "I need to read a book"
        })
    )

    assert resp.status_code == 201
    assert resp.content_type == "application/json"


def test_todo_by_id_get_200(test_app, test_database, add_todo):
    """TodoDetail.GET - 200"""

    _todo = add_todo("Walk with chiqui", "Walk with chiqui around 25 min")
    client = test_app.test_client()
    resp = client.get("/api/v1/todo/1")

    assert resp.status_code == 200
    assert resp.content_type == "application/json"


def test_todo_get_404(test_app, test_database):
    """TodoDetail.GET - 404"""

    client = test_app.test_client()
    resp = client.get("/api/v1/todos/1234")
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404
    assert "Not found" in data["error"]


def test_todo_put_200(test_app, test_database, add_todo):
    """TodoDetail.PUT - 200"""

    _todo = add_todo("test_todo_put")
    client = test_app.test_client()
    resp = client.put(
        f"/api/v1/todo/1",
        content_type="application/json",
        data=json.dumps({
            "title": "test_todo_put_200",
            "description": "test_todo_put_200",
            "completed": True
        })
    )

    assert resp.status_code == 200
    assert resp.content_type == "application/json"


def test_todo_put_404(test_app, test_database):
    """TodoDetail.PUT - 404"""

    client = test_app.test_client()
    resp = client.put(
        "/api/v1/todo/342343",
        content_type="application/json",
        data=json.dumps({
            "title": "does not exist",
            "description": "does not exist",
            "completed": True
        })
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404
    assert "Not found" in data["error"]


def test_todo_delete_204(test_app, test_database, add_todo):
    """TodoDetail.DELETE - 204"""

    _todo = add_todo("test_todo_delete")
    client = test_app.test_client()
    resp = client.delete(f"/api/v1/todo/1")

    assert resp.status_code == 204
    assert resp.content_type == "application/json"


def test_todo_delete_404(test_app, test_database):
    """TodoDetail.DELETE - 404"""

    client = test_app.test_client()
    resp = client.delete("/api/v1/todo/343243")
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404
    assert "Not found" in data["error"]