from pathlib import Path

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from slugify import slugify

from silicon.j2_filters import human_timestamp, mark_query_results
from silicon.render_md import md_renderer, toc_renderer
from silicon import page, related


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
        p['relatives'] = related.get(title)
        if 'body' in p:
            p['toc']  = toc_renderer(p['body'])

    if p['revision'] is None:
        return render_template('not_found.html.j2', **p), 404
    else:
        p['html'] = md_renderer(p['body'])
        return render_template('view.html.j2', **p)


@bp.route('/edit/<title>', methods=['GET', 'POST'])
def edit(title):
    title = slugify(title, separator='_')
    p = page.read(title)
    p['relatives'] = related.get(title)
    if 'body' in p:
        p['toc']  = toc_renderer(p['body'])
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


@bp.route('/docs', defaults={'title': 'main'})
@bp.route('/docs/<title>')
def docs(title):
    p = {}

    p['title'] = slugify(title)

    doc = Path(__file__).parent.parent / 'docs' / f'{title}.md'
    try:
        with doc.open() as f:
            body = f.read()
            p['html'] = md_renderer(body)
    except FileNotFoundError:
        p['html'] = f'No documentation for "{title}" found.'
        return render_template('docs.html.j2', **p), 404

    p['toc']  = toc_renderer(body)
    return render_template('docs.html.j2', **p)


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


@bp.route('/toc', methods=['POST'])
def toc():
    if 'body' not in request.form:
        return 'Invalid request', 400
    return toc_renderer(request.form['body'])


@bp.route('/related/<title>')
def get_relatives(title):
    return render_template('related.html.j2',title=title,
        relatives=related.get(title))


@bp.route('/related/<title>', methods=['POST'])
def add_relative(title):
    if 'relative' in request.form:
        related.add(title, request.form['relative'])
    return render_template('related.html.j2',title=title,
        relatives=related.get(title))


@bp.route('/related/<title>/<relative>', methods=['DELETE'])
def delete_relative(title, relative):
    related.delete(title, relative)
    return render_template('related.html.j2',title=title,
        relatives=related.get(title))
