from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from notes.render import get_md_renderer
from notes import page


bp = Blueprint('page', __name__)


@bp.route('/view/')
@bp.route('/edit/')
@bp.route('/history/')
@bp.route('/')
def home():
    return redirect(url_for('page.view', title='home'))


@bp.route('/view/<path:title>')
def view(title):
    if 'revision' in request.args:
        p = page.read(title, request.args.get('revision'))
    else:
        p = page.read(title)

    if p['revision'] is None:
        return render_template('view.html.j2', **p), 404
    else:
        markdown = get_md_renderer()
        p['html'] = markdown(p['body'])
        return render_template('view.html.j2', **p)


@bp.route('/edit/<path:title>', methods=['GET', 'POST'])
def edit(title):
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
        return redirect(url_for('page.view', title=title))

@bp.route('/history/<path:title>')
def history(title):
    return f"History for {title}: Not Yet Implemented"

@bp.route('/docs/', defaults={'title': 'overview'})
@bp.route('/docs/<path:title>')
def docs(title):
    return f"Docs for {title}: Not Yet Implemented"
