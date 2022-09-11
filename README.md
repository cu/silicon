# What's all this, then?!

Silicon Notes: A somewhat lightweight, low-friction personal knowledge base.

Features:

* Plaintext editing in Markdown, rendering in HTML
* Language syntax highlighting in rendered HTML
* Bi-directional page relationships
* Powerful full-text and page title search
* Page history
* A table of contents in the left sidebar, where it belongs
* A quite-usuable mobile layout
* Built-in documentation
* No-frills UI
* No big frameworks, just a few smallish dependencies

For the rationale on why this was created and paper-thin justifications on
certain design decisions, see [DESIGN.md](./DESIGN.md).

<a href="https://gist.githubusercontent.com/cu/addb3a5f6ba1de11b8fb5eedd212d82a/raw/58e80468acbdd832d012fd776afac6d58357cbb3/view_full.png">
  <img src="https://gist.githubusercontent.com/cu/addb3a5f6ba1de11b8fb5eedd212d82a/raw/58e80468acbdd832d012fd776afac6d58357cbb3/view_full.png" width="400" height="275">
</a>

<a href="https://gist.githubusercontent.com/cu/addb3a5f6ba1de11b8fb5eedd212d82a/raw/bd5c9022462fe6aa6fd239b07a56777275bccf85/view_full_codemirror.png">
  <img src="https://gist.githubusercontent.com/cu/addb3a5f6ba1de11b8fb5eedd212d82a/raw/bd5c9022462fe6aa6fd239b07a56777275bccf85/view_full_codemirror.png" width="400" height="275">
</a>

<a href="https://gist.githubusercontent.com/cu/addb3a5f6ba1de11b8fb5eedd212d82a/raw/58e80468acbdd832d012fd776afac6d58357cbb3/view_mobile.png">
  <img src="https://gist.githubusercontent.com/cu/addb3a5f6ba1de11b8fb5eedd212d82a/raw/58e80468acbdd832d012fd776afac6d58357cbb3/view_mobile.png" width="248" height="275">
</a>

# Tech Stack

Projects we rely on and appreciate!

