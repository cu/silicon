from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from slugify import slugify

from notes.j2_filters import human_timestamp, mark_query_results
from notes.render_md import md_renderer
#from notes.render_toc import toc_renderer
from notes import page


bp = Blueprint('page', __name__)
bp.add_app_template_filter(human_timestamp)
bp.add_app_template_filter(mark_query_results)


@bp.route('/view/')
@bp.route('/edit/')
@bp.route('/history/')
@bp.route('/')
def home():
    return redirect(url_for(f'{bp.name}.view', title='home'))


@bp.route('/view/<title>')
def view(title):
    title = slugify(title, separator='_')
    if 'revision' in request.args:
        p = page.read(title, request.args.get('revision'))
    else:
        p = page.read(title)

    if p['revision'] is None:
        return render_template('not_found.html.j2', **p), 404
    else:
        p['html'] = md_renderer(p['body'])
        return render_template('view.html.j2', **p)


@bp.route('/edit/<title>', methods=['GET', 'POST'])
def edit(title):
    title = slugify(title, separator='_')
    p = page.read(title)
    if request.method == 'GET':
        return render_template('edit.html.j2', **p)
    elif request.method == 'POST':
        if 'body' not in request.form:
            flash('"body" field missing!')
            return render_template('edit.html.j2', **p)
        # was there a previous revision of the page?
        if p['revision'] == None:
            p['body'] = None
        # only save the page if the new text differs from previous revision
        if p['body'] != request.form['body']:
            error = page.write(title, request.form['body'])
            if error:
                flash(error)
                return render_template('edit.html.j2',
                    title=title, body=request.form['body'])
        return redirect(url_for(f'{bp.name}.view', title=title))


@bp.route('/history/<title>')
def history(title):
    p = {}
    p['title'] = slugify(title, separator='_')
    p['revisions'] = page.history(p['title'])
    p['count'] = len(p['revisions'])
    if p['count'] == 0:
        return render_template('not_found.html.j2', **p), 404
    return render_template('history.html.j2', **p)


@bp.route('/history/<title>/<req_revision>')
def history_revision(title, req_revision):
    title = slugify(title, separator='_')

    p = page.read(title, req_revision)

    # req_revision not found, redirect back to history index
    if p['revision'] is None:
        return redirect(url_for(f'{bp.name}.history', title=title))

    p['req_revision'] = req_revision
    p['revisions'] = page.history(title)
    p['count'] = len(p['revisions'])
    p['html'] = md_renderer(p['body'])

    return render_template('history.html.j2', **p)


@bp.route('/docs/', defaults={'title': 'overview'})
@bp.route('/docs/<title>')
def docs(title):
    return f"Docs for {title}: Not Yet Implemented"


@bp.route('/search')
def search():
    def render_template_err(msg):
        return render_template(
            'search.html.j2',
            err_msg=msg,
            title="Invalid Query"
        )

    query = request.args.get('query', '').strip()
    if not query:
        return render_template_err('No query specified.'), 400
    try:
        title_results, body_results = page.search(request.args['query'])
    except page.SearchError as err:
        return render_template_err(err), 400
    return render_template('search.html.j2',
        title=f"Results for '{request.args['query']}'",
        title_results=title_results,
        body_results=body_results)

# @bp.route('/htmx/toc/<title>')
# def toc(title):
#     title = slugify(title, separator='_')
#     p = page.read(title)
#     if p['revision'] is None:
#         return 'No such page', 404
#     return toc_renderer(p['body'])


@bp.route('/htmx/toc/<title>')
def toc(title):
    return "To be continued"
