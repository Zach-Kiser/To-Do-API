import pytest
from flask import Flask
from flask_restful import Api
from main import Task, TaskList
import json

class Test_API():
    @pytest.fixture(autouse=True)
    def set_up_tests(self):
        self.app = Flask("TaskAPI")
        self.api = Api(self.app)
        self.api.add_resource(Task, '/tasks/<task_id>')
        self.api.add_resource(TaskList, '/tasks')
        self.client = self.app.test_client()

    def test_get_all_tasks_empty_list(self):
        response = self.client.get('/tasks')
        data = response.get_json()
        assert response.status_code == 200
        assert data == {}

    def test_get_all_tasks(self):
        self.client.post('/tasks', json={
               'name': 'Calculus exam',
               'description': 'Study for exam on Thursday',
               'status': 'Incomplete'})
        self.client.post('/tasks', json={
               'name': 'Groceries',
               'description': 'Go grocery shopping',
               'status': 'Incomplete'}) 
        response = self.client.get('/tasks')
        data = response.get_json()
        assert response.status_code == 200
        assert len(data) > 1
    
    def test_get_task(self):
        response = self.client.get('/tasks/task1')
        data = response.get_json()
        assert response.status_code == 200
        assert data["name"] == 'Calculus exam'

    def test_get_invalid_task(self):
        response = self.client.get('/tasks/invalid')
        data = response.get_json()
        assert response.status_code == 404

    def test_create_new_task(self):
        response = self.client.post('/tasks', json={
               'name': 'Term paper',
               'description': 'Finish English essay by Monday',
               'status': 'Incomplete'})
        data = response.get_json()
        assert response.status_code == 201
        assert data["name"] == "Term paper"

    def test_create_invalid_task(self):
        response = self.client.post('/tasks', json={
               'name': 'Missing description',
               'status': 'Incomplete'})
        assert response.status_code == 400
    
    def test_update_task(self):
        response = self.client.put('/tasks/task1', json={
            'name': 'Term paper',
            'description': 'Finish English essay by Monday',
            'status': 'Complete'})
        data = response.get_json()
        assert response.status_code == 200
        assert data['task1']['name'] == 'Term paper'
        assert data['task1']['description'] == 'Finish English essay by Monday'
        assert data['task1']['status'] == 'Complete'

    def test_update_task_invalid(self):
        response = self.client.put('/tasks/task100', json={
            'name': 'Term paper',
            'description': 'Finish English essay by Monday',
            'status': 'Complete'})
        data = response.get_json()
        assert response.status_code == 404
    
    def test_update_missing_fields(self):
        response = self.client.put('/tasks/task2', json={'name': 'Grocery shopping'})
        data = response.get_json()
        assert response.status_code == 400

    def test_delete_task(self):
        response = self.client.delete('/tasks/task1')
        data = response.get_json()
        assert data == ""

    def test_delete_task_invalid(self):
        response = self.client.delete('/tasks/task500')
        data = response.get_json()
        assert response.status_code == 404

    
