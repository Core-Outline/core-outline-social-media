from flask import Blueprint, request, jsonify
from app_container.models.data_source import DataSource

data_source_controller = Blueprint('data_source', __name__)
dataSource = DataSource()


@data_source_controller.route('/', methods=['GET'])
def fetch_data_sources():
    params = dict(request.args)
    obj = dataSource.fetch(params)
    obj = [{**item, "_id": str(item['_id'])} for item in obj]
    return jsonify(obj)


@data_source_controller.route('/create-data-source', methods=['POST'])
def create_data_source():
    req = request.get_json()
    req['type'] = 'csv'
    return jsonify(str(dataSource.create(req)))


@data_source_controller.route('/get-data-source', methods=['GET'])
def get_data_source():
    params = dict(request.args)
    obj = dataSource.get(params)
    obj['_id'] = str(obj['_id'])
    return jsonify(obj)
