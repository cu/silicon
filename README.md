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

Create a virtual env:

```sh
python3 -m venv .venv
. .venv/bin/activate
```

Install the package in editable mode via pip:

```
pip install -e '.[dev]'
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
file named `.env` in the project root. You can set any environment variables
mentioned in the Flask or Werkzeug docs, but these are some you might care to
know about:

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

To run the tests, install the test dependencies and run `pytest`:

```
pip install '.[test]'
pytest
```


## Installation for a production deployment

Be aware that this is a web application which contains no authentication or
security mechanisms whatsoever. Only deploy this to a trusted private network
such as a local LAN segregated from the public Internet by a firewall or VPN.
If deploying on a public server, you are responsible for ensuring all access to
it is secure. One example may be deploying it behind an HTTPS proxy with
HTTP basic authentication enabled.

{An example scenario or two go here.}


# Terminology


# FAQ


## Why can't I add tags to a page? Or put pages into a heirarchy or namespaces?

A previous iteration of this project supported these features, but I decided
to remove them. I found that no matter how hard I tried, I ended up using
tags and page heirarchies inconsistently across varous subjects. Some
sections had a nice obvious heirarchical system, others lent themselves more
to tags. Still others didn't fit either well.

Next I tried ditching tags altogether because managing an accurate list of
relevant tags for each and every page, and reviewing them on every edit,
became a chore that I grew to loathe. Plus on the development side of things,
saving tags with each revision meant an extra layer of metadata. So I got rid
of tags and only supported heirarchies (via namespaces).

Until I got rid of those too. I found that I only ever used them in one
section (my notes on Python) and found myself having to look up the linking
syntax involving namespaces every. single. time. Since SQLite has an awesome
full-text search engine built right in, I found that I could do "soft"
namespacing and just find everything I need through the search which returns
matches on both titles and body text. These days, the pages that make up my
section of Python notes look something like this (after slugifying the page
names):

* python
* python_operators
* python_functions
* python_classes
* python_virtual_environments
* (et al)

To put it another way, I want my notes to be a tool. They have very low value
on their own, but very high value in conjunction with my work. Any time spent
"curating" them is value subtracted from more important endeavours.
