from flask import Blueprint, request, jsonify
from app_container.models.query import Query

query_controller = Blueprint('query', __name__)
query = Query()


@query_controller.route('/', methods=['GET'])
def fetch_queries():
    params = dict(request.args)
    return jsonify(query.fetch(params))


@query_controller.route('/create-query', methods=['POST'])
def create_query():
    
    req = request.get_json()
    return jsonify(query.create(req))


@query_controller.route('/get-query', methods=['GET'])
def get_query():
    params = dict(request.args)
    return jsonify(query.get(params))


@query_controller.route('/get-query/<account_id>', methods=['GET'])
def get_account_query(account_id):
    params = dict(request.args)
    params['account_id'] = account_id
    return jsonify(query.fetch_account_queries(params))

# @query_controller.route('/insta-user-engagement', methods=['GET'])
# def instagram_user_engagement():
#     params = dict(request.args)
#     print(params)
#     return jsonify(query.instaUserEngagement(params))
