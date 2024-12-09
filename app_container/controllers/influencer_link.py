from flask import Blueprint, request, jsonify
from app_container.models.query import Query

influencer_link_controller = Blueprint('query', __name__)
query = Query()


@influencer_link_controller.route('/', methods=['GET'])
def fetch_influencer_links():
    params = dict(request.args)
    return jsonify(query.fetch(params))


@influencer_link_controller.route('/create-influencer-link', methods=['POST'])
def create_query(): 
    req = request.get_json()
    return jsonify(query.create(req))


@influencer_link_controller.route('/get-influencer-link', methods=['GET'])
def get_query():
    params = dict(request.args)
    return jsonify(query.get(params))


# @query_controller.route('/insta-user-engagement', methods=['GET'])
# def instagram_user_engagement():
#     params = dict(request.args)
#     print(params)
#     return jsonify(query.instaUserEngagement(params))
