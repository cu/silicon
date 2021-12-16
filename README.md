# Quickstart

This project is configured and deployed much like any other Flask project.
For details, see the [Flask configuration handling Docs].

[Flask configuration handling docs]: https://flask.palletsprojects.com/en/1.1.x/config/

## Requirements

This project requires Python 3.7 or greater and `npm` to install the
third-party Javascript and CSS static resources. On a Debian/Ubuntu system,
that means the following packages:

* `python3`
* `python3-pip` (unless installed via other means)
* `python3-dev`
* `python3-venv`
* `npm` (optional, if you already have docker installed)

## For development or local use

Create a virtual env:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install wheel
```

Go to the local repo and install requirements:

```
pip install -r requirements.txt
```

Install third-party Javascript/CSS static packages:

```
(cd notes/static && npm install)
```

Or, if you'd rather just use npm from inside a docker container:

```
docker run -ti --rm -v $PWD/notes/static:/app -w /app node:alpine npm install
```

The `.flaskenv` file sets the `FLASK_APP` environment variable so as long as you
issue the `flask` command from the root of the repo, flask will know which
app to run. If you try to run `flask` from somewhere else, you will need to
set:

```
FLASK_APP=notes
```

Flask is configured via environment variables. There is a file called
`.flaskenv` which sets the name of the app. Write all other custom
environment variables to a file named `.env` in the project root. You can set
any environment variables mentioned in the Flask or Werkzeug docs, but these
are some you might care to know about:

* `FLASK_ENV`: `production` (default), or `development`
* `FLASK_RUN_HOST`: defaults to `127.0.0.1`
* `FLASK_RUN_PORT`: defaults to `5000`
* `INSTANCE_PATH`: where the notes data (in particular the database) is stored
* `WERKZEUG_DEBUG_PIN`: the PIN to enable the Werkzeug debug console. Set to
"off" to disable it if you are sure the app is only listening on localhost.

To initialize the database after the configuration settings have been set,
run the following command. It will create an `instance` directory in the root
of the project and initialize the SQLite database from `schema.sql`.

```
flask init-db
```

Run the project via the `flask` development server:

```
flask run
```

Unless you changed the defaults, you should be able to access the UI on
http://localhost:5000/
