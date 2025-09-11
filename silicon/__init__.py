import os
from pathlib import Path
import secrets
import sys
import tempfile

from flask import Flask


def create_app(testing=False):
    """
    Create the application object, sprinkle in some configuration,
    add our commands, add views, and return the app.

    Flask has a system for putting config files into the instance path but we
    are opting to use environment variables instead, to avoid having to manage
    configuration in multiple places.

    `app.instance_path` is the directory where the database, secret key, export
    directory, and other user data are stored.

    Flask requires a secret key for session handling. If one was provided in
    the environment, we use that. Otherwise, we try to read one from a file
    in the instance path. If that fails, we generate a new key and write it out
    to disk.
    """

    if testing:
        instance_path = tempfile.mkdtemp()
        app = Flask(__name__, instance_path=instance_path)
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "test"
    else:
        app = Flask(__name__)
        os.makedirs(app.instance_path, exist_ok=True)
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', None)

    if app.debug:
        print(sys.version)
        print(f"Instance path: {app.instance_path}")

    app.config['DATABASE'] = os.path.join(app.instance_path, 'silicon.sqlite')

    if app.config['SECRET_KEY'] is None:
        # try to read the secret key
        secret_key_path = Path(app.instance_path) / 'secret.key'
        try:
            app.config['SECRET_KEY'] = secret_key_path.read_bytes()
        except FileNotFoundError:
            # generate and save a new one
            app.config['SECRET_KEY'] = secrets.token_bytes(16)
            os.umask(0)
            secret_key_fd = os.open(
                secret_key_path, os.O_CREAT | os.O_WRONLY, 0o600)
            with open(secret_key_fd, 'wb') as f:
                f.write(app.config['SECRET_KEY'])

    app.config['SILICON_EDITOR'] = os.getenv('SILICON_EDITOR', 'codemirror')

    from . import commands
    commands.init_app(app)

    from . import views
    app.register_blueprint(views.bp)

    return app
