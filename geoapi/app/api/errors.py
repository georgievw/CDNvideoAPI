from flask import jsonify, make_response
from . import api

@api.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@api.app_errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@api.app_errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

@api.app_errorhandler(415)
def unsupported_media_type(error):
    return make_response(jsonify({'error': 'Unsupported Media Type'}), 415)

@api.app_errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)