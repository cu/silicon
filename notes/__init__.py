import os
import sys

from flask import Flask


def create_app(test_config=None):
    """
    Create the application object, sprinkle in some configuration,
    add our commands, add views, and return the app.

    Note that Flask has a system for putting config files into the instance
    folder but we are opting to use environment variables instead, to avoid
    having to managing configuration in different places.

    `instance_path` is where the database is stored.
    """
    instance_path = os.getenv('INSTANCE_PATH', None)

    if instance_path is None:
        app = Flask(__name__)
    else:
        app = Flask(__name__, instance_path=instance_path)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    if app.config['ENV'] == 'development':
        print(sys.version)
        print(f"Instance path: {app.instance_path}")

    from . import views
    app.register_blueprint(views.bp)

    return app
