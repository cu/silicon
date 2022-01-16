# What's all this, then?

Bityard Notes is designed to be a low-friction personal knowledge base, with a
wiki-like interface.


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


## Installation for development or local use

Install [Poetry](https://python-poetry.org/) if necessary.

Use poetry to create a virtual environment and install the dependencies:

```
poetry install
```

Install third-party Javascript/CSS static packages:

```
(cd notes/static && npm install)
```

Or, if you'd rather just use npm from inside a docker container:

```
docker run -ti --rm -v $PWD/notes/static:/app -w /app node:alpine npm install
```

Flask is configured via environment variables. There is a file called
`.flaskenv` which sets the name of the app. If you want to run `flask` from
somewhere else, you will need to set:

```
FLASK_APP=notes
```

All other settings can either be set as environment variables or written to a
file named `.env` in the project root. For development, this will suffice:

```
FLASK_ENV=development
WERKZEUG_DEBUG_PIN=off
SECRET_KEY=for_dev_use_only
```

You can set any environment variables mentioned in the Flask or Werkzeug
docs, but these are some you might care to know about:

* `FLASK_ENV`: `production` (default), or `development`
* `FLASK_RUN_HOST`: defaults to `127.0.0.1`
* `FLASK_RUN_PORT`: defaults to `5000`
* `INSTANCE_PATH`: where the notes data (in particular the database) is stored
* `WERKZEUG_DEBUG_PIN`: the PIN to enable the Werkzeug debug console. Set to
  "off" to disable it if you are sure the app is only listening on localhost.
* `SECRET_KEY`: A string used in session cookies. For development purposes, this
  can be anything, but for production it should be a 16-byte (or larger) string
  of random characters.

To initialize the database after the configuration settings have been set,
run the following command. It will create an `instance` directory in the root
of the project and initialize the SQLite database from `schema.sql`.

```
poetry run flask init-db
```

Run the project via the `flask` development server:

```
poetry run flask run
```

Unless you changed the defaults, you should be able to access the UI on
http://localhost:5000/

To run the tests, install the test dependencies and run `pytest`:

```
poetry run pytest
```


## Installation for a production deployment

Be aware that this is a web application which contains no authentication or
security mechanisms whatsoever. Only deploy this to a trusted private network
such as a local LAN segregated from the public Internet by a firewall or VPN.
If deploying on a public server, you are responsible for ensuring all access to
it is secure. One example may be deploying it behind an HTTPS proxy with
HTTP basic authentication enabled.

{An example scenario or two go here.}

## Running tests

```
poetry run pytest
```

If you have a tmpfs filesystem, you can set the `TMP` environment variable to
have test databases created there:

```
TMP=/dev/shm poetry run pytest
```


# Terminology


# FAQ


## Why can't I add tags to a page? Or put pages into a heirarchy or namespaces?

Previous iterations of this project supported these features. But I found
that no matter how hard I tried, I ended up using tags and page heirarchies
inconsistently across varous subjects. Some subjects lent themselves to a
nice obvious heirarchical system, others worked better with tags. Still
others didn't fit either well.

First I dropped support for tags because managing an accurate list of
relevant tags for each and every page, and reviewing them on every edit,
became a chore that I grew to loathe. Plus on the development side of things,
saving tags with each revision meant an extra layer of metadata. Since the FTS5
search engine in SQLite is excellent, tags became a labor-intensive redundant
feature.

Until I got rid of heirarchies too. I found that I only ever used them in one
section (my notes on Python) and found myself having to look up the linking
syntax involving namespaces every. Single. Time. Again, thanks to FTS5, I
found that I could do "soft" namespacing via page title prefixes (e.g.
"python_operators" instead of "python/operators") and just find everything I
need through the search which returns matches on both titles and body text.
These days, the pages that make up my section of Python notes look something
like this (after slugifying the page names):

* python
* python_operators
* python_functions
* python_classes
* python_virtual_environments
* (et al)

To put it another way, I want my database of notes to be a tool. They have
very low value on their own, but very high value in conjunction with my
day-to-day work. Any time spent "curating" them is time subtracted from
getting important things done.
