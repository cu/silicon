[![Integration tests](https://github.com/cu/silicon/actions/workflows/tests.yaml/badge.svg)](https://github.com/cu/silicon/actions/workflows/tests.yaml)

# What's all this, then?!

Silicon Notes: A somewhat lightweight, low-friction personal knowledge base.

![silicon logo](https://gist.githubusercontent.com/cu/addb3a5f6ba1de11b8fb5eedd212d82a/raw/b56dfbf4cd3ac77487e61cfbdeba7519d8b4f487/favicon-view-192.png)

Features:

* Plaintext editing in Markdown, rendering in HTML
* Language syntax highlighting in rendered HTML
* Bi-directional page relationships
* Powerful full-text and page title search
* Page history
* A table of contents in the left sidebar, where it belongs
* A quite-usable mobile layout
* Built-in documentation
* No-frills UI
* No big frameworks, just a few smallish dependencies

For the rationale on why this was created and paper-thin justifications on
certain design decisions, see [this blog article](https://blog.bityard.net/articles/2022/December/the-design-of-silicon-notes-with-cartoons).

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
* [uv](https://github.com/astral-sh/uv) for project management.
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

## Running Locally

See the Development section below for steps on running the app locally.

For production, this project is configured and deployed much like any other
Flask project.  For details, see the [Flask configuration handling Docs].

[Flask configuration handling docs]: https://flask.palletsprojects.com/en/stable/config/

## Docker or Podman

If containers are more your speed, the following commands should get you going.
You obviously need to have [Docker](https://www.docker.com) installed. (If you
have [Podman](https://podman.io), simply substitute `docker` for `podman`.)

```sh
docker run \
  -ti \
  --rm \
  -p 127.0.0.1:5000:5000 \
  -v silicon_instance:/home/silicon/instance \
  docker.io/bityard/silicon
```

And then open http://localhost:5000/ with your local web browser.

You could also start it with `docker-compose` (or `docker compose`):

```sh
cd deploy/docker-local
docker-compose up
```

If you want to build the image, a `Dockerfile` and a `docker-compose.yaml` file
are provided, so you can build the container with:

```sh
docker build -t docker.io/bityard/silicon .
```

Or with buildah:

```sh
buildah build --format docker -t docker.io/bityard/silicon .
```

Silicon will listen on port 5000 (plaintext HTTP) and stores all application
data in `/home/silicon/instance`.

# Development

## Prerequisites

This repo tries to be somewhat flexible about its tools and workflow. However,
along the happy path you will find some combination of Python 3.9 (or better),
`uv`, Docker/Podman, and `npm`.

Install [uv](https://github.com/astral-sh/uv) if necessary. If you are not a fan
of curlpipes, there are many other ways to install it:

* `pip install --user uv`
* `pipx install uv`
* download binaries from the [latest release](https://github.com/astral-sh/uv)

## Setup

Some settings can either be set as environment variables or written to a
file named `.env` in the project root. For development, this will suffice:

```sh
WERKZEUG_DEBUG_PIN=off
```

You can set any environment variables mentioned in the Flask or Werkzeug
docs, but these are some you might care to know about:

* `FLASK_RUN_HOST`: defaults to `127.0.0.1`
* `FLASK_RUN_PORT`: defaults to `5000`
* `INSTANCE_PATH`: where the silicon data (in particular the database) is stored
* `WERKZEUG_DEBUG_PIN`: the PIN to enable the Werkzeug debug console. Set to
  "off" to disable it if you are sure the app is only listening on localhost.
* `SECRET_KEY`: A string used in session cookies. For development purposes, this
  can be anything, but for production it should be a 16-byte (or larger) string
  of random characters. Setting this is optional as the app will create one
  (and write it to a file in `INSTANCE_PATH`) if one doesn't exist.
* `SILICON_EDITOR`: When set to `textarea`, this disables the CodeMirror text
  editor when editing pages and uses a standard textarea element instead.

To initialize the database after the configuration settings have been set, run
the `init-db` command as described below. It will create an `instance` directory
in the root of the project and initialize the SQLite database from `schema.sql`.

## Commands

[Poethepoet](https://poethepoet.natn.io/index.html) is used as a task runner.
There are two ways to use it:

**With `uv run`:**

It is automatically installed as a dev dependency and has some `uv` integration,
so you can run:

```sh
uv run poe <command>
```

**Global install**

If you install the `poethepoet` package via `uv tool install` or `pipx install`,
then you can save yourself some typing:

```sh
poe <command>
```

These are the currently-supported commands. You can browse `pyproject.toml` to
see how they are defined if you are curious:

* `init-db`: Initialize the database.
* `devserver`: Run a development server on http://localhost:5000/.
* `test`: Run the integration tests.
* `flake8`: Run the flake8 checker.
* `npm`: Install front-end JS dependencies.
* `npm-docker`: Install front-end JS dependencies via docker.

# Production Deployment

Silicon Notes is a fairly simple web application which contains no built-in
authentication or authorization mechanisms whatsoever. If deploying the
application on its own, you should only deploy this to a trusted private network
such as a local LAN segregated from the public Internet by a firewall or VPN.
**If deploying on a public server, you are responsible for ensuring all access
to it is secure.**

The `deploy` direcctory contains various sample deployments that may be helpful
as starting points for a production deployment.

Normally, it is easiest to host applications like this on their own domain or
subdomain, such as https://silicon.example.com/. If you would rather host it
under a prefix instead (as in https://example.com/silicon), see [this
issue](https://github.com/cu/silicon/issues/3) for hints on how to do that.

# Configuring the CodeMirror Editor

Support for [CodeMirror](https://codemirror.net) as a text editor is included by
default. It does add a lot of "heft" to the UI, mostly around having to make a
separate network request for each language and addon specified. To use it, you
also have to install third-party Javascript/CSS static packages by running ONE
of the following commands:

```sh
# If you have `npm` installed
uv run poe npm
```

Or:

```sh
# if you have `docker` installed
uv run poe npm-docker
```

Currently only a handful of languages are enabled for syntax highlighting, if
you want to edit the list to suit your needs, you can edit
`silicon/static/js/edit.js`. You can find a list of supported lanauges
[here](https://codemirror.net/mode/).

To disable CodeMirror and use a regular textarea instead, add the following to
your `.env` file or environment:

```sh
SILICON_EDITOR=textarea
```

# Data Export and Import

There are two schools of thought where it comes to data storage on note-taking
systems:

1. Throw everything into plaintext files. This makes the data far easier to
read/edit with any file browser and text editor and is inherently portable. But
it forces the app developer to either reimplement many of the nicities that you
get for free with a database system, or abandon them entirely.
2. Throw everything into a database (relational or otherwise) because database
systems tend to take care of most of the heavy lifting. They offer a variety of
features that fit very well with note-taking, content, and knowledge systems in
general. The downside is that viewing and exporting the data outside of the
application itself can get cumbersome in a hurry, especially if you don't
already know SQL and the app's table structure.

Silicon attempts to straddle these two by paying close attention to the goals.
As a user, I want my data easily accessible outside of the application when
necessary without jumping through a lot of hoops. But as a developer, I don't
want to reinvent a perfectly good wheel.

To that end, Silicon supports robust exporting and importing of data in an
attempt to get the best of both worlds and to facilitiate any significant
changes to the storage layer going forward. This is still a work in progress but
for now, the following commands are supported:

```sh
uv run poe export
```

This exports all pages (and all revisions) to an `export` directory under the
instance path. Each page has its own file named `<page_name>.json`. The JSON
file structure is documented in `silicon/exporter.py`.

To import pages from JSON files in the `export` directory:

```sh
uv run poe import
```

This will read all `.json` files from the `export` directory and import them
into the database. If a database does not already exist, this will create one
and then perform the import. If a database _does_ exist, it will refuse to
import unless the `--force` flag is specified. In the case that a specific
revision of a given page already exists, the body will be overwritten. This
allows for merging two divergent exports in a "last import wins" fashion.

Future versions of this command may support exporting and importing individual
pages (and revisions) as markdown as well as other more flexible forms of
export.

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
functional, but it renders task list items inside an ordinary `<ul>` as just
another kind of list item. This means the task list items get prefixed with
_both_ a bullet point and a checkbox. IMO, this is fairly ugly and the "right"
way to display a task list item is the have the checkbox replace the bullet
point.

[task_lists plugin]: https://mistune.readthedocs.io/en/latest/plugins.html#task-lists

To do this right, I think task lists should be their own separate kind of list
rather than just another item type in regular lists. It should be possible to
accomplish this with a Mistune plugin.

# Release Process

1. Set the `version` string in `pyproject.toml` to the version to be released.
1. Run `uv lock`.
1. Commit `pyproject.toml` and `uv.lock`.
1. Push a tag containing just the version number. The tag has to be pushed before a release can be made. GitHub will use the tag name as the release name, so a tag prefix as in `release-1.2.3` will not be kosher.
   ```
   git log -1
   git tag <version> <commit>
   git push origin <version>
   ```
1. This will kick off an action to build a container for each arch and tag/push:
   * `latest`
   * major.minor.patch
1. Create a release in GitHub containing URLs to docker images.
