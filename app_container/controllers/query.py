from flask import Blueprint, request, jsonify
from app_container.models.query import Query

query_controller = Blueprint('query', __name__)
query = Query()


@query_controller.route('/query', methods=['GET'])
def fetch_queries():
    params = request.args()
    return jsonify(query.get(params))


@query_controller.route('/create-query', methods=['POST'])
def create_query():
    req = request.get_json()
    return jsonify(query.create(req))


@query_controller.route('/get-query', methods=['GET'])
def get_query():
    params = dict(request.args)
    return jsonify(query.get(params))


@query_controller.route('/execute-query', methods=['GET'])
def execute_query():
    req = request.get_json()
    return jsonify(query.execute(req))
