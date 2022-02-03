from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from slugify import slugify

from notes.j2_filters import human_timestamp
from notes.render import get_md_renderer
from notes import page


bp = Blueprint('page', __name__)
bp.add_app_template_filter(human_timestamp)


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
        markdown = get_md_renderer()
        p['html'] = markdown(p['body'])
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
    markdown = get_md_renderer()
    p['html'] = markdown(p['body'])

    return render_template('history.html.j2', **p)


@bp.route('/docs/', defaults={'title': 'overview'})
@bp.route('/docs/<title>')
def docs(title):
    return f"Docs for {title}: Not Yet Implemented"