* [Python](https://www.python.org/), of course.
* [Poetry](https://python-poetry.org/) for project management.
* [Flask](https://flask.palletsprojects.com/), the micro-framework.
* [Mistune](https://github.com/lepture/mistune) to render Markdown into HTML.
* [Pygments](https://pygments.org/) for syntax highlighting of code blocks.
* [python-slugify](https://github.com/un33k/python-slugify) creates URL-friendly
  "slugs" from strings.
* [python-dotenv](https://github.com/theskumar/python-dotenv) for configuration
  management.
* [Gunicorn](https://gunicorn.org/) for deployment.
* [Pytest](https://pytest.org/) and
  [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for functional testing.
* [CodeMirror](https://codemirror.net/) (optional) for editor syntax
  highlighting


# Quickstart

This project is configured and deployed much like any other Flask project.
For details, see the [Flask configuration handling Docs].

[Flask configuration handling docs]: https://flask.palletsprojects.com/en/1.1.x/config/

## Docker

If you want to take this for a quick spin and have Docker installed, a
`Dockerfile` and a `docker-compose.yaml` file are provided, so you can build
the container with:

```sh
docker build -t silicon .
```

Silicon will listen on port 5000 (plaintext HTTP) and stores all application
data in `/home/silicon/instance`.

If you use `docker-compose`, you can simply run this command to build and
start the application:

```sh
docker-compose up
```

## Development

### Pre-requisites

This project requires Python 3.9 or greater. On a Debian/Ubuntu system, that
means the following packages:

* `python3`
* `python3-pip` (unless installed via other means)
* `python3-dev`
* `python3-venv`
* `npm` (or `docker`) (optional to enable CodeMirror editor)

Install [Poetry](https://python-poetry.org/) if necessary. Everyone has their
own way of setting up their Python tooling but I'm a fan of
[pipx](https://github.com/pypa/pipx):

```
pip3 install --user pipx
pipx install poetry
```

Use poetry to create a virtual environment and install the dependencies:

```
poetry install
```

Flask is configured via environment variables. There is a file called
`.flaskenv` which sets the name of the app. If you want to run `flask` from
somewhere else, you will need to set:

```
FLASK_APP=silicon
```

All other settings can either be set as environment variables or written to a
file named `.env` in the project root. For development, this will suffice:

```
FLASK_ENV=development
WERKZEUG_DEBUG_PIN=off
```

You can set any environment variables mentioned in the Flask or Werkzeug
docs, but these are some you might care to know about:

* `FLASK_ENV`: `production` (default), or `development`
* `FLASK_RUN_HOST`: defaults to `127.0.0.1`
* `FLASK_RUN_PORT`: defaults to `5000`
* `INSTANCE_PATH`: where the silicon data (in particular the database) is stored
* `WERKZEUG_DEBUG_PIN`: the PIN to enable the Werkzeug debug console. Set to
  "off" to disable it if you are sure the app is only listening on localhost.
* `SECRET_KEY`: A string used in session cookies. For development purposes, this
  can be anything, but for production it should be a 16-byte (or larger) string
  of random characters. Setting this is optional as the app will create one
  (and write it to a file in `INSTANCE_PATH`) if one doesn't exist.

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


# Production Deployment

Be aware that this is a web application which contains no authentication or
security mechanisms whatsoever. Those are up to you to provide. Otherwise,
you should only deploy this to a trusted private network such as a local LAN
segregated from the public Internet by a firewall or VPN. **If deploying on a
public server, you are responsible for ensuring all access to it is secure.**
One simple option may be deploying it behind an HTTPS proxy with HTTP Basic
Authentication enabled.


## Configuring the CodeMirror Editor

Support for [CodeMirror](https://codemirror.net) as a text editor is
included by default. It does add a lot of "heft" to the
UI, mostly around having to make a separate network request for each language
and addon specified. To disable CodeMirror and use a regular textarea instead,
add the following to your `.env` or environment:

```
SILICON_EDITOR=textarea
```

You also have to install third-party Javascript/CSS static packages:

```
(cd silicon/static && npm install)
```

Or, if you'd rather just use npm from inside a docker container:

```
docker run -ti --rm -v $PWD/silicon/static:/app -w /app node:alpine npm install
```

Currently only a handful of languages are enabled for syntax highlighting, if
you want to edit the list to suit your needs, you can edit
`silicon/static/js/edit.js`. You can find a list of supported lanauges
[here](https://codemirror.net/mode/).

## Running tests

To run the tests, install the test dependencies and run `pytest`:

```
poetry run pytest
```

If you have a tmpfs filesystem, you can set the `TMP` environment variable to
have test databases created there (which is faster and results in less
wear-and-tear on your disk):

```
TMP=/dev/shm poetry run pytest
```


# Suggested Contributions

## Clean Up CSS

The current style sheets were more or less arrived at by trial and error. Any
help in organizing the rules in a more coherent yet extensible way would be
much appreciated.

## Dark Theme

It would be nice if the CSS adjusted itself to a dark theme based on the
preference set by the user in the browser. This should be pretty easy since
almost all of the colors are in one file.

## Clean up Javascript

To put it mildly, my JS skills are not the best. I would very much appreciate
any suggestions on improvements to the small amount of code there is, or
whether there is a better way to organize it. I won't bring in any kind of
Javascript "build" tool as a project dependency, though.

## Diffs Between Revisions

This is pretty standard on wiki-like apps, but it's not a critical feature
for me so I haven't yet mustered up the fortitude to implement it. (It would
also likely involve adding a diff library as a dependency.)

## Redirect to Slugified URL

We currently "slugify" the page title in at least two places:

1. When building the URL for an internal page link generated from wiki link
syntax `[[like this]]` in `render.py`.
2. When processing requests with page titles in the URLs for certain routes in
`views.py`.

In the second case, page titles are slugified immediately, meaning every
instance of the page title is slugified in the HTML. However, the URL will
still contain the non-slugified title. This is pretty much purely cosmetic,
but it would be nice if the application could immediately redirect to a
slugified page title instead, if necessary.

I found lots of ugly ways to do this but nothing I was comfortable shipping.

## Draft Feature / Autosave / Leap-frog Detection

To prevent the loss of unsaved changes while editing, we use the browser's
"are you sure?" nag if there has been a change to the editing area since the
page was loaded. However, there are still (at least) two opportunies to lose
work:

1. The browser crashes.
2. Two simulatenous edits of a page in separate tabs or windows.

The first is rare and the second is not as serious since both revisions are
saved. But it is currently up to the user to recognize what happened and
remedy the situation by hand.

These are technically three separate features but I believe they would be
quite closely coupled if implemented together.

## Refine Tests

The `tests` directory contains functional tests that were deemed the most
important. But they could be better organized and optimized/flexible. Code
coverage is not likely very high. Some tests are lacking or missing because I
was not able to work out the right way to test certain things.

## Add Anchors to Headings

Anchors on headers are a very common feature on various CMSes. They let you
link directly to headings, e.g.:

http://example.com/view/page_title#some-section

## Implement a (Better) Task List Plugin

Mistune (the Markdown->HTML renderer) ships with a [task_lists plugin]. It is
functional, but it renders task list items inside an ordinary `<ol>` as just
another kind of list item. This means the task list items get prefixed with
_both_ a bullet point and a checkbox. IMO, this is fairly ugly and the "right"
way to display a task list item is the have the checkbox replace the bullet
point.

[task_lists plugin]: https://mistune.readthedocs.io/en/latest/plugins.html#task-lists

To do this right, I think task lists should be their own separate kind of list
rather than just another item type in regular lists. It should be possible to
accomplish this with a Mistune plugin.
