from flask import Blueprint, jsonify, request
from todo.models import db
from todo.models.todo import Todo
from datetime import datetime, timedelta
 
api = Blueprint('api', __name__, url_prefix='/api/v1') 

TEST_ITEM = {
    "id": 1,
    "title": "Watch CSSE6400 Lecture",
    "description": "Watch the CSSE6400 lecture on ECHO360 for week 1",
    "completed": True,
    "deadline_at": "2023-02-27T00:00:00",
    "created_at": "2023-02-20T00:00:00",
    "updated_at": "2023-02-20T00:00:00"
}
 
@api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})

# Implement a get todo with filtering like completed state like api call /api/v1/todos?completed=true
@api.route('/todos', methods=['GET'])
def get_todos():
    completed = request.args.get('completed')
    if completed is not None:
        completed = completed.lower() == 'true'
        todos = Todo.query.filter_by(completed=completed)
    else:
        todos = Todo.query.all()

    # Handle deadline window filtering
    window = request.args.get('window')
    if window is not None:
        try:
            window = int(window)
            now = datetime.now()
            deadline = now + timedelta(days=window)
            todos = Todo.query.filter(
                Todo.deadline_at.isnot(None),
                Todo.deadline_at <= deadline)
        except ValueError:
            return jsonify({"error": "Invalid window value"}), 400
        
    result = []
    for todo in todos:
        result.append(todo.to_dict())
    return jsonify(result)

# Implement a get todo with filtering like deadline_at like api call /api/v1/todos?deadline_at=2023-02-27T00:00:00


@api.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not Found"}), 404
    return jsonify(todo.to_dict())
    

@api.route('/todos', methods=['POST'])
def create_todo():
    # Check if no extra field exists in the request
    for key in request.json.keys():
        if key not in ['title', 'description', 'completed', 'deadline_at']:
            return jsonify({"error": f"Invalid field {key} in request"}), 400
    # Check if title exists in the request
    if 'title' not in request.json:
        return jsonify({"error": "Title is required"}), 400

    todo = Todo(
        title = request.json.get('title'),
        description = request.json.get('description'),
        completed = request.json.get('completed', False),
    )
    if 'deadline_at' in request.json:
        todo.deadline_at = datetime.fromisoformat(request.json['deadline_at'])
    
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@api.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not Found"}), 404
    # Check if todo's id exists in the request
    if 'id' in request.json and request.json['id'] != todo_id:
        return jsonify({"error": "Id in request does not match id in URL"}), 400
    todo.title = request.json.get('title', todo.title)
    todo.description = request.json.get('description', todo.description)
    todo.completed = request.json.get('completed', todo.completed)
    todo.deadline_at = request.json.get('deadline_at', todo.deadline_at)
    # Check if no extra field exists in the request
    for key in request.json.keys():
        if key not in ['id', 'title', 'description', 'completed', 'deadline_at']:
            return jsonify({"error": f"Invalid field {key} in request"}), 400
    db.session.commit()
    return jsonify(todo.to_dict())

@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({}), 200
    
    db.session.delete(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 200
