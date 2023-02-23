from flask import jsonify, abort, request, Blueprint


TODO_API = Blueprint('todo_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return TODO_API


TODO_REQUESTS = {
    1: {
        'title': u'Read a book',
        'description': u"Today I'm going to read a chapter of my new book",
        'complete': False
    },
    2: {
        'title': u'jogging',
        'description': u'1 hour of jogging',
        'complete': False
    }
}
TASK_NUMBER = 3

@TODO_API.route('/todo', methods=['GET'])
async def get_records():
    """Return all todo tasks
    @return: 200: an array of all known TODO_REQUESTS as a \
    flask/response object with application/json mimetype.
    """
    return jsonify(TODO_REQUESTS)


@TODO_API.route('/todo/<int:_id>', methods=['GET'])
async def get_record_by_id(_id):
    """Get todo task details by it's id
    @param _id: the id
    @return: 200: a TODO_REQUESTS as a flask/response object \
    with application/json mimetype.
    @raise 404: if book request not found
    """
    if _id not in TODO_REQUESTS:
        abort(404)
    return jsonify(TODO_REQUESTS[_id])


@TODO_API.route('/todo', methods=['POST'])
async def create_record():
    """Create a todo task record
    @param description: post : the requesters task description
    @param title: post : the title of the todo task
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('description'):
        abort(400)
    if not data.get('title'):
        abort(400)

    todo_task = {
        'title': data['title'],
        'description': data['description'],
        'complete': False
    }
    global TASK_NUMBER
    TODO_REQUESTS[TASK_NUMBER] = todo_task
    # HTTP 201 Created
    response = (jsonify({"id": TASK_NUMBER}), 201) 
    TASK_NUMBER += 1
    return response


@TODO_API.route('/todo/<int:_id>', methods=['PUT'])
async def edit_record(_id):
    """Edit a book request record
    @param description: post : the requesters task description
    @param title: post : the title of the todo task
    @return: 200: a booke_request as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if _id not in TODO_REQUESTS:
        abort(404)

    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('description'):
        abort(400)
    if not data.get('title'):
        abort(400)
    if not data.get('complete'):
        abort(400)

    todo_task = {
        'title': data['title'],
        'description': data['description'],
        'complete': data['complete']
    }

    TODO_REQUESTS[_id] = todo_task
    return jsonify(TODO_REQUESTS[_id]), 200


@TODO_API.route('/todo/<int:_id>', methods=['DELETE'])
async def delete_record(_id):
    """Delete a todo task
    @param id: the todo task id
    @return: 204: an empty payload.
    @raise 404: if book request not found
    """
    if _id not in TODO_REQUESTS:
        abort(404)

    del TODO_REQUESTS[_id]

    return '', 204