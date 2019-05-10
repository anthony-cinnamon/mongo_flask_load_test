from functools import wraps

import pymongo
from flask import current_app, g, jsonify
from pymongo.errors import ConnectionFailure


def get_db():
    if 'db' not in g:
        mongodb_endpoint = current_app.config['MONGODB_ENDPOINT']
        g.db = pymongo.MongoClient(mongodb_endpoint)
    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        retry_count = 2
        while (retry_count > 0):
            try:
                result = f(*args, **kwargs)
                if hasattr(result, 'status_code'):
                    if result.status_code == 200:
                        break
                else:
                    break
            except ConnectionFailure:
                current_app.logger.error("Connection error")
                response = jsonify({'error': 'connection error'})
                response.status_code = 500
                result = response
            finally:
                retry_count = retry_count - 1
        return result

    return wrapper
