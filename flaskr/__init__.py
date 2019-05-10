import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_json('/etc/config.json', silent=True)
    app.config.from_json('config.json', silent=True)
    # app.config.from_mapping(
    #     MONGODB_ENDPOINT='mongodb://127.0.0.1:27017'
    # )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import people
    app.register_blueprint(people.bp)
    app.debug = True

    return app


application = create_app()
