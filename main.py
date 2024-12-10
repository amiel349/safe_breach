from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from app.services.task_factory import TaskFactory
from app.services.task_manager import TaskManager
from logger import logger

app = Flask(__name__)
task_manager = TaskManager()


@app.route('/run_task/<task_type>', methods=['POST'])
def run_task(task_type):
    data = request.json

    task = TaskFactory.create_task(task_type, **data)
    future = task_manager.run_task(task)

    try:
        result = future.result(timeout=10)
        logger.info(f"Task {task_type} executed successfully with result: {result}")
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        logger.error(f"Unexpected error in task execution: {str(e)}")
        return jsonify({"status": "failure", "error": str(e)})


@app.route('/run_task/http_server/start', methods=['POST'])
def start_http_server():
    try:
        data = request.json
        task = TaskFactory.create_task("http_server", action="start", **data)
        uuid = task.start_server()
        return jsonify({"status": "success", "uuid": uuid})
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)}), 400


@app.route('/run_task/http_server/stop', methods=['POST'])
def stop_http_server():
    try:
        data = request.json
        uuid = data.get("uuid")
        if not uuid:
            return jsonify({"status": "failure", "error": "Missing UUID"}), 400

        task = TaskFactory.create_task("http_server", action="stop", **{"port": 8080, "uri": "/example", "data": "Dummy data"})
        ips = task.stop_server(uuid)
        if ips is not None:
            return jsonify({"status": "success", "accessed_ips": ips})
        else:
            return jsonify({"status": "failure", "error": "Server not found"}), 404
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)}), 500


# Swagger UI setup
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"  # This JSON file will define the API schema
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={"app_name": "Task API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == "__main__":
    app.run(debug=True)
