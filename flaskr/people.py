from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request

from . import db

bp = Blueprint('people', __name__)


@bp.route('/people', methods=['DELETE'])
def clean():
    client = db.get_db()
    mdb = client.test_db
    mdb.people.remove({})

    return jsonify({})


@bp.route('/people/count', methods=['GET'])
def count_people():
    client = db.get_db()
    mdb = client.test_db

    result = {'count': mdb.people.find({}).count_documents({})}
    return jsonify(result)


@bp.route('/people', methods=['GET'])
@db.handle_errors
def people():
    client = db.get_db()
    mdb = client.test_db
    people = mdb.people
    result = people.find({})
    result = list(map(_replace_id, result))

    return jsonify(result)


@bp.route('/person', methods=['POST'])
@db.handle_errors
def add_person():
    client = db.get_db()
    mdb = client.test_db
    people = mdb.people
    people_id = str(people.insert_one(request.json).inserted_id)

    result = {
        '_id': people_id
    }

    return jsonify(result)


@bp.route('/person/<person_id>', methods=['GET'])
@db.handle_errors
def get_person(person_id):
    client = db.get_db()
    mdb = client.test_db
    people = mdb.people
    person = people.find_one({'_id': ObjectId(person_id)})
    person['_id'] = str(person['_id'])

    return jsonify(person)


@bp.route('/person/<person_id>/increase_age', methods=['PATCH'])
@db.handle_errors
def increase_age_person(person_id):
    client = db.get_db()
    mdb = client.test_db
    people = mdb.people
    person = people.find_one({'_id': ObjectId(person_id)})

    if person is not None:
        new_age = {
            "$set": {
                'age': person['age'] + 1
            }
        }
        people.update_one({'_id': ObjectId(person_id)}, new_age)

        person = people.find_one({'_id': ObjectId(person_id)})
        person['_id'] = str(person['_id'])

        return jsonify(person)
    else:
        response = jsonify({})
        response.status_code = 404
        return response


def _replace_id(person):
    person['_id'] = str(person['_id'])
    return person
