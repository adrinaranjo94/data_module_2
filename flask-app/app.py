from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Lista de tareas (En memoria)
todo_list = []

# Ruta principal que muestra el To-Do List (Front-end)
@app.route('/')
def index():
    return render_template('index.html', tasks=todo_list)

# API: Endpoint para consultar la lista de tareas
@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todo_list), 200

# API: Endpoint para agregar una nueva tarea
@app.route('/api/add', methods=['POST'])
def add_task():
    task = request.json.get('task')  # Recibe el JSON con la clave 'task'
    if task:
        todo_list.append(task)
        return jsonify({'message': 'Task added successfully!'}), 201
    return jsonify({'message': 'Task is required!'}), 400

# API: Endpoint para eliminar una tarea por su índice
@app.route('/api/delete/<int:task_index>', methods=['DELETE'])
def delete_task(task_index):
    if 0 <= task_index < len(todo_list):
        todo_list.pop(task_index)
        return jsonify({'message': 'Task deleted successfully!'}), 200
    return jsonify({'message': 'Task not found!'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
