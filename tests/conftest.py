import pytest

from src.adapters.app.application import create_app
from src.main.config import init_db, get_db
from src.domain.model.todo import todo_factory


@pytest.fixture(scope="module")
def test_app():
    """fixture for testing the application"""

    app = create_app()
    with app.app_context():
        yield app # testing happens here


@pytest.fixture(scope="module")
def test_database():
    """fixture for cleaning and leveraging test db"""

    db = get_db()
    init_db()
    yield db() # testing happens here
    


@pytest.fixture(scope="module")
def add_todo():
    def _add_todo(title, description=""):
        todo = todo_factory(title=title, description=description)
        data = (todo.title, todo.description, todo.completed)
        query = "INSERT INTO todo (title, description, completed) VALUES (?, ?, ?)"
        db = get_db()
        db = db()
        db.execute(query, data)
        db.commit()
        return todo
    
    return _add_todo