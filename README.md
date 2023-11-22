__A To-Do List API project implemented using Python/Flask__

__After cloning the repository, dependencies can be installed by running:__

pip install -r requirements.txt

__To run the API:__

python main.py

__Documentation was created using Swagger, and is viewable by visiting the below URL while the API is running:__

http://127.0.0.1:5000/swagger

__To run unit tests:__

pytest test_api.py

__Example of manually sending requests:__

curl -H "Content-Type: application/json" -X POST -d '{"name":"Do homework","description":"Finish English paper","status":"Incomplete"}' http://localhost:5000/tasks
