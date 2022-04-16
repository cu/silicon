import os
from pathlib import Path
import secrets
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

    `app.instance_path` is the directory where the database and secret key are
    stored.

    Flask requires a secret key for session handling. If one was provided in
    the environment, we use that. Otherwise, we try to read one from a file
    in the instance path. If that fails, we generate a new key and write it out
    to disk.
    """
    instance_path = os.getenv('INSTANCE_PATH', None)

    if instance_path is not None:
        app = Flask(__name__, instance_path=instance_path)
    else:
        # Flask defaults to setting `instance_path` to a directory named
        # `instance` next to the package.
        app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        # ensure the instance folder exists
        os.makedirs(app.instance_path, exist_ok=True)

        if app.config['ENV'] == 'development':
            print(sys.version)
            print(f"Instance path: {app.instance_path}")

        app.config['DATABASE'] = os.path.join(app.instance_path, 'silicon.sqlite')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', None)
    if app.config['SECRET_KEY'] is None:
        # try to read the secret key
        try:
            with open(Path(app.instance_path) / 'secret.key', 'rb') as f:
                app.config['SECRET_KEY'] = f.read()
        except:
            # generate and save a new one
            app.config['SECRET_KEY'] = secrets.token_bytes(16)
            os.umask(0)
            with open(os.open(Path(app.instance_path) / 'secret.key', os.O_CREAT | os.O_WRONLY, 0o600), 'wb') as f:
                f.write(app.config['SECRET_KEY'])

    app.config['SILICON_EDITOR'] = os.getenv('SILICON_EDITOR', 'codemirror')

    from . import commands
    commands.init_app(app)

    from . import views
    app.register_blueprint(views.bp)

    return app
