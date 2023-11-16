from flask import Flask
from flask.json import jsonify
from flask_restful import Resource, Api, reqparse, abort
from flask_swagger_ui import get_swaggerui_blueprint
import json


app = Flask("TaskAPI")
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('description', required=True)
parser.add_argument('status', required=True)


tasks = {}

class Task(Resource):
    def get(self, task_id):
        if task_id == None:
            return tasks
        if task_id not in tasks:
            abort(404, message=f"Task {task_id} not found")
        return tasks[task_id], 200 # successful

    def put(self, task_id):
        if task_id not in tasks:
            abort(404, message=f"Task {task_id} not found")
        args = parser.parse_args()
        #Only update specified fields
        tasks[task_id]['name'] = args['name']
        tasks[task_id]['description'] = args['description']
        tasks[task_id]['status'] = args['status']
        return {task_id: tasks[task_id]}, 200
    
    def delete(self, task_id):
        if task_id not in tasks:
            abort(404, message=f"Task {task_id} not found")
        del tasks[task_id]
        return ""

class TaskList(Resource):
    def get(self):
        return tasks, 200
    
    def post(self):
        args = parser.parse_args()
        if (len(tasks) == 0):
            new_id = 1
        else:
            # assign new identifier linearly
            new_id = max(int(task.strip('task')) for task in tasks) + 1
        new_task = {
            'name': args['name'],
            'description': args['description'],
            'status': args['status']
            }
        #make id more meaningful
        task_id = f"task{new_id}"
        tasks[task_id] = new_task
        return tasks[task_id], 201 # successfully created

api.add_resource(Task, '/tasks/<task_id>')
api.add_resource(TaskList, '/tasks')


SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:5000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "To-Do List API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run()