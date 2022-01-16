import os
import sys

from flask import Flask

class AppConfigurationError(Exception):
    pass

def create_app(test_config=None):
    """
    Create the application object, sprinkle in some configuration,
    add our commands, add views, and return the app.

    Note that Flask has a system for putting config files into the instance
    path but we are opting to use environment variables instead, to avoid
    having to manage configuration in different places.

    `instance_path` is where the database is stored.
    """
    instance_path = os.getenv('INSTANCE_PATH', None)

    if instance_path is not None:
        app = Flask(__name__, instance_path=instance_path)
    else:
        # Flask defaults to setting `instance_path` to a directory named
        # `instance` next to the package.
        app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', None)

    if test_config:
        app.config.update(test_config)
    else:
        # ensure the instance folder exists
        os.makedirs(app.instance_path, exist_ok=True)

        if app.config['ENV'] == 'development':
            print(sys.version)
            print(f"Instance path: {app.instance_path}")

        app.config['DATABASE'] = os.path.join(app.instance_path, 'notes.sqlite')

    if app.config['SECRET_KEY'] is None:
        raise AppConfigurationError('SECRET_KEY must be defined, see README.md')

    from . import commands
    commands.init_app(app)

    from . import views
    app.register_blueprint(views.bp)

    return app
