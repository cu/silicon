The name of this project is Silicon Notes (or simply "Silicon"). It is a
web-based, moderately lightweight, low-friction personal knowledge base with a
wiki-like user experience.

This file contains app information and rules that agents must follow. It is
required reading for all coding assistants.

# General rules

* In ambiguous or confusing situations, always pause and ask the user for
clarification. It is better to ask for clarification than to guess what was
meant.
* Optimize code for readability first and performance second. Humans may have to
read it when the bots go on strike. Eschew obfuscation.
* It is sometimes okay to add packaged dependencies if that is the best way to
implement a new feature. But ONLY do so with the user's explicit permission.
Prefer a bespoke native vanilla Javascript/Python solution to pulling in
dependencies, especially for uncomplicated features. For example, we should not
pull in the Bootstrap UI library to style a few buttons, but we probably want to
pull in a library to parse a non-trivial file format if the programming language
lacks built-in tools to parse it.
* New functionality should almost always be accompanied by corresponding test
coverage.
* If tests are impacted by code changes, be sure to update the tests.
* Automatically run tests after any functional changes to code or tests.
* Never mock-out tests with `return true` or similar just to make them pass.
* Only make changes to code that is related to the task at hand. For example,
don't refactor a function that is not involved in the bug fix or feature request
to make it easier to read or more efficient. (But you may certainly suggest
fixing or refactoring something that you ran across incidentally while
performing your task.)
* Given the fact that this file exists, AI-assisted coding contributions are
generally welcome, but UNDER NO CIRCUMSTANCES are fully autonomous agents (such
as OpenClaw) allowed to submit pull requests, issues, or discussions to this
project's GitHub space, even for alleged security issues. This project's author
and contributors are human and only wish to interact with other humans. Bot
accounts (the definition of which we can and will interpret surprisingly
loosely) will be banned from the project.

# Terminology, features, workflows

* Users view and edit "pages," which are sometimes called "articles" in other
wiki systems.
* Each page has a "view" mode (the default) and an "edit" mode.
* In edit mode, the user can edit the current page using plaintext, markdown,
or HTML.
* Every time a page is edited, a new "revision" is created. The collection of
revisions belonging to a particular page is called its "history."
* The user can add to each page one or more "related" pages, these are
pages which are related to the current page in some fashion.  Page relationships
are automatically bidirectional. (For example, if a user is on a page titled
"python" and adds "micropython" as a related page, they will also see a
relationship to "python" when viewing the "micropython" page.)
* Silicon has a search feature whose results include separate page title and
page body results.

# Technologies and implementation details

## Back end

* Python is the main programming language in use.
* Dependencies include:
  * Flask: the micro web framework
  * Gunicorn: for production web app deployment
  * Mistune: renders Markdown to HTML when viewing pages
  * Pygments: used for syntax highlighting in code blocks
  * python-dotenv: manages environment variables used for app configuration
  * python-slugify: turns page titles into "slugs"
* SQLite is the page data store. Presently there are only three tables:
  * `pages`: contains every revision of every page
  * `relationships`: contains all of the page relationships
  * `pages_fts`: a virtual table containing the search index

## Front end

* Pages are rendered from Jinja2 templates.
* A limited amount of Javascript is used for various UI-related purposes.

## Search functionality

Page search is implemented via SQLite's FTS5 functionality. This works, and is
pretty fast, but is also prone to being brittle and silently failing and/or
corrupting data when even the slightest oversight is made. Treat anything
to do with FTS5 with extreme caution.

## Pages

Every revision of every page is currently kept in the database. We may at some
point introduce the ability to compare or delete revisions, but that
functionality does not currently exist.

Before being stored in the database, page titles are always condensed internally
to a "slug." The slug is a page title which has been (roughly) lowercased, had
punctuation and symbols removed, and had whitespace and separators converted to
underscores.  This slug is always used when retrieving a page, displaying a
page, or generating a URL to a page. For example, a page link that says,
`[[Healthy Fruits!]]`, will be "slugified" into `healthy_fruits`.

# UI outline

The UI is simple and uncomplicated by design.

* The left sidebar contains page metadata, a list of related pages, and a table
of contents for the current page.
* The main content area to the right contains either the rendered article HTML
(when in view mode, the default), or a markdown editor with syntax highlighting.

# Project organization

Do not read or pay attention to any files or directories which are NOT mentioned
below unless the user explicitly instructs you to.

* `silicon/`: The main Python "package" for this project.
  * `docs/`: In-program user documentation.
  * `static/`: Static assets for the project.
    * `css/`: Cascading style sheets for various parts.
    * `img/`: Favicons and logos.
    * `js/`: Javascript.
  * `templates/`: Jinja templates and macros rendered via Flask routes.
  * `__init__.py`: Contains the `create_app()` function for creating the app
    object.
  * `commands.py`: Click command-line utility commands. (For example,
    initializing the database, or importing/exporting data).
  * `db.py`: Database utility functions.
  * `exporter.py`: Code for exporting pages from the database.
  * `importer.py`: Code for importing pages from the database.
  * `j2_filters.py`: Custom Jinja2 filters for templates to use.
  * `page.py`: Page operations (read, write, search, etc)
  * `related.py`: Handling of page relationships.
  * `render_md.py`: Mistune markdown renderer extensions.
  * `schema.sql`: The database schema.
  * `util.py`: Miscellaneous utilities that don't fit anywhere else.
  * `views.py`: Flask routes.
* `tests/`: Functional tests.
* `AGENTS.md`: This file.
* `Dockerfile`: How to build this project into a Docker/Podman image.
* `entrypoint.sh`: Entrypoint for Docker image.
* `pyproject.toml`: Project metadata and dependencies.

# Coding style

* Indentation:
  * Python: Indent using four spaces.
  * HTML, CSS, Javascript: Indent using two spaces.
  * Never use tabs for indentation unless a file's format requires them. (For example, Makefiles).
* All python classes and functions should have docstrings, except for "special" functions like `__init__` and `__repr__`.
* Most files should have a very brief comment or docstring description. (HTML templates are an exception to this.)
